from django.conf.urls import url, include

import register.views as register_views

app_name = 'register'
urlpatterns = [
    # new registration
    url(r'^new$', register_views.registernew, name='register_new'),
    # change password
    url(r'^chang_password$', register_views.chang_pass, name='chang_pass'),
    # change password
    url(r'^complete_info$', register_views.complete_info, name='complete_info'),
    # sign up
    url(r'^manager/', include('manager.urls')),

    url(r'^changepassword$', register_views.changepassword, name='changepassword'),

    url(r'^complite', register_views.complite, name='complite'),

]
