from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductBacklogMain.as_view(), name='product_backlog_main'),
    path('pbi/<int:pbi>', views.PBIMain.as_view(), name='pbi_main'),
    path('pbi/add', views.PBIAdd.as_view(), name='pbi_add'),
    path('pbi/<int:pbi>/modify', views.PBIModify.as_view(), name='pbi_modify'),
    path('pbi/<int:pbi>/delete', views.PBIDelete.as_view(), name='pbi_delete'),
]
