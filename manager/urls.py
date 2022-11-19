# from django.contrib import admin
from django.conf.urls import url

from . import views

app_name = 'manager'
urlpatterns = [

    url(r'^$', views.index, name='index'),

    # /manager/id
    url(r'^(?P<pk>[0-9]+)/$', views.passwordsPage, name='passwords'),

    url(r'^createGroup/(.)*$', views.createGroup, name='createGroup'),

    url(r'^(.)*addPassword/(.)*$', views.addPassword, name='addPassword'),

    url(r'^(.)*deletePassword/(.)*$', views.deletePassword, name='deletePassword'),

    url(r'^(.)*deleteGroup/(.)*$', views.deleteGroup, name='deleteGroup'),

    # login
    url(r'^sign_up/(.)*$', views.sign_up, name='sign_up'),

    url(r'^login/(.)*$', views.login, name='login'),

    url(r'^logout', views.logout, name='logout'),
]
