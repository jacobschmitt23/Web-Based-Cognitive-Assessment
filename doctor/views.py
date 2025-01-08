from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from model.models import *
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.contrib.auth.models import User
import numpy
import io
import matplotlib.pyplot
import mpld3
import base64
from .spreadsheet.ss import *
from scipy.stats import norm

matplotlib.use('AGG')

def convert_to_dict(instance):
    return {
        'avgLatency1': instance.avgLatency1,
        'avgLatency2': instance.avgLatency2,
        'avgLatency3': instance.avgLatency3,
        'avgLatency4': instance.avgLatency4,
        'avgLatency5': instance.avgLatency5,
        'avgDuration': instance.avgDuration,
        'avg4SpanScore': instance.avg4SpanScore,
        'avg5SpanScore': instance.avg5SpanScore,
        'avgScoreDigit': instance.avgScoreDigit,
        'avgScoreMixed': instance.avgScoreMixed,
        'avgScore': instance.avgScore,
    }
# Create your views here.

def login(request):
     if (request.method == 'GET'):
        return render(request, "doctor/login.html", {})
     else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            doctor = User.objects.filter(username=username).first()
            


            if request.POST.get("action") == "login":
                doctor = authenticate(username=username,password=password)
                if doctor is not None:
                    log_in(request, doctor)
                    return redirect('/doctor/manageTestLinks/')
                else:
                    return render(request, "doctor/login.html", {"error": "Invalid Credentials"})
            
            elif request.POST.get("action") == "signup":
                if doctor is None:
                    # Add doctor signup logic here
                    user = User.objects.create_user(username=username, password=password)
                    log_in(request, user)
                    return redirect('/doctor/manageTestLinks/')
                else:
                    return render(request, "doctor/login.html", {"error": "Invalid Credentials"})
    


def manageTestLinks(request):
    #list1 = ['one', 'two', 'three', 'four', 'five', 'oisdiwdiu'] # Sample list of links for testing
    #list2 = ['True', 'False', 'True', 'True', 'False', 'Invalid'] # Sample list for the status of the link. True means that the test has been completed, False for incomplete, a third option will exist but will be defined when the database is configured for that third option.
    #'Fal2se' is not a typo, it is for testing the third possible test state of "invalidated" or eqivalent.

    doctorToGet = request.user.username
    #Get the specific doctor's links
    user = User.objects.get(username = doctorToGet)
    linkQuery =  doctorLink.objects.filter(doctor = user.id)

    count = 0
    list1 = []
    list2 = []
    for link in linkQuery:
        #print(link.linkID, count)
        list1.append(link.linkID)
        count += 1
        individualTest = individualTable.objects.get(linkID = link)
        #print(individualTest.get_completed_display())
        if individualTest.get_completed_display() == 'Completed':
            list2.append('True')
        elif individualTest.get_completed_display() == 'Incomplete':
            list2.append('False')
        else:
            list2.append('Invalid')
    
    testsList = zip(list1, list2) #zip the lists together to be sent together

    if request.method == 'GET':
        return render(request, "doctor/manageTestLinks.html", {'list' : testsList, 'usersName' : doctorToGet})
    else:
        #trying to display a dynamic number of buttons on the page and assigning them different values that will be sent for different operations
        if 'delete' in request.POST:
            try:
                print(request.POST.get('delete'))
                print("Delete Triggered")
                linkToDelete = doctorLink.objects.get(linkID=request.POST.get('delete'))
                print(f"{bcolors.BOLD}{bcolors.WARNING}Deleting Object:", linkToDelete, f"{bcolors.ENDC}")
                linkToDelete.delete()
                print(f"{bcolors.BOLD}{bcolors.OKGREEN}Object Deleted Successfully", f"{bcolors.ENDC}")
                doctorToGet = request.user.username
                #Get the specific doctor's links
                user = User.objects.get(username = doctorToGet)
                linkQuery =  doctorLink.objects.filter(doctor = user.id)

                count = 0
                list1 = []
                list2 = []
                for link in linkQuery:
                #print(link.linkID, count)
                    list1.append(link.linkID)
                    count += 1
                    individualTest = individualTable.objects.get(linkID = link)
                #print(individualTest.get_completed_display())
                    if individualTest.get_completed_display() == 'Completed':
                        list2.append('True')
                    elif individualTest.get_completed_display() == 'Incomplete':
                        list2.append('False')
                    else:
                        list2.append('Invalid')
                testsList = zip(list1, list2) #zip the lists together to be sent together
                return render(request, "doctor/manageTestLinks.html", {'list' : testsList, 'usersName' : doctorToGet})
            except:
                print(f"{bcolors.FAIL}{bcolors.BOLD}!!!Failed to delete Object!!!{bcolors.ENDC}")
        elif 'download' in request.POST:
            print(request.POST.get('download'))
            print("Download Triggered")
            generateSpreadsheet(request.POST.get('download'))
            filePath = os.path.join(settings.BASE_DIR, 'temp/'+ request.POST.get('download') + '.xlsx') #Getting the path to the file.
            openedFile = open(filePath, 'rb')
            return FileResponse(openedFile)
            #generateSpreadsheet(request.POST.get('download'))
        elif 'view' in request.POST:
            print(request.POST.get('view'))
            print("View Triggered")
            #gottenTable = individualTable.objects.get(linkID=request.POST.get('view'))
            gottenTable = request.POST.get('view')
            #datapage(request, request.POST.get('view'))
            return redirect('doctor:datapage', gottenTable=gottenTable)
        elif 'generateLink' in request.POST:
            print("Generate Link Triggered")
            age = int(request.POST['age'])
            print(age)
            generatedLinkID = generateLink(age, user)
            
            doctorToGet = request.user.username
            #Get the specific doctor's links
            user = User.objects.get(username = doctorToGet)
            linkQuery =  doctorLink.objects.filter(doctor = user.id)

            count = 0
            list1 = []
            list2 = []
            for link in linkQuery:
                #print(link.linkID, count)
                list1.append(link.linkID)
                count += 1
                individualTest = individualTable.objects.get(linkID = link)
                #print(individualTest.get_completed_display())
                if individualTest.get_completed_display() == 'Completed':
                    list2.append('True')
                elif individualTest.get_completed_display() == 'Incomplete':
                    list2.append('False')
                else:
                    list2.append('Invalid')
    
            testsList = zip(list1, list2) #zip the lists together to be sent together

            return render(request, "doctor/manageTestLinks.html", {'list' : testsList, 'usersName' : doctorToGet, 'newLinkID' : generatedLinkID})
            #return HttpResponse(f"Generated Link: {generatedLinkID}") #respond with the input age for testing
        elif 'Logout' in request.POST:
            log_out(request)
            return HttpResponseRedirect("/doctor/login/")

        #Redirect page so that it will properly refresh 
        return HttpResponseRedirect("/doctor/manageTestLinks/")



def datapage(request, gottenTable):

    link = doctorLink.objects.get(linkID=gottenTable)
    variable = None
    if isinstance(gottenTable, str):
        tableToProcess = individualTable.objects.get(linkID=link)
    if request.method=="GET":
        aggregateTable = getAggregateDataForAgeSummary(tableToProcess.age)
        avg = aggregateTable['avgScore']
        sd = aggregateTable['sdScore']
        graph = generateGraph(avg,sd,tableToProcess,None)

    if request.method=="POST":
        tableToProcess = individualTable.objects.get(linkID=link)
        variable = request.POST.get('update', 'Score')
        avg,sd = getAggregateField(variable,tableToProcess.age)
        graph = generateGraph(avg,sd,tableToProcess,f"avg{variable}")
        return render(request, 'doctor/output.html', {
            'avg': round(avg, 3),
            'sd': round(sd, 3),
            'percentile': round(getFieldPercentile(variable, convert_to_dict(tableToProcess).get(f"avg{variable}"), tableToProcess.age), 1),
            'graph': graph,
        })

    return render(request, 'doctor/datapage.html', {'graph': graph, 'avg': round(avg,3), 'sd': round(sd,3), 'percentile': round(getFieldPercentile("Score", tableToProcess.avgScore, tableToProcess.age),1),
    'gottenTable': gottenTable, 'age': tableToProcess.age, 'lat1': round(tableToProcess.avgLatency1,3), 'lat2': round(tableToProcess.avgLatency2,3), 'lat3': round(tableToProcess.avgLatency3,3),
    'lat4': round(tableToProcess.avgLatency4,3), 'lat5': round(tableToProcess.avgLatency5,3), 'variable': variable,'duration': round(tableToProcess.avgDuration,3), '4span': round(tableToProcess.avg4SpanScore,3), '5span': round(tableToProcess.avg5SpanScore,3),
    'digit': round(tableToProcess.avgScoreDigit,3), "mixed": round(tableToProcess.avgScoreMixed,3), "score": round(tableToProcess.avgScore,3)})    

def generateGraph(avg, sd, table, variable):
    nums = numpy.linspace(avg - 3 * sd, avg + 3 * sd, 1000)

    distribution = norm.pdf(nums,avg, sd)

    fig, ax = matplotlib.pyplot.subplots()
    if(variable is None):
        ax.axvline(table.avgScore, label='Test Result', color='red') 
    else:
        ax.axvline(getattr(table, variable, None), label='Test Result', color='red') 
    ax.plot(nums, distribution, color='blue')
    ax.fill_between(nums, distribution, alpha=0.5)
    ax.set_title('Normal Distribution')
    ax.set_xlabel('Data Point')
    ax.set_ylabel('Likelihood')
    ax.legend()
    
    buffer = io.BytesIO()
    matplotlib.pyplot.savefig(buffer, format='png')
    buffer.seek(0)  
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    return graph
    

#Colors which can be added to print statements
#Call ENDC to reset the terminal font
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Functions for link management
def generateLink(age, user):
    toQuit = False
    i = 0
    while toQuit == False:
        linkIDToGenerate = f"{i+1:05}"
        try:
            doctorLink.objects.get(linkID=linkIDToGenerate)
            #print(linkIDToGenerate, "Already Exists") Debugging print statement
            i += 1
        except:
            print(linkIDToGenerate, f"does not exist: Generating new link with LinkID:{bcolors.BOLD}{bcolors.WARNING}", linkIDToGenerate, f"{bcolors.ENDC}")
            generatedLink = doctorLink.objects.create(linkID=linkIDToGenerate, doctor=user)
            individualTable.objects.create(
                linkID=generatedLink,
                age=age,
                completed=individualTable.completedStatus.INCOMPLETE,
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
                avgScore=None)
            print("LINK GENERATED")
            return linkIDToGenerate
