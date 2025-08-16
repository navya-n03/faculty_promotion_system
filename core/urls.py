from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_faculty_login(request):
    return redirect('faculty_login')

urlpatterns = [
    path('', redirect_to_faculty_login),

    # Faculty URLs
    path('faculty/register/', views.faculty_register, name='faculty_register'),
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/logout/', views.faculty_logout, name='faculty_logout'),

    # Custom Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/faculty/<int:faculty_id>/update/', views.update_promotion_status, name='update_promotion_status'),
]