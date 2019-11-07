from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.SprintBacklogMain.as_view(), name='sprint_backlog_main'),
    path('pbi/<int:pbi_pk>', views.SprintPBIMain.as_view(), name='sprint_pbi_main'),
    path('pbi/<int:pbi_pk>/remove', views.remove, name='remove'),
    path('pbi/add', views.SprintPBIAdd.as_view(), name='sprint_pbi_add'),
    path('pbi/add/<int:pbi_pk>', views.add, name='add_pbi'),
    path('add', views.SprintBacklogAdd.as_view(), name='add_sprint'),
    path('<int:sprint_pk>', views.active, name='active'),
    #path('pbi/<int:pbi_pk>/task/<int:task_pk>', views.TaskMain.as_view(), name='task_main'),
    #path('pbi/<int:pbi_pk>/task/add', views.TaskAdd.as_view(), name='task_add'),
    #path('pbi/<int:pbi_pk>/task/<int:task_pk>/modify', views.task_modify, name='task_modify'),
    #path('pbi/<int:pk>/task/<int:task_pk>/delete', views.TaskDelete.as_view(), name='task_delete'),
    path('finish/', views.finish, name='finish'),
]
