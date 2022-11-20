
from django.conf.urls import url , include
from django.contrib import admin
import mainapp.views as main_views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from api import views

app_name = 'home'
urlpatterns = [

    url(r'^admin/', admin.site.urls),

    # home page
    url(r'^$',main_views.index,name='index'),

    # password manager
    url(r'^manager/', include('manager.urls')),

    # main panell
    url(r'^main_page$', main_views.main, name='main_page'),

    #refister pages
    url(r'^register/',include('register.urls',namespace='register')),

    #image pages
    url(r'^picture/',include('image.urls',namespace='image')),

    #Questionnaire page
    url(r'^questionnaire/',include('questionnaire.urls',namespace='questionnaire')),

    #Report page
    url(r'^report/',include('report.urls',namespace='report')),

    #Resources page
    url(r'^resources/',include('resources.urls',namespace='resources')),

    url(r'^recognize/(?P<img>(.)*)$', views.recognize),

    url(r'^train/(?P<img>(.)*)$', views.train),

    url(r'^new/$', views.new),

    url(r'^users/$', views.users),





]
