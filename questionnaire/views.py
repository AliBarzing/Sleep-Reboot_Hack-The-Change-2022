from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from manager.models import user
from django.contrib.auth.models import User

def stop_bang_new(request):
    return render(request, 'stop_bang.html')


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
    return redirect('main_page')


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
    return redirect('main_page')
