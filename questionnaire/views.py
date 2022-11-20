from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from manager.models import user, SB_questionnaire

def stop_bang_new(request):
    return render(request, 'stop_bang.html')

def sb_results(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    qaObj = SB_questionnaire(userObj.username)
    qaObj.snore = values[0].split('=')[1]
    qaObj.tired = values[1].split('=')[1]
    qaObj.choke = values[2].split('=')[1]
    qaObj.bp = values[3].split('=')[1]
    qaObj.neck = values[4].split('=')[1]
    if userObj.age > 50:
        qaObj.age = 1
    else:
        qaObj.age = 0
    if userObj.weight > 35:
        qaObj.age = 1
    else:
        qaObj.age = 0
    if userObj.gender == "Male":
        qaObj.age = 1
    else:
        qaObj.age = 0

    qaObj.save()
    # return redirect('main_page')
    
def BDI_refer(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    #context_dict = {'firstname': users.firstname, 'weight': users.weight, 'height':users.height}
    context = {
        'firstname': users.firstname,
        'BMI': int(users.weight)**2/(int(users.height)/100)
    }
    return render(request,'BDI.html', context)

def BDI_results(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')

    score = 0
    for counter in range(21): #number of questions
        score+= int(values[counter].split('=')[1])
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    userObj.BDI_score = score
    userObj.save()
    return redirect('questionnaire:ISI_refer')


def ISI_refer(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    context = {
        'firstname': users.firstname,
        'BMI': int(users.weight)**2/(int(users.height)/100)
    }
    return render(request,'ISI.html', context)

def ISI_results(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')

    score = 0
    for counter in range(7): #number of questions
        score+= int(values[counter].split('=')[1])
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    userObj.ISI_score = score
    userObj.save()
    return redirect('report:report')

    # return redirect('main_page')