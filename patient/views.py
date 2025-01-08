from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from model.models import *
from model import models
from django.core.cache import cache
import json

#local variables
testResults = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# function to grab stimuli
def getStimuli():
    stimuliJSON = cache.get('stimuliJSON')
    if not stimuliJSON:
        stimulus_queryset = getOrderedStimuli()
        stimuli = [{'givenString': list(stim.givenString)} for stim in stimulus_queryset]
        stimuliJSON = json.dumps(stimuli)
        cache.set('stimuliJSON', stimuliJSON, timeout=3600)  # Cache for 1 hour

    return stimuliJSON
@require_GET
def stimuli(request):
    stimuliJSON = getStimuli()

    return render(request, "patient/stimuli.html", {"stimuliJSON": stimuliJSON})


# Welcome screen
@require_GET
def welcome(request, value):
    global linkID 
    linkID = int(value)
    link = doctorLink.objects.get(linkID=f"{linkID:05}")
    try:
        print("Attempting to fetch individual record")
        individual = individualTable.objects.get(linkID=link)

        if (individual.completed == individualTable.completedStatus.QUIT):
            print("Test Invalid")
            return render (request, "patient/isInvalid.html",)
        elif (individual.completed == individualTable.completedStatus.COMPLETED):
            print("Test Completed")
            return render(request, "patient/completed.html",)
        else:
            print("Test Valid")
            return render(request, "patient/welcome.html",)
    except individualTable.DoesNotExist:
        print("Record not found with the provided linkID") 
        return render(request, "patient/isInvalid.html",)

@require_GET
def isInvalid(request):
    return render(request, "patient/isInvalid.html",)

@require_GET
def digitIntro(request):
    return render(request, "patient/digitIntro.html",)


@require_GET
def digitKeyboard(request):
    return render(request, "patient/digitKeyboard.html",)


@require_GET
def mixedIntro(request):
    return render(request, "patient/mixedIntro.html",)


@require_GET
def mixedKeyboard(request):
    return render(request, "patient/mixedKeyboard.html",)


@require_GET
def mixedStimuli(request):
    return render(request, "patient/mixedStimuli.html",)




def response(request):
    times = request.POST['times']
    currentSetIndex = request.POST['currentSetIndex']
    currentSetIndex = int(currentSetIndex) - 1
    responses = times.split(" ")
    previous = int(responses[0])
    first = int(responses[0])
    responses.pop(0)
    patientAnswerString = ""
    latencyList = []
    for response in responses:
        values = response.split(':')
        button = values[0]
        patientAnswerString = patientAnswerString + button
        latency = (int(values[1]) - previous)/1000
        latencyList.append(latency)
        previous = int(values[1])
    stimulus = getOrderedStimuli()
    testResults[currentSetIndex].append(stimulus[currentSetIndex])
    testResults[currentSetIndex].append(patientAnswerString)
    testResults[currentSetIndex].append(first)
    testResults[currentSetIndex].append(previous)
    testResults[currentSetIndex].append(latencyList)
    if currentSetIndex == 15:
        link = doctorLink.objects.get(linkID=f"{linkID:05}")
        indTable = models.individualTable.objects.get(linkID=link)
        for i in range(16):
            print(testResults[i])
            indResTable = models.individualResultTable.objects.create(
                indTable = indTable,
                testName=stimulus[i],
                patientAnswerString=str(testResults[i][1]),
                startingDayAndTime=datetime.datetime.fromtimestamp(testResults[i][2] / 1000),
                endingDayAndTime=datetime.datetime.fromtimestamp(testResults[i][3] / 1000)
            )
            if len(testResults[i][4]) <= 4:
                latency_data = {}
                for j in range(len(testResults[i][4])):
                    latency_data[f'latency{j+1}'] = testResults[i][4][j]
                models.latency.objects.create(indResTable=indResTable, **latency_data)
            elif len(testResults[i][4]) >= 5:
                models.latency.objects.create(
                    indResTable=indResTable, latency1=testResults[i][4][0], latency2=testResults[i][4][1], latency3=testResults[i][4][2], latency4=testResults[i][4][3], latency5=testResults[i][4][4])
            indResTable.calculateScore()
            indResTable.calculateDuration()
        indTable.calculateData()

    return render(request, "patient/stimuli.html")

def isQuit(request):
    print("isQuit called")
    print("link id: " + str(f"{linkID:05}"))
    
    if request.method == "POST":
        try:
            print("Attempting to fetch individual record")
            link = doctorLink.objects.get(linkID=f"{linkID:05}")
            individual = individualTable.objects.get(linkID=link)
            individual.completed = individualTable.completedStatus.QUIT
            individual.save()
            print("Status updated to QUIT")
            return JsonResponse({"message": "Status updated to QUIT"})
        except individualTable.DoesNotExist:
            print("Record not found with the provided linkID") 
            return JsonResponse({"message": "Record not found"})
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({"message": "An error occurred"})
    else:
        print("Received a non-POST request to isQuit view")
        return JsonResponse({"message": "Invalid request"})

def conclusion(request):
    return render(request, "patient/conclusion.html")


def practiceFinish(request):
    return render(request, "patient/practiceFinish.html")
