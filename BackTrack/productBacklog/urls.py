from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.ProductBacklogMain.as_view(), name='product_backlog_main'),
    path('pbi/<int:pbi_pk>', views.PBIMain.as_view(), name='pbi_main'),
    path('pbi/add', views.PBIAdd.as_view(), name='pbi_add'),
    path('pbi/<int:pbi_pk>/modify', views.pbi_modify, name='pbi_modify'),
    path('pbi/<int:pk>/delete/', views.PBIDelete.as_view(), name='pbi_delete'),
]
