# from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect

from api import views
from .models import Group, Password, user


def index(request):
    # import pdb;pdb.set_trace()
    if (request.COOKIES.get('permission') != 'T'):
        return redirect('index')
    else:

        userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
        all_groups = userObj.group_set.all()
        # template = loader.get_template('manager/index.html')
        context = {'all_groups': all_groups, 'user_name': request.COOKIES.get('user')}
        r = render(request, 'index_manage.html', context)

        html = ''
        # return HttpResponse(template.render(context, request))
        return r


def passwordsPage(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'passwordsPage.html',
                  {'passes': group.password_set.all(), 'group_id': group.id, 'user_name': request.COOKIES.get('user')})


def createGroup(request, i):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    userObj = user.objects.filter(username=request.COOKIES.get('user'))[0]
    newGroup = Group()
    newGroup.user = userObj
    newGroup.groupName = values[0].split('=')[1].replace('+', ' ')
    newGroup.groupDesc = values[1].split('=')[1].replace('+', ' ')
    newGroup.save()

    return redirect('manager:index')


def addPassword(request, i, j):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    id2 = int(values[0].split('=')[1])
    group = get_object_or_404(Group, pk=id2)

    newPass = Password()
    newPass.group = group
    newPass.name = values[1].split('=')[1].replace('+', ' ')
    newPass.password = values[2].split('=')[1].replace('+', ' ')
    newPass.desc = values[3].split('=')[1].replace('+', ' ')
    newPass.save()
    return redirect('manager:passwords', pk=group.id)


def deletePassword(request, i, j):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    group = get_object_or_404(Group, pk=int(values[0].split('=')[1]))
    password = group.password_set.all().filter(pk=int(values[1].split('=')[1]))[0]
    password.delete()
    return redirect('manager:passwords', pk=group.id)


def deleteGroup(request, i, j):
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')

    group = get_object_or_404(Group, pk=int(values[0].split('=')[1]))
    group.delete()
    return redirect('manager:index')


def sign_up(request, i):
    # import pdb;pdb.set_trace()
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    all_users = user.objects.all()
    if all_users:
        for users in all_users:
            if users.username != values[0].split('=')[1]:
                if values[1].split('=')[1] == values[2].split('=')[1]:
                    newuser = user()
                    newuser.username = values[0].split('=')[1]
                    newuser.password = values[1].split('=')[1]
                    newuser.save()
                    r = redirect('register:complete_info')
                    r.set_cookie('user', newuser.username)
                    r.set_cookie('permission', 'T')
                    return r
                else:
                    return redirect('register:register_new')
            else:
                return redirect('register:register_new')
    else:
        if values[1].split('=')[1] == values[2].split('=')[1]:
            newuser = user()
            newuser.username = values[0].split('=')[1]
            newuser.password = values[1].split('=')[1]
            newuser.save()
            r = redirect(views.new)
            r.set_cookie('user', newuser.username)
            r.set_cookie('permission', 'T')
            return r


def login(request, i):
    # import pdb;pdb.set_trace()
    inputs = request.get_full_path()
    values = inputs.split('?')[1].split('&')
    username = values[0].split('=')[1]
    passw = values[1].split('=')[1]
    all_users = user.objects.all()
    for users in all_users:
        if users.username == username:
            if users.password == passw:
                if users.new_user == 1:
                    r = redirect('register:complete_info')
                else:
                    r = redirect('questionnaire:BDI_refer')
                r.set_cookie('user', username)
                r.set_cookie('permission', 'T')
                return r
            else:
                return redirect('index')


def logout(request):
    r = redirect('index')
    r.delete_cookie('user')
    r.delete_cookie('name')
    r.set_cookie('permission', 'F')
    return r
