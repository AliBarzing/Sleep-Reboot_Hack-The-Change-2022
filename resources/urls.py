from django.conf.urls import url, include

import resources.views as resources_views

app_name = 'resources'

urlpatterns = [
    # new resources page
    url(r'^resources$', resources_views.resource, name='resource'),

]