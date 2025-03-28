from django.urls import path
from . import views

app_name  = 'dashboard'

urlpatterns = [
    # Main Dashboard
    path('', views.dashboard, name='dashboard'),

    # Resume Management
    path('templates/', views.template_gallery, name='template_gallery'),
    path('templates/<slug:template_slug>/', views.template_preview, name='template_preview'),
    path('templates/<slug:template_slug>/select/', views.select_template, name='select_template'),
    path('templates/<slug:template_slug>/customize/', views.customize_template, name='customize_template'),
    path('templates/preview/', views.render_resume_preview, name='render_resume_preview'),

    path('dashboard/resumes/', views.resume_list, name='resume_list'),
    # path('dashboard/resume/create/', views.create_resume, name='create_resume'),
    path('dashboard/resume/<int:id>/edit/', views.edit_resume, name='edit_resume'),
    path('dashboard/resume/<int:id>/delete/', views.delete_resume, name='delete_resume'),
    path('dashboard/resume/<int:id>/duplicate/', views.duplicate_resume, name='duplicate_resume'),
    path('dashboard/resume/<int:id>/download/', views.download_resume, name='download_resume'),

    # Profile Management
    path('dashboard/profile/', views.profile_settings, name='profile_settings'),
    path('dashboard/profile/password/', views.change_password, name='change_password'),
    path('dashboard/profile/email/', views.change_email, name='change_email'),

    # Subscription Management
    path('dashboard/subscription/', views.subscription_details, name='subscription_details'),
    path('dashboard/subscription/upgrade/', views.upgrade_subscription, name='upgrade_subscription'),
    path('dashboard/subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('dashboard/billing/', views.billing_history, name='billing_history'),

    # Template Management
    path('dashboard/templates/<int:id>/', views.template_preview, name='template_preview'),

    # Job Applications Tracking
    path('dashboard/applications/', views.job_applications, name='job_applications'),
    path('dashboard/applications/add/', views.add_application, name='add_application'),
    path('dashboard/applications/<int:id>/edit/', views.edit_application, name='edit_application'),

    # Analytics & Reports
    path('dashboard/analytics/', views.resume_analytics, name='resume_analytics'),
    path('dashboard/reports/', views.generate_reports, name='generate_reports'),

    # Settings
    path('dashboard/settings/', views.account_settings, name='account_settings'),
    path('dashboard/settings/notifications/', views.notification_settings, name='notification_settings'),
    path('dashboard/settings/privacy/', views.privacy_settings, name='privacy_settings'),

    # Help & Support
    path('dashboard/help/', views.help_center, name='help_center'),
    path('dashboard/support/', views.support_ticket, name='support_ticket'),
    path('dashboard/feedback/', views.submit_feedback, name='submit_feedback'),

    # API Access (if needed)
    path('dashboard/api-keys/', views.api_keys, name='api_keys'),
    path('dashboard/api-docs/', views.api_documentation, name='api_documentation'),

    # Activity & History
#    path('dashboard/activity/', views.activity_log, name='activity_log'),
#    path('dashboard/downloads/', views.download_history, name='download_history'),

    # Saved Items
    #path('dashboard/saved-sections/', views.saved_sections, name='saved_sections'),
    #path('dashboard/templates/favorites/', views.favorite_templates, name='favorite_templates'),

    path('', views.dashboard_index, name='index'),
    path('templates/', views.template_gallery, name='template_gallery'),
    path('templates/<slug:template_slug>/', views.template_preview, name='template_preview'),
    path('templates/<slug:template_slug>/select/', views.select_template, name='select_template'),
    path('templates/<slug:template_slug>/customize/', views.customize_template, name='customize_template'),
    path('templates/preview/', views.render_resume_preview, name='render_resume_preview'),
    path('create/', views.create_resume, name='create'),
    path('upload/', views.upload_resume, name='upload'),
    path('my-resumes/', views.my_resumes, name='my_resumes'),
]