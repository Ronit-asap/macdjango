from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-username/', views.change_username, name='change_username'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email'),
    path('change-phone/', views.change_phone, name='change_phone'),
    path('change-address/', views.change_address, name='change_address'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('success/', views.success, name='success'),
]