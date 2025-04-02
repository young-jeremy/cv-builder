from django.urls import path
from . import views

app_name = 'templates_app'

urlpatterns = [
    path('', views.TemplateListView.as_view(), name='template_list'),
    path('filter/', views.template_filter_ajax, name='template_filter_ajax'),
    path('<slug:slug>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('<slug:slug>/preview/', views.template_preview, name='template_preview'),
    path('<slug:slug>/select/', views.select_template, name='select_template'),
    path('contemporary/subscription_plans/', views.subscription_plans, name='subscription_plans'),
    # Add this to your templates_app/urls.py if you don't already have a home URL
    path('contemporary/', views.home, name='home'),

    path('resume/editor/', views.resume_editor, name='resume_editor'),

    # Add these to your urls.py
    path('resume/section/<int:section_id>/', views.get_section, name='get_section'),
    path('resume/section/<int:section_id>/update/', views.update_section, name='update_section'),
    path('resume/<int:resume_id>/update-order/', views.update_section_order, name='update_section_order'),
    path('resume/<int:resume_id>/update-color/', views.update_color_scheme, name='update_color_scheme'),
    path('resume/<int:resume_id>/save/', views.save_resume, name='save_resume'),
    path('resume/<int:resume_id>/preview/', views.preview_resume, name='preview_resume'),
    path('resumes/<int:resume_id>/design/', views.resume_design, name='resume_design'),
path('resumes/<int:resume_id>/download/', views.resume_download, name='resume_download'),path('resumes/<int:resume_id>/download/', views.resume_download, name='resume_download'),

]

