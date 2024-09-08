from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path("system-health/",views.system_data_view,name="system_data"),
    path('system_data_api/', views.system_data_api, name='system_data_api'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('threat_report/add', views.report_threat, name='threat_report_add'),

    path('incident_report/', views.incident_report, name='incident_report'),
    path('incident_report/overview', views.incident_report_overview, name='incident_report_overview'),
    
    path('threat_report/', views.threat, name='threat_report'),
    
    path('incident_list/', views.view_incidents, name='incident_list'),
    
    path('submit_incident/', views.submit_incident, name='submit_incident'),
    path('submit_threat/', views.submit_threat, name='submit_threat'),
    
    
]

