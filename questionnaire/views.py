from django.shortcuts import render

# Create your views here.
from manager.models import user

def stop_bang_new(request):
    return render(request, 'stop_bang.html')

def nosas_new(request):
    return render(request, 'nosas.html')
