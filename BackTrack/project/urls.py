from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectMain.as_view(), name='project_main'),
    path('<int:project_pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('<int:pk>/finish', views.ProjectFinish.as_view(), name='project_finish'),
    path('<int:project_pk>/manager/invite/', views.ManagerInvite.as_view(), name='manager_invite'),
    path('<int:project_pk>/developer/invite/', views.DeveloperInvite.as_view(), name='developer_invite'),
    path('<int:project_pk>/manager/<int:manager_pk>/email/', views.sendManagerEmail, name='manager_email'),
    path('<int:project_pk>/developer/<int:developer_pk>/email/', views.sendDeveloperEmail, name='developer_email'),
    path('<int:project_pk>/manager/<int:manager_pk>/', views.ManagerJoinConfirm.as_view(), name='manager_join_confirm'),
    path('<int:project_pk>/developer/<int:developer_pk>/', views.DeveloperJoinConfirm.as_view(), name='developer_join_confirm'),
    path('<int:project_pk>/manager/<int:manager_pk>/join/', views.managerJoin, name='manager_join'),
    path('<int:project_pk>/developer/<int:developer_pk>/join/', views.developerJoin, name='developer_join'),
    path('create/', views.ProjectCreate.as_view(), name='project_create'),
]
