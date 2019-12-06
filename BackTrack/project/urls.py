from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectMain.as_view(), name='project_main'),
    path('<int:project_pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('<int:pk>/finish', views.ProjectFinish.as_view(), name='project_finish'),
]
