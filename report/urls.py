from django.conf.urls import url, include

import report.views as report_views

app_name = 'report'
urlpatterns = [
    # new stop bang questionnaire
    url(r'^report$', report_views.report, name='report'),

]
