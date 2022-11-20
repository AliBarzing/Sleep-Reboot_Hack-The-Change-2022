from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from manager.models import user
from django.contrib.auth.models import User


def report(request):
    users = user.objects.filter(username=request.COOKIES.get('user'))[0] #This gets the information of the participant
    context = {
        'firstname': users.firstname,
        'BDI_score': int(users.BDI_score),
        'ISI_score': int(users.ISI_score),
        'SB_score': int(users.SB_score)
    }
    return render(request,'report.html', context)

def resources_refer(request):
    return redirect('resources:resource')