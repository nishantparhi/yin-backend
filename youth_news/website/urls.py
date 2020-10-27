from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),    
    path('single/',views.single,name="single"),
    path('contact-us/', views.contactPage, name="contact"),

    # Dashboard
    path('dashboard/', views.dashboardPage, name="dashboard"),

    # Registration
    path('register/',views.register, name='register'),

    # Forget Password
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),
        name="reset_password"
    ),

    path(
        'reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name="password_reset_done"
    ),

    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"
    ),

    path(
        'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),

]
