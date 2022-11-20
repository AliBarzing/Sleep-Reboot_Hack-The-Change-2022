from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from manager.models import user
from django.contrib.auth.models import User


def registernew(request):
    return render(request, 'register.html')


def chang_pass(request):
    return render(request, 'register2.html')


def complete_info(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    context = {'user_name':users.username}
    return render(request, 'demographic.html',context)


def changepassword(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    if userObj.password is values[0].split('=')[1]:
        if values[1].split('=')[1] is values[2].split('=')[1]:
            userObj.password = values[1].split('=')[1]
            userObj.save()
            return redirect('main_page')
        else:
            return redirect('register:chang_pass')
    else:
        return redirect('register:chang_pass')


def complite(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    userObj.firstname = values[0].split('=')[1]
    userObj.lastname = values[1].split('=')[1]
    userObj.gender = values[3].split('=')[1]
    userObj.educationstatus = values[4].split('=')[1]
    userObj.dateofbirth = values[2].split('=')[1]
    userObj.weight = values[5].split('=')[1]
    userObj.height = values[6].split('=')[1]
    userObj.demography_entered()

    userObj.save()
    print(userObj.gender)
    return redirect('questionnaire:BDI_refer')
