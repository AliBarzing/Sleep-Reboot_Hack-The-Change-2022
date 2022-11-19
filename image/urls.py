from django.conf.urls import url, include

import image.views as image_views

app_name = 'image'
urlpatterns = [
    # save image
    url(r'^save$', image_views.image_save, name='image_save'),
    # login
    url(r'^login$', image_views.image_login, name='image_login'),

    url(r'^sendPic', image_views.sendPic, name='send_pic'),

    url(r'^logPic', image_views.logpic, name='log_pic'),

]
