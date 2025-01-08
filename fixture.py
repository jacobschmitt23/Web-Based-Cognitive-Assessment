from model.models import *
import random
import datetime
import numpy

# Example: Generate fake data for doctorLink, dataTable, individualTable, etc.
def generate_fake_data(size=1600,numDiffLinks=18):
    # Create the doctors
    doctor1 = User.objects.create_user(username='Doctor Who', password='who')
    doctor2 = User.objects.create_user(
        username='Doctor Strange', password='strange')
    doctor3 = User.objects.create_user(username='Doctor Doom', password='doom')
    doctors = [doctor1, doctor2, doctor3]
    # Number of sections and ppst
    num_sections = size//4
    num_ppst = size//16

    # The means and sd are derived from the averages of the fields across the tests from the "A DIGITAL APPLICATION FOR ASSESSMENT OF NEUROCOGNITIVE DISABILITIES" paper
    latency_data = {
        '4SpanDigit': {
            'latency1': make_normal_dist(mean=1.84, sd=1.01, low=.2, size=num_sections),
            'latency2': make_normal_dist(mean=2.72, sd=1.28, low=.2, size=num_sections),
            'latency3': make_normal_dist(mean=3.73, sd=1.73, low=.2, size=num_sections),
            'latency4': make_normal_dist(mean=4.36, sd=1.97, low=.2, size=num_sections)
        },
        '4SpanMixed': {
            'latency1': make_normal_dist(mean=2.50, sd=.94, low=.2, size=num_sections),
            'latency2': make_normal_dist(mean=.87, sd=.41, low=.2, size=num_sections),
            'latency3': make_normal_dist(mean=2.20, sd=.86, low=.2, size=num_sections),
            'latency4': make_normal_dist(mean=.91, sd=1.69, low=.2, size=num_sections)
        },
        '5SpanDigit': {
            'latency1': make_normal_dist(mean=2.13, sd=1.28, low=.2, size=num_sections),
            'latency2': make_normal_dist(mean=.99, sd=.54, low=.2, size=num_sections),
            'latency3': make_normal_dist(mean=1.72, sd=1.37, low=.2, size=num_sections),
            'latency4': make_normal_dist(mean=1.30, sd=.99, low=.2, size=num_sections),
            'latency5': make_normal_dist(mean=.56, sd=.34, low=.2, size=num_sections)
        },
        '5SpanMixed': {
            'latency1': make_normal_dist(mean=2.99, sd=1.61, low=.2, size=num_sections),
            'latency2': make_normal_dist(mean=.85, sd=.55, low=.2, size=num_sections),
            'latency3': make_normal_dist(mean=2.44, sd=2.91, low=.2, size=num_sections),
            'latency4': make_normal_dist(mean=1.92, sd=1.23, low=.2, size=num_sections),
            'latency5': make_normal_dist(mean=.96, sd=1.38, low=.2, size=num_sections)
        }
    }
    # The means and sd are derived from the averages of the fields across the tests from the "A DIGITAL APPLICATION FOR ASSESSMENT OF NEUROCOGNITIVE DISABILITIES" paper
    score4SpanDigitData = make_normal_dist(
        mean=98.96, sd=5.26, low=0, high=100, size=num_sections)
    idx4SpanDigit = 0
    score4SpanMixedData = make_normal_dist(
        mean=91.69, sd=13.76, low=0, high=100, size=num_sections)
    idx4SpanMixed = 0
    score5SpanDigitData = make_normal_dist(
        mean=90.64, sd=13.17, low=0, high=100, size=num_sections)
    idx5SpanDigit = 0
    score5SpanMixedData = make_normal_dist(
        mean=74.88, sd=17.85, low=0, high=100, size=num_sections)
    idx5SpanMixed = 0

    # Create the doctor links and individual tables
    for i in range(num_ppst):
        doctor = random.choice(doctors)
        doctor_link = doctorLink.objects.create(
            linkID=f"{i+1:05}", doctor=doctor)

        age = random.randint(10, 100)
        # Create the individual table
        ind_table = individualTable.objects.create(
            linkID=doctor_link,
            age=age,
            completed=individualTable.completedStatus.COMPLETED,
            avgLatency1=None,
            avgLatency2=None,
            avgLatency3=None,
            avgLatency4=None,
            avgLatency5=None,
            avgDuration=None,
            avg4SpanScore=None,
            avg5SpanScore=None,
            avgScoreDigit=None,
            avgScoreMixed=None,
            avgScore=None
        )
        # Create the individual result tables
        for j in range(16):
            if (j == 0 or (j > 1 and j < 5)):
                test_type = '4SpanDigit'
                span = 4
                score = score4SpanDigitData[idx4SpanDigit]
                idx4SpanDigit += 1
            elif (j == 1 or (j > 4 and j < 8)):
                test_type = '5SpanDigit'
                span = 5
                score = score5SpanDigitData[idx5SpanDigit]
                idx5SpanDigit += 1
            elif (j == 8 or (j > 9 and j < 13)):
                test_type = '4SpanMixed'
                span = 4
                score = score4SpanMixedData[idx4SpanMixed]
                idx4SpanMixed += 1
            elif (j == 9 or (j > 12 and j < 16)):
                test_type = '5SpanMixed'
                span = 5
                score = score5SpanMixedData[idx5SpanMixed]
                idx5SpanMixed += 1

            score = score / 100
            # Create the individual result table
            ind_result_table = individualResultTable.objects.create(
                indTable=ind_table,
                testName=stimulus[j],
                patientAnswerString=create_patient_answer(
                    score=score, span=span, stim=stimulus[j]),
                startingDayAndTime=None,
                endingDayAndTime=None,
                score=0,
                duration=0
            )
            # Create the latency tables
            if (span == 4):
                latency.objects.create(
                    indResTable=ind_result_table,
                    latency1=latency_data[test_type]['latency1'][i],
                    latency2=latency_data[test_type]['latency2'][i],
                    latency3=latency_data[test_type]['latency3'][i],
                    latency4=latency_data[test_type]['latency4'][i],
                    latency5=None
                )
            else:
                latency.objects.create(
                    indResTable=ind_result_table,
                    latency1=latency_data[test_type]['latency1'][i],
                    latency2=latency_data[test_type]['latency2'][i],
                    latency3=latency_data[test_type]['latency3'][i],
                    latency4=latency_data[test_type]['latency4'][i],
                    latency5=latency_data[test_type]['latency5'][i]
                )

            # Calculate the score and duration for the individual result table
            ind_result_table.calculateScore()
            if j == 0:
                startDate = None
            startDate, endDate = generate_random_times(ind_result_table, startDate)
            ind_result_table.startingDayAndTime = startDate
            ind_result_table.endingDayAndTime = endDate
            startDate = endDate
            ind_result_table.save()
            ind_result_table.calculateDuration()
        # Calculate the averages for the individual table
        ind_table.calculateData()

    for i in range(num_ppst,num_ppst+numDiffLinks):
        if i < num_ppst + (numDiffLinks/3):
            doctor = doctor1
        elif i < num_ppst + (numDiffLinks/3)*2:
            doctor = doctor2
        else:
            doctor = doctor3
        doctor_link = doctorLink.objects.create(
            linkID=f"{i+1:05}", doctor=doctor)
        age = random.randint(10, 100)
        if i % 2 == 0:
            completedStatus = individualTable.completedStatus.INCOMPLETE
        else:
            completedStatus = individualTable.completedStatus.QUIT
        # Create the individual table
        ind_table = individualTable.objects.create(
            linkID=doctor_link,
            age=age,
            completed=completedStatus,
            avgLatency1=None,
            avgLatency2=None,
            avgLatency3=None,
            avgLatency4=None,
            avgLatency5=None,
            avgDuration=None,
            avg4SpanScore=None,
            avg5SpanScore=None,
            avgScoreDigit=None,
            avgScoreMixed=None,
            avgScore=None
        )


# Create a normal distribution of data
def make_normal_dist(mean, sd, size, low, high=0):
    data = []
    while len(data) < size:
        sample = numpy.random.normal(loc=mean, scale=sd, size=size)
        if (high == 0):
            sample_in_range = sample[(sample >= low)]
        else:
            sample_in_range = sample[(sample >= low) & (sample <= high)]
        data.extend(sample_in_range)
    return data[:size]


# Create the patient's answer based on the stimuli and the score
def create_patient_answer(score, span, stim):
    if ('mixed' in stim.name):
        chars = ['2', '3', '4', '5', '6', '7', '8',
                 '9', 'J', 'R', 'W', 'Y', 'F', 'S', 'K', 'U']
    else:
        chars = ['2', '3', '4', '5', '6', '7', '8', '9']
    patientAnswer = ''
    num_correct = 0
    initial_score = score
    for i in range(span):
        character = stim.correctString[i]
        if (random.random() < score):
            patientAnswer += character
            num_correct += 1
        else:
            idx = random.randint(0, len(chars)-1)
            while (chars[idx] == character):
                idx = random.randint(0, len(chars)-1)
            patientAnswer += chars[idx]
        remaining_chars = span - i - 1
        if remaining_chars > 0:
            needed_correct = initial_score * span - num_correct
            if needed_correct == remaining_chars:
                score = 1
            elif needed_correct == 0:
                score = 0
            else:
                score = needed_correct / remaining_chars
    return patientAnswer


# Generate random times for the starting and ending day and time
def generate_random_times(ind_res_table, startDate):
    latencyTables = latency.objects.filter(indResTable=ind_res_table)
    totalDuration = 0
    count = 0
    for latencies in latencyTables:
        latDuration = latencies.getDurationOfTest()
        if (latDuration is not None):
            totalDuration += latDuration
            count += 1
    duration = totalDuration / count

    if startDate is None:
        year = random.randint(2020,2024)
        month = random.randint(1,12)
        day = random.randint(1, 28)
        date = datetime.datetime(year, month, day)
        min = random.randint(0, 23 * 60 + 58)
        sec = random.randint(0, 59)
        startDate = date + datetime.timedelta(minutes=min, seconds=sec)

    endDate = startDate + datetime.timedelta(seconds=duration)

    return startDate, endDate

# Main
# Clear the tables
for c in [User, doctorLink, individualResultTable, individualTable, latency]:
    c.objects.all().delete()

stimulus = getOrderedStimuli()
generate_fake_data()
aggregateData()
