from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.inicio_comunidad,name='home'),
    path('newuser/',views.createuser,name='createuser'),
   #path('listavol', views.lista_com, name='listavol'),
    path('vol_getdata/<int:user_id>',views.get_volunteerdata, name='vol_profile'),
    path('manager_getdata/<int:user_id>',views.manager_getdata, name='profile'),
    path('ver_org/', views.ver_org, name='ver_org'),
    path('vista-org/', views.vista_org, name='vista_org'),
    path('org_getdata/<int:organization_id>/',views.get_orgdata, name='org_getdata'),
    path('crear_org/', views.crear_org, name='crear_org'),
    path('delete_organization/<int:organization_id>/', views.delete_organization, name='delete_organization'),
    path('update_organizationdata/<int:organization_id>/', views.update_organizationdata, name='update_organizationdata'),
    path('organization/<int:organization_id>/comments/', views.view_comments, name='view_comments'),
    path('get_interesados/<int:organization_id>/', views.get_interesados, name='get_interesados'),
    path('view_intereses/<int:organization_id>/', views.view_intereses, name='view_intereses'),
    path('update_organizationname/<int:organization_id>/', views.update_organizationname, name='update_organizationname'),
    path('update_organizationmail/<int:organization_id>/', views.update_organizationmail, name='update_organizationmail'),
]