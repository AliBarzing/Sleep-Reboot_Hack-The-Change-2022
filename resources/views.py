from django.shortcuts import render, get_object_or_404, redirect



def resource(request):
    return render(request,'resources.html')