from django.conf.urls import url, include

import questionnaire.views as questionnaire_views

app_name = 'questionnaire'
urlpatterns = [
    # new stop bang questionnaire
    url(r'^stop_bang$', questionnaire_views.stop_bang_refer, name='stop_bang_refer'),

    # stop bang submit
    url(r'sb_results$', questionnaire_views.sb_results, name='sb_results'),

    #new BDI questionnaire
    url(r'^BDI$', questionnaire_views.BDI_refer, name='BDI_refer'),

    url(r'^BDI_results$', questionnaire_views.BDI_results, name='BDI_results'),

        # new stop ISI questionnaire
    url(r'^ISI$', questionnaire_views.ISI_refer, name='ISI_refer'),

    url(r'^ISI_results$', questionnaire_views.ISI_results, name='ISI_results'),
]
