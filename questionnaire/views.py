from django.shortcuts import render

# Create your views here.
from manager.models import user, SB_questionnaire

def stop_bang_new(request):
    return render(request, 'stop_bang.html')

def sb_results(request):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    qaObj = SB_questionnaire(userObj.username)
    qaObj.snore = values[0].split('=')[1]
    qaObj.tired = values[1].split('=')[1]
    qaObj.choke = values[2].split('=')[1]
    qaObj.bp = values[3].split('=')[1]
    qaObj.neck = values[4].split('=')[1]
    if userObj.age > 50:
        qaObj.age = 1
    else:
        qaObj.age = 0
    if userObj.weight > 35:
        qaObj.age = 1
    else:
        qaObj.age = 0
    if userObj.gender == "Male":
        qaObj.age = 1
    else:
        qaObj.age = 0

    qaObj.save()
    # return redirect('main_page')