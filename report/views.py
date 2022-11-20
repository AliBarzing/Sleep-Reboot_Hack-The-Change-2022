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

    #BDI_SCORE classification
    if int(users.BDI_score) <=15:
        bdi_str = 'Normal'
    elif int(users.BDI_score) <=30:
        bdi_str = 'Borderline'
    elif int(users.BDI_score) <=40: 
        bdi_str = 'Severe'
    else:
        bdi_str = 'Extreme'

    #ISI_SCORE classification
    if int(users.ISI_score) <=12:
        isi_str = 'No clinically significant'
    elif int(users.ISI_score) <=21:
        isi_str = 'Clinically moderate'
    else:
        isi_str = 'Clinically severe'

    context = {
        'user_name':users.username,
        'firstname': users.firstname,
        'BDI_score': int(users.BDI_score),
        'ISI_score': int(users.ISI_score),
        'SB_score': int(users.SB_score),
        'BDI_str': bdi_str,
        'ISI_str': isi_str

    }

    print(bdi_str)
    return render(request,'report.html', context)