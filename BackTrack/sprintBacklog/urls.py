from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.SprintBacklogMain.as_view(), name='sprint_backlog_main'),
    #path('pbi/<int:pbi_pk>', views.SprintBacklogPBIMain.as_view(), name='sprint_backlog_pbi_main'),
    #path('pbi/add', views.SprintBacklogPBIAdd.as_view(), name='sprint_backlog_pbi_add'),
    #path('pbi/<int:pbi_pk>/task/<int:task_pk>', views.TaskMain.as_view(), name='task_main'),
    #path('pbi/<int:pbi_pk>/task/add', views.TaskAdd.as_view(), name='task_add'),
    #path('pbi/<int:pbi_pk>/task/<int:task_pk>/modify', views.task_modify, name='task_modify'),
    #path('pbi/<int:pk>/task/<int:task_pk>/delete', views.TaskDelete.as_view(), name='task_delete'),
]
