from django.shortcuts import render, get_object_or_404, redirect

from manager.models import user


def registernew(request):
    return render(request, 'register.html')


def chang_pass(request):
    return render(request, 'register2.html')


def complete_info(request):
    return render(request, 'register3.html')


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
    # userObj.firstname = values[0].split('=')[1]
    # userObj.lastname = values[1].split('=')[1]
    # userObj.country = values[2].split('=')[1]
    # userObj.save()
    return redirect('main_page')
