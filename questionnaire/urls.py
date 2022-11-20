from django.conf.urls import url, include

import questionnaire.views as questionnaire_views

app_name = 'register'
urlpatterns = [
    # new stop bang questionnaire
    url(r'^/stop_bang', questionnaire_views.stop_bang_new, name='stop_bang_new'),

    # new stop bang questionnaire
    url(r'^/nosas', questionnaire_views.nosas_new, name='nosas_new')
]
