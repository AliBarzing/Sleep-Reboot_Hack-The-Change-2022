from urllib import parse

from django.shortcuts import render, redirect

from api import views


def image_login(request):
    return render(request, 'login_picture.html')


def image_save(request):
    return render(request, 'save_picture.html')


def sendPic(request):
    url = parse.unquote(request.GET.get("image"))
    r = redirect(views.train, img=url)
    return r


def logpic(request):
    url = parse.unquote(request.GET.get("image"))
    r = redirect(views.recognize, img=url)
    return r
