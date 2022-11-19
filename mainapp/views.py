from django.shortcuts import render, redirect


def index(request):
    if request.COOKIES.get('permission') == 'T':
        return redirect('manager:index')
    else:
        return render(request, 'index.html')


def main(request):
    return render(request, 'main.html')
