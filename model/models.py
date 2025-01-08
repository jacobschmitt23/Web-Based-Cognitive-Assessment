import datetime
from django.db import models
from django.db.models import Avg, StdDev, Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import sys
import scipy.stats as stats
from django.utils.timezone import now

# Model for the stimuli
class stimuli(models.Model):
    name = models.TextField()
    givenString = models.TextField()
    correctString = models.TextField()

    def __str__(self):
        return f"{self.name}"

# Model for the doctor to patient link
class doctorLink(models.Model):
    linkID = models.TextField()
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.doctor} - LinkID: {self.linkID}"

# Model for the aggregate data table
class aggregateDataTable(models.Model):
    minAge = models.IntegerField()
    maxAge = models.IntegerField()
    numTests = models.IntegerField(default=0)
    avgLatency1 = models.FloatField(null=True, default=None)
    sdLatency1 = models.FloatField(null=True, default=None)
    avgLatency2 = models.FloatField(null=True, default=None)
    sdLatency2 = models.FloatField(null=True, default=None)
    avgLatency3 = models.FloatField(null=True, default=None)
    sdLatency3 = models.FloatField(null=True, default=None)
    avgLatency4 = models.FloatField(null=True, default=None)
    sdLatency4 = models.FloatField(null=True, default=None)
    avgLatency5 = models.FloatField(null=True, default=None)
    sdLatency5 = models.FloatField(null=True, default=None)
    avgDuration = models.FloatField(null=True, default=None)
    sdDuration = models.FloatField(null=True, default=None)
    avg4SpanScore = models.FloatField(null=True, default=None)
    sd4SpanScore = models.FloatField(null=True, default=None)
    avg5SpanScore = models.FloatField(null=True, default=None)
    sd5SpanScore = models.FloatField(null=True, default=None)
    avgScoreDigit = models.FloatField(null=True, default=None)
    sdScoreDigit = models.FloatField(null=True, default=None)
    avgScoreMixed = models.FloatField(null=True, default=None)
    sdScoreMixed = models.FloatField(null=True, default=None)
    avgScore = models.FloatField(null=True, default=None)
    sdScore = models.FloatField(null=True, default=None)
    avg4SpanDigitScore = models.FloatField(null=True, default=None)
    sd4SpanDigitScore = models.FloatField(null=True, default=None)
    avg4SpanMixedScore = models.FloatField(null=True, default=None)
    sd4SpanMixedScore = models.FloatField(null=True, default=None)
    avg5SpanDigitScore = models.FloatField(null=True, default=None)
    sd5SpanDigitScore = models.FloatField(null=True, default=None)
    avg5SpanMixedScore = models.FloatField(null=True, default=None)
    sd5SpanMixedScore = models.FloatField(null=True, default=None)
    avg4SpanScoreUnordered = models.FloatField(null=True, default=None)
    sd4SpanScoreUnordered = models.FloatField(null=True, default=None)
    avg5SpanScoreUnordered = models.FloatField(null=True, default=None)
    sd5SpanScoreUnordered = models.FloatField(null=True, default=None)
    avgScoreDigitUnordered = models.FloatField(null=True, default=None)
    sdScoreDigitUnordered = models.FloatField(null=True, default=None)
    avgScoreMixedUnordered = models.FloatField(null=True, default=None)
    sdScoreMixedUnordered = models.FloatField(null=True, default=None)
    avgScoreUnordered = models.FloatField(null=True, default=None)
    sdScoreUnordered = models.FloatField(null=True, default=None)
    avg4SpanDigitScoreUnordered = models.FloatField(null=True, default=None)
    sd4SpanDigitScoreUnordered = models.FloatField(null=True, default=None)
    avg4SpanMixedScoreUnordered = models.FloatField(null=True, default=None)
    sd4SpanMixedScoreUnordered = models.FloatField(null=True, default=None)
    avg5SpanDigitScoreUnordered = models.FloatField(null=True, default=None)
    sd5SpanDigitScoreUnordered = models.FloatField(null=True, default=None)
    avg5SpanMixedScoreUnordered = models.FloatField(null=True, default=None)
    sd5SpanMixedScoreUnordered = models.FloatField(null=True, default=None)
    avgScoreStim1 = models.FloatField(null=True, default=None)
    sdScoreStim1 = models.FloatField(null=True, default=None)
    avgScoreStim2 = models.FloatField(null=True, default=None)
    sdScoreStim2 = models.FloatField(null=True, default=None)
    avgScoreStim3 = models.FloatField(null=True, default=None)
    sdScoreStim3 = models.FloatField(null=True, default=None)
    avgScoreStim4 = models.FloatField(null=True, default=None)
    sdScoreStim4 = models.FloatField(null=True, default=None)
    avgScoreStim5 = models.FloatField(null=True, default=None)
    sdScoreStim5 = models.FloatField(null=True, default=None)
    avgDurationWholeTest = models.FloatField(null=True, default=None)
    sdDurationWholeTest = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"{self.minAge} - {self.maxAge}"


# Model for the individual table
class individualTable(models.Model):
    # Choices for the completed status
    class completedStatus(models.TextChoices):
        COMPLETED = 'COMPLETED','Completed'
        INCOMPLETE = 'INCOMPLETE','Incomplete'
        QUIT = 'QUIT','Quit'
    linkID = models.ForeignKey(
        doctorLink, on_delete=models.CASCADE, blank=True, null=True)
    dateAndtime = models.DateTimeField(default=now)
    age = models.IntegerField(null=True)
    completed = models.CharField(max_length=10, choices=completedStatus.choices, default=completedStatus.INCOMPLETE)
    avgLatency1 = models.FloatField(null=True)
    avgLatency2 = models.FloatField(null=True)
    avgLatency3 = models.FloatField(null=True)
    avgLatency4 = models.FloatField(null=True)
    avgLatency5 = models.FloatField(null=True)
    avgDuration = models.FloatField(null=True)
    avg4SpanScore = models.FloatField(null=True)
    avg5SpanScore = models.FloatField(null=True)
    avgScoreDigit = models.FloatField(null=True)
    avgScoreMixed = models.FloatField(null=True)
    avgScore = models.FloatField(null=True)

    # Calculate the average values for the individualTable
    def calculateData(self):
        # Get all related results for this individualTable
        results = individualResultTable.objects.filter(indTable=self).exclude(testName__name__icontains="Practice")

        # Calculate average latency values for each latency field
        # Double underscore filters across relationships
        # Avg deals with nulls so it is ok if some of the rows have nulls
        latencies = latency.objects.filter(indResTable__indTable=self).exclude(indResTable__testName__name__icontains="Practice")
        avg_latencies = latencies.aggregate(
            avg_lat1=Avg('latency1'),
            avg_lat2=Avg('latency2'),
            avg_lat3=Avg('latency3'),
            avg_lat4=Avg('latency4'),
            avg_lat5=Avg('latency5')
        )
        self.avgLatency1 = avg_latencies['avg_lat1'] or 0
        self.avgLatency2 = avg_latencies['avg_lat2'] or 0
        self.avgLatency3 = avg_latencies['avg_lat3'] or 0
        self.avgLatency4 = avg_latencies['avg_lat4'] or 0
        self.avgLatency5 = avg_latencies['avg_lat5'] or 0

        # Calculate the average duration from the individualResultTable
        self.avgDuration = results.aggregate(Avg('duration'))[
            'duration__avg'] or 0

        # Calculate average 4-span score
        four_span_tests = ['First digit 4 span', 'Second digit 4 span', 'Third digit 4 span',
                           'First mixed 4 span', 'Second mixed 4 span', 'Third mixed 4 span']
        avg4_span_scores = results.filter(
            testName__name__in=four_span_tests).aggregate(Avg('score'))['score__avg'] or 0
        self.avg4SpanScore = avg4_span_scores

        # Calculate average 5-span score
        five_span_tests = ['First digit 5 span', 'Second digit 5 span', 'Third digit 5 span',
                           'First mixed 5 span', 'Second mixed 5 span', 'Third mixed 5 span']
        avg5_span_scores = results.filter(
            testName__name__in=five_span_tests).aggregate(Avg('score'))['score__avg'] or 0
        self.avg5SpanScore = avg5_span_scores

        # Calculate average score for digit tests
        digit_tests = ['First digit 4 span', 'Second digit 4 span', 'Third digit 4 span',
                       'First digit 5 span', 'Second digit 5 span', 'Third digit 5 span']
        avg_score_digit = results.filter(testName__name__in=digit_tests).aggregate(
            Avg('score'))['score__avg'] or 0
        self.avgScoreDigit = avg_score_digit

        # Calculate average score for mixed tests
        mixed_tests = ['First mixed 4 span', 'Second mixed 4 span', 'Third mixed 4 span',
                       'First mixed 5 span', 'Second mixed 5 span', 'Third mixed 5 span']
        avg_score_mixed = results.filter(testName__name__in=mixed_tests).aggregate(
            Avg('score'))['score__avg'] or 0
        self.avgScoreMixed = avg_score_mixed

        # Calculate the overall average score
        self.avgScore = (avg_score_digit + avg_score_mixed) / 2

        # If the individualTable has all the results, set the status to completed
        self.completed = self.completedStatus.COMPLETED

        # Save the updated averages back to the database
        self.save()


    def calculateExtraData(self):
        # Initialize dictionary that will be returned with values
        data = {}

        # Get all related results for this individualTable
        results = individualResultTable.objects.filter(indTable=self).exclude(testName__name__icontains="Practice")

        # Calculate average score for 4 span digit tests
        four_span_digit_test = ['First digit 4 span', 'Second digit 4 span', 'Third digit 4 span']
        four_span_digit = results.filter(testName__name__in=four_span_digit_test)
        avg_four_span_digit = four_span_digit.aggregate(Avg('score'))['score__avg'] or 0
        data["4SpanDigitScore"] = avg_four_span_digit

        # Calculate average score unordered for 4 span digit tests
        sum = 0
        for test in four_span_digit:
            sum += test.calculateScoreUnordered()
        data["4SpanDigitScoreUnordered"] = sum / len(four_span_digit_test)

        #Calculate average score for 4 span mixed tests
        four_span_mixed_test = ['First mixed 4 span', 'Second mixed 4 span', 'Third mixed 4 span']
        four_span_mixed = results.filter(testName__name__in=four_span_mixed_test)
        avg_four_span_mixed = four_span_mixed.aggregate(Avg('score'))['score__avg'] or 0
        data["4SpanMixedScore"] = avg_four_span_mixed

        # Calculate average score unordered for 4 span mixed tests
        sum = 0
        for test in four_span_mixed:
            sum += test.calculateScoreUnordered()
        data["4SpanMixedScoreUnordered"] = sum / len(four_span_mixed_test)

        # Calculate average score for 5 span digit tests
        five_span_digit_test = ['First digit 5 span', 'Second digit 5 span', 'Third digit 5 span']
        five_span_digit = results.filter(testName__name__in=five_span_digit_test)
        avg_five_span_digit = five_span_digit.aggregate(Avg('score'))['score__avg'] or 0
        data["5SpanDigitScore"] = avg_five_span_digit

        # Calculate average score unordered for 5 span digit tests
        sum = 0
        for test in five_span_digit:
            sum += test.calculateScoreUnordered()
        data["5SpanDigitScoreUnordered"] = sum / len(five_span_digit_test)

        # Calculate average score for 5 span mixed tests
        five_span_mixed_test = ['First mixed 5 span', 'Second mixed 5 span', 'Third mixed 5 span']
        five_span_mixed = results.filter(testName__name__in=five_span_mixed_test)
        avg_five_span_mixed = five_span_mixed.aggregate(Avg('score'))['score__avg'] or 0
        data["5SpanMixedScore"] = avg_five_span_mixed

        # Calculate average score unordered for 5 span mixed tests
        sum = 0
        for test in five_span_mixed:
            sum += test.calculateScoreUnordered()
        data["5SpanMixedScoreUnordered"] = sum / len(five_span_mixed_test)

        # Calculate average score unordered for 4 span tests
        four_span_tests = ['First digit 4 span', 'Second digit 4 span', 'Third digit 4 span',
                           'First mixed 4 span', 'Second mixed 4 span', 'Third mixed 4 span']
        four_span = results.filter(testName__name__in=four_span_tests)
        sum = 0
        for test in four_span:
            sum += test.calculateScoreUnordered()
        data["4SpanScoreUnordered"] = sum / len(four_span_tests)

        # Calculate average score unordered for 5 span tests
        five_span_tests = ['First digit 5 span', 'Second digit 5 span', 'Third digit 5 span',
                           'First mixed 5 span', 'Second mixed 5 span', 'Third mixed 5 span']
        five_span = results.filter(testName__name__in=five_span_tests)
        sum = 0
        for test in five_span:
            sum += test.calculateScoreUnordered()
        data["5SpanScoreUnordered"] = sum / len(five_span_tests)

        # Calculate average score unordered for digit tests
        digit_tests = ['First digit 4 span', 'Second digit 4 span', 'Third digit 4 span',
                       'First digit 5 span', 'Second digit 5 span', 'Third digit 5 span']
        digit = results.filter(testName__name__in=digit_tests)
        sum = 0
        for test in digit:
            sum += test.calculateScoreUnordered()
        data["ScoreDigitUnordered"] = sum / len(digit_tests)

        # Calculate average score unordered for mixed tests
        mixed_tests = ['First mixed 4 span', 'Second mixed 4 span', 'Third mixed 4 span',
                       'First mixed 5 span', 'Second mixed 5 span', 'Third mixed 5 span']
        mixed = results.filter(testName__name__in=mixed_tests)
        sum = 0
        for test in mixed:
            sum += test.calculateScoreUnordered()
        data["ScoreMixedUnordered"] = sum / len(mixed_tests)

        # Calculate the overall average score unordered
        data["ScoreUnordered"] = (data["ScoreDigitUnordered"] + data["ScoreMixedUnordered"]) / 2

        # Calculate the scores for each character in the stimuli
        sums = [0,0,0,0,0]
        for test in results:
            scores = test.calculateScorePerChar()
            for i in range(len(scores)):
                sums[i] += scores[i]
        num_tests = len(results)
        data["ScoreStim1"] = sums[0] / num_tests
        data["ScoreStim2"] = sums[1] / num_tests
        data["ScoreStim3"] = sums[2] / num_tests
        data["ScoreStim4"] = sums[3] / num_tests
        data["ScoreStim5"] = sums[4] / (num_tests / 2) 

        # Calculate the duration for the whole test
        sum = 0
        for test in results:
            duration = test.duration
            if duration is not None:
                sum += duration
        data["DurationWholeTest"] = sum

        return data


    def getAllFields(self):
        allFields = {
            'linkID': self.linkID,
            'dateAndtime': self.dateAndtime,
            'age': self.age,
            'completed': self.completed,
            'avgLatency1': self.avgLatency1,
            'avgLatency2': self.avgLatency2,
            'avgLatency3': self.avgLatency3,
            'avgLatency4': self.avgLatency4,
            'avgLatency5': self.avgLatency5,
            'avgDuration': self.avgDuration,
            'avg4SpanScore': self.avg4SpanScore,
            'avg5SpanScore': self.avg5SpanScore,
            'avgScoreDigit': self.avgScoreDigit,
            'avgScoreMixed': self.avgScoreMixed,
            'avgScore': self.avgScore
        }
        return allFields

    def __str__(self):
        return f"{self.linkID} - Avg Score: {self.avgScore} - Avg Duration: {self.avgDuration}"

# Model for the individual result table
class individualResultTable(models.Model):
    indTable = models.ForeignKey(
        individualTable, on_delete=models.CASCADE, blank=True, null=True)
    testName = models.ForeignKey(
        stimuli, on_delete=models.CASCADE, blank=True, null=True)
    patientAnswerString = models.TextField(null=True)
    startingDayAndTime = models.DateTimeField(null=True)
    endingDayAndTime = models.DateTimeField(null=True)
    score = models.FloatField(null=True)
    duration = models.FloatField(null=True)

    # These 3 calculate scores loop over the same thing so should really be one function returning/saving all these aspects but would have to change other implementation
    # Calculate the score for the single span test
    def calculateScore(self):
        correctString = self.testName.correctString
        patientString = self.patientAnswerString
        correctLength = len(correctString)
        patientLength = len(patientString)
        num_correct = 0
        for i in range(min(patientLength, correctLength)):
            if correctString[i] == patientString[i]:
                num_correct += 1
        self.score = num_correct / correctLength
        self.save()

    def calculateScoreUnordered(self):
        correctString = self.testName.correctString
        patientString = self.patientAnswerString
        patientLength = len(patientString)
        correctLength = len(correctString)
        num_correct = 0
        for i in range(min(patientLength, correctLength)):
            character = patientString[i]
            if character in correctString:
                num_correct += 1
                correctString = correctString.replace(character,'',1)
        return num_correct / correctLength
    
    def calculateScorePerChar(self):
        correctString = self.testName.correctString
        patientString = self.patientAnswerString
        patientLength = len(patientString)
        correctLength = len(correctString)
        correctChar = []
        for i in range(min(patientLength, correctLength)):
            if correctString[i] == patientString[i]:
                correctChar.append(1)
            else:
                correctChar.append(0)
        correctCharLength = len(correctChar)
        if correctCharLength != correctLength:
            for i in range(correctLength-correctCharLength):
                correctChar.append(0)
        return correctChar

    # Calculate the duration for the single span test
    def calculateDuration(self):
        duration = self.endingDayAndTime - self.startingDayAndTime
        if duration == 0:
            duration = None
        self.duration = duration.total_seconds()
        self.save()

    def __str__(self):
        return f"{self.testName} - Score: {self.score} - Duration: {self.duration}"

# Model for the latency table
class latency(models.Model):
    indResTable = models.ForeignKey(
        individualResultTable, on_delete=models.CASCADE, blank=True, null=True)
    latency1 = models.FloatField(null=True)
    latency2 = models.FloatField(null=True)
    latency3 = models.FloatField(null=True)
    latency4 = models.FloatField(null=True)
    latency5 = models.FloatField(null=True)

    # Calculate the duration of the span test
    def getDurationOfTest(self):
        latencies = [self.latency1, self.latency2, self.latency3, self.latency4, self.latency5]
        duration = 0
        for latency in latencies:
            if latency is not None:
                duration += latency
        if duration == 0:
            duration = None
        return duration

    def __str__(self):
        return f"{self.latency1}, {self.latency2}, {self.latency3}, {self.latency4}, {self.latency5}"


@receiver(post_migrate)
def create_default_stimuli(sender, **kwargs):
    default_stimuli = [
        {'name': 'Practice Digit 4 span', 'givenString': '5386', 'correctString': '3568'},
        {'name': 'Practice Digit 5 span', 'givenString': '94853', 'correctString': '34589'},
        {'name': 'First digit 4 span', 'givenString': '3254', 'correctString': '2345'},
        {'name': 'Second digit 4 span', 'givenString': '6584', 'correctString': '4568'},
        {'name': 'Third digit 4 span', 'givenString': '9324', 'correctString': '2349'},
        {'name': 'First digit 5 span', 'givenString': '65438', 'correctString': '34568'},
        {'name': 'Second digit 5 span', 'givenString': '87962', 'correctString': '26789'},
        {'name': 'Third digit 5 span', 'givenString': '53849', 'correctString': '34589'},
        {'name': 'Practice mixed 4 span', 'givenString': '7K3F', 'correctString': '37FK'},
        {'name': 'Practice mixed 5 span', 'givenString': 'R3JU7', 'correctString': '37JRU'},
        {'name': 'First mixed 4 span', 'givenString': '5WK4', 'correctString': '45KW'},
        {'name': 'Second mixed 4 span', 'givenString': 'R4W7', 'correctString': '47RW'},
        {'name': 'Third mixed 4 span', 'givenString': 'S8F4', 'correctString': '48FS'},
        {'name': 'First mixed 5 span', 'givenString': 'Y54JR', 'correctString': '45JRY'},
        {'name': 'Second mixed 5 span', 'givenString': '6UYR4', 'correctString': '46RUY'},
        {'name': 'Third mixed 5 span', 'givenString': 'WS84K', 'correctString': '48KSW'},
    ]

    for stimulus in default_stimuli:
        stimuli.objects.get_or_create(name=stimulus['name'], givenString=stimulus['givenString'], correctString=stimulus['correctString'])


@receiver(post_migrate)
def create_default_aggregated_data(sender, **kwargs):
    default_aggregated_data = [
        {'minAge': 0, 'maxAge': 12},
        {'minAge': 13, 'maxAge': 17},
        {'minAge': 18, 'maxAge': 39},
        {'minAge': 40, 'maxAge': 64},
        {'minAge': 65, 'maxAge': 79},
        {'minAge': 80, 'maxAge': sys.maxsize},
    ]

    for aggregated_data in default_aggregated_data:
        aggregateDataTable.objects.get_or_create(minAge=aggregated_data['minAge'], maxAge=aggregated_data['maxAge'])

def getOrderedStimuli():
    orderedStimulus = [
        stimuli.objects.get(name='Practice Digit 4 span'),
        stimuli.objects.get(name='Practice Digit 5 span'),
        stimuli.objects.get(name='First digit 4 span'),
        stimuli.objects.get(name='Second digit 4 span'),
        stimuli.objects.get(name='Third digit 4 span'),
        stimuli.objects.get(name='First digit 5 span'),
        stimuli.objects.get(name='Second digit 5 span'),
        stimuli.objects.get(name='Third digit 5 span'), 
        stimuli.objects.get(name='Practice mixed 4 span'),
        stimuli.objects.get(name='Practice mixed 5 span'),
        stimuli.objects.get(name='First mixed 4 span'),
        stimuli.objects.get(name='Second mixed 4 span'),
        stimuli.objects.get(name='Third mixed 4 span'),
        stimuli.objects.get(name='First mixed 5 span'),
        stimuli.objects.get(name='Second mixed 5 span'),
        stimuli.objects.get(name='Third mixed 5 span'),
    ]
    return orderedStimulus


def aggregateData():
    all_aggregate_data = aggregateDataTable.objects.all()
    for aggregated_data_row in all_aggregate_data:
        tests = individualTable.objects.filter(age__gt=aggregated_data_row.minAge-1, age__lt=aggregated_data_row.maxAge+1, completed=individualTable.completedStatus.COMPLETED)
        aggregated_data_row.numTests = tests.count()
        aggregated_data = tests.aggregate(
            avg_lat1=Avg('avgLatency1'),
            sd_lat1=StdDev('avgLatency1'),
            avg_lat2=Avg('avgLatency2'),
            sd_lat2=StdDev('avgLatency2'),
            avg_lat3=Avg('avgLatency3'),
            sd_lat3=StdDev('avgLatency3'),
            avg_lat4=Avg('avgLatency4'),
            sd_lat4=StdDev('avgLatency4'),
            avg_lat5=Avg('avgLatency5'),
            sd_lat5=StdDev('avgLatency5'),
            avg_duration=Avg('avgDuration'),
            sd_duration=StdDev('avgDuration'),
            avg_4SpanScore=Avg('avg4SpanScore'),
            sd_4SpanScore=StdDev('avg4SpanScore'),
            avg_5SpanScore=Avg('avg5SpanScore'),
            sd_5SpanScore=StdDev('avg5SpanScore'),
            avg_ScoreDigit=Avg('avgScoreDigit'),
            sd_ScoreDigit=StdDev('avgScoreDigit'),
            avg_ScoreMixed=Avg('avgScoreMixed'),
            sd_ScoreMixed=StdDev('avgScoreMixed'),
            avg_Score=Avg('avgScore'),
            sd_Score=StdDev('avgScore')
        )
        aggregated_data_row.avgLatency1 = aggregated_data['avg_lat1'] or 0
        aggregated_data_row.sdLatency1 = aggregated_data['sd_lat1'] or 0
        aggregated_data_row.avgLatency2 = aggregated_data['avg_lat2'] or 0
        aggregated_data_row.sdLatency2 = aggregated_data['sd_lat2'] or 0
        aggregated_data_row.avgLatency3 = aggregated_data['avg_lat3'] or 0
        aggregated_data_row.sdLatency3 = aggregated_data['sd_lat3'] or 0
        aggregated_data_row.avgLatency4 = aggregated_data['avg_lat4'] or 0
        aggregated_data_row.sdLatency4 = aggregated_data['sd_lat4'] or 0
        aggregated_data_row.avgLatency5 = aggregated_data['avg_lat5'] or 0
        aggregated_data_row.sdLatency5 = aggregated_data['sd_lat5'] or 0
        aggregated_data_row.avgDuration = aggregated_data['avg_duration'] or 0
        aggregated_data_row.sdDuration = aggregated_data['sd_duration'] or 0
        aggregated_data_row.avg4SpanScore = aggregated_data['avg_4SpanScore'] or 0
        aggregated_data_row.sd4SpanScore = aggregated_data['sd_4SpanScore'] or 0
        aggregated_data_row.avg5SpanScore = aggregated_data['avg_5SpanScore'] or 0
        aggregated_data_row.sd5SpanScore = aggregated_data['sd_5SpanScore'] or 0
        aggregated_data_row.avgScoreDigit = aggregated_data['avg_ScoreDigit'] or 0
        aggregated_data_row.sdScoreDigit = aggregated_data['sd_ScoreDigit'] or 0
        aggregated_data_row.avgScoreMixed = aggregated_data['avg_ScoreMixed'] or 0
        aggregated_data_row.sdScoreMixed = aggregated_data['sd_ScoreMixed'] or 0
        aggregated_data_row.avgScore = aggregated_data['avg_Score'] or 0
        aggregated_data_row.sdScore = aggregated_data['sd_Score'] or 0

        dataFields = ["4SpanDigitScore", "4SpanMixedScore", "5SpanDigitScore", "5SpanMixedScore", "4SpanScoreUnordered", "5SpanScoreUnordered",
                     "ScoreDigitUnordered", "ScoreMixedUnordered", "ScoreUnordered", "4SpanDigitScoreUnordered", "4SpanMixedScoreUnordered", 
                     "5SpanDigitScoreUnordered", "5SpanMixedScoreUnordered", "ScoreStim1", "ScoreStim2", "ScoreStim3", "ScoreStim4", 
                     "ScoreStim5", "DurationWholeTest"]
        extraData = {"4SpanDigitScore":[], "4SpanMixedScore":[], "5SpanDigitScore":[], "5SpanMixedScore":[], "4SpanScoreUnordered":[], "5SpanScoreUnordered":[],
                     "ScoreDigitUnordered":[], "ScoreMixedUnordered":[], "ScoreUnordered":[], "4SpanDigitScoreUnordered":[], "4SpanMixedScoreUnordered":[], 
                     "5SpanDigitScoreUnordered":[], "5SpanMixedScoreUnordered":[], "ScoreStim1":[], "ScoreStim2":[], "ScoreStim3":[], "ScoreStim4":[], 
                     "ScoreStim5":[], "DurationWholeTest":[]}
        for test in tests:
            indTableData = test.calculateExtraData()
            for dataField in dataFields:
                extraData[dataField].append(indTableData[dataField])
        avgExtraData = {}
        sdExtraData = {}
        for dataField in dataFields:
            avgExtraData[dataField] = calculateAvg(extraData[dataField])
            sdExtraData[dataField] = calculateSd(extraData[dataField],avgExtraData[dataField])
        aggregated_data_row.avg4SpanDigitScore = avgExtraData["4SpanDigitScore"]
        aggregated_data_row.sd4SpanDigitScore = sdExtraData["4SpanDigitScore"]
        aggregated_data_row.avg4SpanMixedScore = avgExtraData["4SpanMixedScore"]
        aggregated_data_row.sd4SpanMixedScore = sdExtraData["4SpanMixedScore"]
        aggregated_data_row.avg5SpanDigitScore = avgExtraData["5SpanDigitScore"]
        aggregated_data_row.sd5SpanDigitScore = sdExtraData["5SpanDigitScore"]
        aggregated_data_row.avg5SpanMixedScore = avgExtraData["5SpanMixedScore"]
        aggregated_data_row.sd5SpanMixedScore = sdExtraData["5SpanMixedScore"]
        aggregated_data_row.avg4SpanScoreUnordered = avgExtraData["4SpanScoreUnordered"]
        aggregated_data_row.sd4SpanScoreUnordered = sdExtraData["4SpanScoreUnordered"]
        aggregated_data_row.avg5SpanScoreUnordered = avgExtraData["5SpanScoreUnordered"]
        aggregated_data_row.sd5SpanScoreUnordered = sdExtraData["5SpanScoreUnordered"]
        aggregated_data_row.avgScoreDigitUnordered = avgExtraData["ScoreDigitUnordered"]
        aggregated_data_row.sdScoreDigitUnordered = sdExtraData["ScoreDigitUnordered"]
        aggregated_data_row.avgScoreMixedUnordered = avgExtraData["ScoreMixedUnordered"]
        aggregated_data_row.sdScoreMixedUnordered = sdExtraData["ScoreMixedUnordered"]
        aggregated_data_row.avgScoreUnordered = avgExtraData["ScoreUnordered"]
        aggregated_data_row.sdScoreUnordered = sdExtraData["ScoreUnordered"]
        aggregated_data_row.avg4SpanDigitScoreUnordered = avgExtraData["4SpanDigitScoreUnordered"]
        aggregated_data_row.sd4SpanDigitScoreUnordered = sdExtraData["4SpanDigitScoreUnordered"]
        aggregated_data_row.avg4SpanMixedScoreUnordered = avgExtraData["4SpanMixedScoreUnordered"]
        aggregated_data_row.sd4SpanMixedScoreUnordered = sdExtraData["4SpanMixedScoreUnordered"]
        aggregated_data_row.avg5SpanDigitScoreUnordered = avgExtraData["5SpanDigitScoreUnordered"]
        aggregated_data_row.sd5SpanDigitScoreUnordered = sdExtraData["5SpanDigitScoreUnordered"]
        aggregated_data_row.avg5SpanMixedScoreUnordered = avgExtraData["5SpanMixedScoreUnordered"]
        aggregated_data_row.sd5SpanMixedScoreUnordered = sdExtraData["5SpanMixedScoreUnordered"]
        aggregated_data_row.avgScoreStim1 = avgExtraData["ScoreStim1"]
        aggregated_data_row.sdScoreStim1 = sdExtraData["ScoreStim1"]
        aggregated_data_row.avgScoreStim2 = avgExtraData["ScoreStim2"]
        aggregated_data_row.sdScoreStim2 = sdExtraData["ScoreStim2"]
        aggregated_data_row.avgScoreStim3 = avgExtraData["ScoreStim3"]
        aggregated_data_row.sdScoreStim3 = sdExtraData["ScoreStim3"]
        aggregated_data_row.avgScoreStim4 = avgExtraData["ScoreStim4"]
        aggregated_data_row.sdScoreStim4 = sdExtraData["ScoreStim4"]
        aggregated_data_row.avgScoreStim5 = avgExtraData["ScoreStim5"]
        aggregated_data_row.sdScoreStim5 = sdExtraData["ScoreStim5"]
        aggregated_data_row.avgDurationWholeTest = avgExtraData["DurationWholeTest"]
        aggregated_data_row.sdDurationWholeTest = sdExtraData["DurationWholeTest"]

        aggregated_data_row.save()


def getAggregateDataForAgeSummary(age):
    aggregateData =  aggregateDataTable.objects.get(minAge__lte=age, maxAge__gte=age)
    aggregateDictionary = {
        'minAge': aggregateData.minAge,
        'maxAge': aggregateData.maxAge,
        'numTests': aggregateData.numTests,
        'avgLatency1': aggregateData.avgLatency1,
        'sdLatency1': aggregateData.sdLatency1,
        'avgLatency2': aggregateData.avgLatency2,
        'sdLatency2': aggregateData.sdLatency2,
        'avgLatency3': aggregateData.avgLatency3,
        'sdLatency3': aggregateData.sdLatency3,
        'avgLatency4': aggregateData.avgLatency4,
        'sdLatency4': aggregateData.sdLatency4,
        'avgLatency5': aggregateData.avgLatency5,
        'sdLatency5': aggregateData.sdLatency5,
        'avgDuration': aggregateData.avgDuration,
        'sdDuration': aggregateData.sdDuration,
        'avg4SpanScore': aggregateData.avg4SpanScore,
        'sd4SpanScore': aggregateData.sd4SpanScore,
        'avg5SpanScore': aggregateData.avg5SpanScore,
        'sd5SpanScore': aggregateData.sd5SpanScore,
        'avgScoreDigit': aggregateData.avgScoreDigit,
        'sdScoreDigit': aggregateData.sdScoreDigit,
        'avgScoreMixed': aggregateData.avgScoreMixed,
        'sdScoreMixed': aggregateData.sdScoreMixed,
        'avgScore': aggregateData.avgScore,
        'sdScore': aggregateData.sdScore
    }
    return aggregateDictionary

def getAggregateDataForAgeComplete(age):
    aggregateData =  aggregateDataTable.objects.get(minAge__lte=age, maxAge__gte=age)
    aggregateDictionary = {
        'minAge': aggregateData.minAge,
        'maxAge': aggregateData.maxAge,
        'numTests': aggregateData.numTests,
        'avgLatency1': aggregateData.avgLatency1,
        'sdLatency1': aggregateData.sdLatency1,
        'avgLatency2': aggregateData.avgLatency2,
        'sdLatency2': aggregateData.sdLatency2,
        'avgLatency3': aggregateData.avgLatency3,
        'sdLatency3': aggregateData.sdLatency3,
        'avgLatency4': aggregateData.avgLatency4,
        'sdLatency4': aggregateData.sdLatency4,
        'avgLatency5': aggregateData.avgLatency5,
        'sdLatency5': aggregateData.sdLatency5,
        'avgDuration': aggregateData.avgDuration,
        'sdDuration': aggregateData.sdDuration,
        'avg4SpanScore': aggregateData.avg4SpanScore,
        'sd4SpanScore': aggregateData.sd4SpanScore,
        'avg5SpanScore': aggregateData.avg5SpanScore,
        'sd5SpanScore': aggregateData.sd5SpanScore,
        'avgScoreDigit': aggregateData.avgScoreDigit,
        'sdScoreDigit': aggregateData.sdScoreDigit,
        'avgScoreMixed': aggregateData.avgScoreMixed,
        'sdScoreMixed': aggregateData.sdScoreMixed,
        'avgScore': aggregateData.avgScore,
        'sdScore': aggregateData.sdScore,
        'avg4SpanDigitScore': aggregateData.avg4SpanDigitScore,
        'sd4SpanDigitScore': aggregateData.sd4SpanDigitScore,
        'avg4SpanMixedScore': aggregateData.avg4SpanMixedScore,
        'sd4SpanMixedScore': aggregateData.sd4SpanMixedScore,
        'avg5SpanDigitScore': aggregateData.avg5SpanDigitScore,
        'sd5SpanDigitScore': aggregateData.sd5SpanDigitScore,
        'avg5SpanMixedScore': aggregateData.avg5SpanMixedScore,
        'sd5SpanMixedScore': aggregateData.sd5SpanMixedScore,
        'avg4SpanScoreUnordered': aggregateData.avg4SpanScoreUnordered,
        'sd4SpanScoreUnordered': aggregateData.sd4SpanScoreUnordered,
        'avg5SpanScoreUnordered': aggregateData.avg5SpanScoreUnordered,
        'sd5SpanScoreUnordered': aggregateData.sd5SpanScoreUnordered,
        'avgScoreDigitUnordered': aggregateData.avgScoreDigitUnordered,
        'sdScoreDigitUnordered': aggregateData.sdScoreDigitUnordered,
        'avgScoreMixedUnordered': aggregateData.avgScoreMixedUnordered,
        'sdScoreMixedUnordered': aggregateData.sdScoreMixedUnordered,
        'avgScoreUnordered': aggregateData.avgScoreUnordered,
        'sdScoreUnordered': aggregateData.sdScoreUnordered,
        'avg4SpanDigitScoreUnordered': aggregateData.avg4SpanDigitScoreUnordered,
        'sd4SpanDigitScoreUnordered': aggregateData.sd4SpanDigitScoreUnordered,
        'avg4SpanMixedScoreUnordered': aggregateData.avg4SpanMixedScoreUnordered,
        'sd4SpanMixedScoreUnordered': aggregateData.sd4SpanMixedScoreUnordered,
        'avg5SpanDigitScoreUnordered': aggregateData.avg5SpanDigitScoreUnordered,
        'sd5SpanDigitScoreUnordered': aggregateData.sd5SpanDigitScoreUnordered,
        'avg5SpanMixedScoreUnordered': aggregateData.avg5SpanMixedScoreUnordered,
        'sd5SpanMixedScoreUnordered': aggregateData.sd5SpanMixedScoreUnordered,
        'avgScoreStim1': aggregateData.avgScoreStim1,
        'sdScoreStim1': aggregateData.sdScoreStim1,
        'avgScoreStim2': aggregateData.avgScoreStim2,
        'sdScoreStim2': aggregateData.sdScoreStim2,
        'avgScoreStim3': aggregateData.avgScoreStim3,
        'sdScoreStim3': aggregateData.sdScoreStim3,
        'avgScoreStim4': aggregateData.avgScoreStim4,
        'sdScoreStim4': aggregateData.sdScoreStim4,
        'avgScoreStim5': aggregateData.avgScoreStim5,
        'sdScoreStim5': aggregateData.sdScoreStim5,
        'avgDurationWholeTest': aggregateData.avgDurationWholeTest,
        'sdDurationWholeTest': aggregateData.sdDurationWholeTest
    }
    return aggregateDictionary

def getFieldPercentile(field, patient_data_point, age):
    zScore = calculateZScore(field, patient_data_point, age)
    return stats.norm.cdf(zScore)*100

def calculateZScore(field, patient_data_point, age):
    avg, sd = getAggregateField(field, age)
    return (patient_data_point - avg) / sd

def getAllPercentiles(patient_data_points, age):
    percentileDictionary = {
        'Latency1': getFieldPercentile('Latency1', patient_data_points['avgLatency1'], age),
        'Latency2': getFieldPercentile('Latency2', patient_data_points['avgLatency2'], age),
        'Latency3': getFieldPercentile('Latency3', patient_data_points['avgLatency3'], age),
        'Latency4': getFieldPercentile('Latency4', patient_data_points['avgLatency4'], age),
        'Latency5': getFieldPercentile('Latency5', patient_data_points['avgLatency5'], age),
        'Duration': getFieldPercentile('Duration', patient_data_points['avgDuration'], age),
        '4SpanScore': getFieldPercentile('4SpanScore', patient_data_points['avg4SpanScore'], age),
        '5SpanScore': getFieldPercentile('5SpanScore', patient_data_points['avg5SpanScore'], age),
        'ScoreDigit': getFieldPercentile('ScoreDigit', patient_data_points['avgScoreDigit'], age),
        'ScoreMixed': getFieldPercentile('ScoreMixed', patient_data_points['avgScoreMixed'], age),
        'Score': getFieldPercentile('Score', patient_data_points['avgScore'], age),
        '4SpanDigitScore': getFieldPercentile('4SpanDigitScore', patient_data_points['avg4SpanDigitScore'], age),
        '4SpanMixedScore': getFieldPercentile('4SpanMixedScore', patient_data_points['avg4SpanMixedScore'], age),
        '5SpanDigitScore': getFieldPercentile('5SpanDigitScore', patient_data_points['avg5SpanDigitScore'], age),
        '5SpanMixedScore': getFieldPercentile('5SpanMixedScore', patient_data_points['avg5SpanMixedScore'], age),
        '4SpanScoreUnordered': getFieldPercentile('4SpanScoreUnordered', patient_data_points['avg4SpanScoreUnordered'], age),
        '5SpanScoreUnordered': getFieldPercentile('5SpanScoreUnordered', patient_data_points['avg5SpanScoreUnordered'], age),
        'ScoreDigitUnordered': getFieldPercentile('ScoreDigitUnordered', patient_data_points['avgScoreDigitUnordered'], age),
        'ScoreMixedUnordered': getFieldPercentile('ScoreMixedUnordered', patient_data_points['avgScoreMixedUnordered'], age),
        'ScoreUnordered': getFieldPercentile('ScoreUnordered', patient_data_points['avgScoreUnordered'], age),
        '4SpanDigitScoreUnordered': getFieldPercentile('4SpanDigitScoreUnordered', patient_data_points['avg4SpanDigitScoreUnordered'], age),
        '4SpanMixedScoreUnordered': getFieldPercentile('4SpanMixedScoreUnordered', patient_data_points['avg4SpanMixedScoreUnordered'], age),
        '5SpanDigitScoreUnordered': getFieldPercentile('5SpanDigitScoreUnordered', patient_data_points['avg5SpanDigitScoreUnordered'], age),
        '5SpanMixedScoreUnordered': getFieldPercentile('5SpanMixedScoreUnordered', patient_data_points['avg5SpanMixedScoreUnordered'], age),
        'ScoreStim1': getFieldPercentile('ScoreStim1', patient_data_points['avgScoreStim1'], age),
        'ScoreStim2': getFieldPercentile('ScoreStim2', patient_data_points['avgScoreStim2'], age),
        'ScoreStim3': getFieldPercentile('ScoreStim3', patient_data_points['avgScoreStim3'], age),
        'ScoreStim4': getFieldPercentile('ScoreStim4', patient_data_points['avgScoreStim4'], age),
        'ScoreStim5': getFieldPercentile('ScoreStim5', patient_data_points['avgScoreStim5'], age),
        'DurationWholeTest': getFieldPercentile('DurationWholeTest', patient_data_points['avgDurationWholeTest'], age)
    }
    return percentileDictionary

def getAllZScore(patient_data_points, age):
    zScoreDictionary = {
        'Latency1': calculateZScore('Latency1', patient_data_points['avgLatency1'], age),
        'Latency2': calculateZScore('Latency2', patient_data_points['avgLatency2'], age),
        'Latency3': calculateZScore('Latency3', patient_data_points['avgLatency3'], age),
        'Latency4': calculateZScore('Latency4', patient_data_points['avgLatency4'], age),
        'Latency5': calculateZScore('Latency5', patient_data_points['avgLatency5'], age),
        'Duration': calculateZScore('Duration', patient_data_points['avgDuration'], age),
        '4SpanScore': calculateZScore('4SpanScore', patient_data_points['avg4SpanScore'], age),
        '5SpanScore': calculateZScore('5SpanScore', patient_data_points['avg5SpanScore'], age),
        'ScoreDigit': calculateZScore('ScoreDigit', patient_data_points['avgScoreDigit'], age),
        'ScoreMixed': calculateZScore('ScoreMixed', patient_data_points['avgScoreMixed'], age),
        'Score': calculateZScore('Score', patient_data_points['avgScore'], age),
        '4SpanDigitScore': calculateZScore('4SpanDigitScore', patient_data_points['4SpanDigitScore'], age),
        '4SpanMixedScore': calculateZScore('4SpanMixedScore', patient_data_points['4SpanMixedScore'], age),
        '5SpanDigitScore': calculateZScore('5SpanDigitScore', patient_data_points['5SpanDigitScore'], age),
        '5SpanMixedScore': calculateZScore('5SpanMixedScore', patient_data_points['5SpanMixedScore'], age),
        '4SpanScoreUnordered': calculateZScore('4SpanScoreUnordered', patient_data_points['4SpanScoreUnordered'], age),
        '5SpanScoreUnordered': calculateZScore('5SpanScoreUnordered', patient_data_points['5SpanScoreUnordered'], age),
        'ScoreDigitUnordered': calculateZScore('ScoreDigitUnordered', patient_data_points['ScoreDigitUnordered'], age),
        'ScoreMixedUnordered': calculateZScore('ScoreMixedUnordered', patient_data_points['ScoreMixedUnordered'], age),
        'ScoreUnordered': calculateZScore('ScoreUnordered', patient_data_points['ScoreUnordered'], age),
        '4SpanDigitScoreUnordered': calculateZScore('4SpanDigitScoreUnordered', patient_data_points['4SpanDigitScoreUnordered'], age),
        '4SpanMixedScoreUnordered': calculateZScore('4SpanMixedScoreUnordered', patient_data_points['4SpanMixedScoreUnordered'], age),
        '5SpanDigitScoreUnordered': calculateZScore('5SpanDigitScoreUnordered', patient_data_points['5SpanDigitScoreUnordered'], age),
        '5SpanMixedScoreUnordered': calculateZScore('5SpanMixedScoreUnordered', patient_data_points['5SpanMixedScoreUnordered'], age),
        'ScoreStim1': calculateZScore('ScoreStim1', patient_data_points['ScoreStim1'], age),
        'ScoreStim2': calculateZScore('ScoreStim2', patient_data_points['ScoreStim2'], age),
        'ScoreStim3': calculateZScore('ScoreStim3', patient_data_points['ScoreStim3'], age),
        'ScoreStim4': calculateZScore('ScoreStim4', patient_data_points['ScoreStim4'], age),
        'ScoreStim5': calculateZScore('ScoreStim5', patient_data_points['ScoreStim5'], age),
        'DurationWholeTest': calculateZScore('DurationWholeTest', patient_data_points['DurationWholeTest'], age)
    }
    return zScoreDictionary

def getAggregateField(field, age):
    aggregateData = aggregateDataTable.objects.get(minAge__lte=age, maxAge__gte=age)
    match field:
        case 'minAge':
            return aggregateData.minAge
        case 'maxAge':
            return aggregateData.maxAge
        case 'numTests':
            return aggregateData.numTests
        case 'Latency1':
            return aggregateData.avgLatency1, aggregateData.sdLatency1
        case 'Latency2':
            return aggregateData.avgLatency2, aggregateData.sdLatency2
        case 'Latency3':
            return aggregateData.avgLatency3, aggregateData.sdLatency3
        case 'Latency4':
            return aggregateData.avgLatency4, aggregateData.sdLatency4
        case 'Latency5':
            return aggregateData.avgLatency5, aggregateData.sdLatency2
        case 'Duration':
            return aggregateData.avgDuration, aggregateData.sdDuration
        case '4SpanScore':
            return aggregateData.avg4SpanScore, aggregateData.sd4SpanScore
        case '5SpanScore':
            return aggregateData.avg5SpanScore, aggregateData.sd5SpanScore
        case 'ScoreDigit':
            return aggregateData.avgScoreDigit, aggregateData.sdScoreDigit
        case 'ScoreMixed':
            return aggregateData.avgScoreMixed, aggregateData.sdScoreMixed
        case 'Score':
            return aggregateData.avgScore, aggregateData.sdScore
        case '4SpanDigitScore':
            return aggregateData.avg4SpanDigitScore, aggregateData.sd4SpanDigitScore
        case '4SpanMixedScore':
            return aggregateData.avg4SpanMixedScore, aggregateData.sd4SpanMixedScore
        case '5SpanDigitScore':
            return aggregateData.avg5SpanDigitScore, aggregateData.sd5SpanDigitScore
        case '5SpanMixedScore':
            return aggregateData.avg5SpanMixedScore, aggregateData.sd5SpanMixedScore
        case '4SpanScoreUnordered':
            return aggregateData.avg4SpanScoreUnordered, aggregateData.sd4SpanScoreUnordered
        case '5SpanScoreUnordered':
            return aggregateData.avg5SpanScoreUnordered, aggregateData.sd5SpanScoreUnordered
        case 'ScoreDigitUnordered':
            return aggregateData.avgScoreDigitUnordered, aggregateData.sdScoreDigitUnordered
        case 'ScoreMixedUnordered':
            return aggregateData.avgScoreMixedUnordered, aggregateData.sdScoreMixedUnordered
        case 'ScoreUnordered':
            return aggregateData.avgScoreUnordered, aggregateData.sdScoreUnordered
        case '4SpanDigitScoreUnordered':
            return aggregateData.avg4SpanDigitScoreUnordered, aggregateData.sd4SpanDigitScoreUnordered
        case '4SpanMixedScoreUnordered':
            return aggregateData.avg4SpanMixedScoreUnordered, aggregateData.sd4SpanMixedScoreUnordered
        case '5SpanDigitScoreUnordered':
            return aggregateData.avg5SpanDigitScoreUnordered, aggregateData.sd5SpanDigitScoreUnordered
        case '5SpanMixedScoreUnordered':
            return aggregateData.avg5SpanMixedScoreUnordered, aggregateData.sd5SpanMixedScoreUnordered
        case 'ScoreStim1':
            return aggregateData.avgScoreStim1, aggregateData.sdScoreStim1
        case 'ScoreStim2':
            return aggregateData.avgScoreStim2, aggregateData.sdScoreStim2
        case 'ScoreStim3':
            return aggregateData.avgScoreStim3, aggregateData.sdScoreStim3
        case 'ScoreStim4':
            return aggregateData.avgScoreStim4, aggregateData.sdScoreStim4
        case 'ScoreStim5':
            return aggregateData.avgScoreStim5, aggregateData.sdScoreStim5
        case 'DurationWholeTest':
            return aggregateData.avgDurationWholeTest, aggregateData.sdDurationWholeTest
    
def calculateAvg(data):
    sum = 0
    count = 0
    for value in data:
        if value is not None:
            sum += value
            count += 1
    return sum / count

def calculateSd(data, avg):
    sum = 0
    count = 0
    for value in data:
        if value is not None:
            sum += (value-avg)**2
            count += 1
    return (sum/count)**.5
    
