from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/create/', views.tenant_create, name='tenant_create'),
    path('tenants/<int:pk>/edit/', views.tenant_edit, name='tenant_edit'),
    path('tenants/<int:pk>/delete/', views.tenant_delete, name='tenant_delete'),
    path('archived-tenants/', views.archived_tenant_list, name='archived_tenant_list'),
    path('archived-tenants/<int:pk>/unarchive/', views.unarchive_tenant, name='unarchive_tenant'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('export/properties/excel/', views.export_properties_excel, name='export_properties_excel'),
    path('export/tenants/excel/', views.export_tenants_excel, name='export_tenants_excel'),
    path('export/archived-tenants/excel/', views.export_archived_tenants_excel, name='export_archived_tenants_excel'),
    #path('print/properties/pdf/', views.print_properties_pdf, name='print_properties_pdf'),
    #path('print/tenants/pdf/', views.print_tenants_pdf, name='print_tenants_pdf'),
    path('print/archived-tenants/pdf/', views.print_archived_tenants_pdf, name='print_archived_tenants_pdf'),
    path('tenants/pdf/', views.tenant_list_pdf, name='tenant_list_pdf'),
    path('properties/pdf/', views.property_list_pdf, name='property_list_pdf'),
    path('forms_pdf/', views.forms_list, name='forms_list'),
    path('managers/', views.managers_list, name='managers_list'),
    path('managers/new/', views.manager_create, name='manager_create'),
    path('managers/<int:pk>/edit/', views.manager_edit, name='manager_edit'),
    #path('sectors/', views.sectors_list, name='sectors_list'),
    #path('sectors/create/', views.sectors_create, name='sectors_create'),
    #path('sectors/<int:pk>/edit/', views.sectors_edit, name='sectors_edit'),

]