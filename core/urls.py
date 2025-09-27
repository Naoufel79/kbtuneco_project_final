from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/apply/', views.project_apply, name='project_apply'),
    path('projects/<int:project_id>/withdraw/', views.project_withdraw, name='project_withdraw'),

    path('suggestions/', views.suggestions_for_user, name='suggestions'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('documents/upload/', views.upload_document, name='upload_document'),

    path('messages/', views.inbox, name='messages'),
    path('messages/inbox/', views.inbox, name='inbox'),
    path('messages/compose/', views.send_message, name='compose'),

    path('events/', views.events_list, name='events_list'),
    path('events/<int:event_id>/register/', views.event_register, name='event_register'),

    # auth

    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.profile_view, name='profile'),
    path('auth/profile/edit/', views.profile_edit, name='profile_edit'),

    # password reset
    path('auth/password_reset/', views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt',
        success_url='/auth/password_reset/done/'
    ), name='password_reset'),
    path('auth/password_reset/done/', views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        success_url='/auth/reset/done/'
    ), name='password_reset_confirm'),
    path('auth/reset/done/', views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('auth/my-projects/', views.user_projects, name='user_projects'),
    path('auth/my-applications/', views.my_applications, name='my_applications'),
    path('projects/<int:project_id>/applications/', views.manage_applications, name='manage_applications'),
    path('applications/<int:application_id>/accept/', views.accept_application, name='accept_application'),
    path('applications/<int:application_id>/reject/', views.reject_application, name='reject_application'),
]
