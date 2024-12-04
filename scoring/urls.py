from django.urls import path

from scoring.views.views import scoring_view, scoring_result_list, scoring_result_detail, scoring_result_detail_api

urlpatterns = [
    path('', scoring_view, name='home'),
    path('scoring-tasks/', scoring_result_list, name='scoring_tasks'),
    path('scoring-tasks/<int:pk>/', scoring_result_detail, name='scoring_task_detail'),
    path('scoring-tasks-api/<int:pk>', scoring_result_detail_api, name='scoring_task_detail_api'),
]
