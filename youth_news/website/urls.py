from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
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
    
    # view news
    path('create_post/', views.createPost, name='create_post'),
    path('edit_post/<slug:slug>/', views.editPost, name='edit_post'),
    path('delete_post/<slug:slug>/', views.deletePost, name='delete_post'),
    path('news/<slug:slug>/', views.blog, name="blog"),
    path('view_blogs/', views.viewBlogs, name="view_blogs"),
    path('pending_blogs/', views.pendingBlogs, name="pending_blogs"),

    # approve/reject post - Developer
    path('developer/', views.developerDashboard, name="developer"),
    path('pending_blogs_developer/', views.pendingBlogsDeveloper, name="pending_blogs_developer"),
    path('approve_post/<slug:slug>/', views.approvePost, name='approve_post'),
    path('delete_post_developer/<slug:slug>/', views.deletePostDeveloper, name='delete_post_developer'),
    path('preview/<slug:slug>/', views.previewPost, name="preview_post"),
]
