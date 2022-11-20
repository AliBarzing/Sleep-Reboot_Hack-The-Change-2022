from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from manager.models import user, SB_questionnaire
from datetime import datetime

def stop_bang_refer(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    context = {
        'user_name':users.username,
    }
    return render(request, 'stop_bang.html',context)

def sb_results(request):
    score = 0
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    qaObj = SB_questionnaire(userObj.username)
    qaObj.snore = values[0].split('=')[1]
    score += int(qaObj.snore)
    qaObj.tired = values[1].split('=')[1]
    score += int(qaObj.snore)
    qaObj.choke = values[2].split('=')[1]
    score += int(qaObj.choke)
    qaObj.bp = values[3].split('=')[1]
    score += int(qaObj.bp)
    qaObj.neck = values[4].split('=')[1]
    score += int(qaObj.neck)
    dob = userObj.dateofbirth
    now_date = datetime.now()
    delta = now_date - datetime.strptime(dob, '%Y-%m-%d')
    age = delta.days / 365.2425
    if age > 50:
        qaObj.age = 1
        score += 1
    else:
        qaObj.age = 0
    if int(userObj.weight) > 35:
        qaObj.weight = 1
        score += 1
    else:
        qaObj.weight = 0
    if userObj.gender == "Male":
        qaObj.sex = 1
        score += 1
    else:
        qaObj.sex = 0

    userObj.SB_score = score

    userObj.save()
    qaObj.save()
    return redirect('report:report')
    
def BDI_refer(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    #context_dict = {'firstname': users.firstname, 'weight': users.weight, 'height':users.height}
    context = {
        'user_name':users.username,
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
        'user_name':users.username,
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
    return redirect('questionnaire:stop_bang_refer')