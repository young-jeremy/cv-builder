from django.urls import path
from . import views

app_name = 'templates_app'

urlpatterns = [
    path('', views.TemplateListView.as_view(), name='template_list'),
    path('templates/gallery/', views.template_gallery, name='template_gallery'),
    path('filter/', views.template_filter_ajax, name='template_filter_ajax'),
    path('<slug:slug>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('<slug:slug>/preview/', views.template_preview, name='template_preview'),
    path('<slug:slug>/select/', views.select_template, name='select_template'),
    path('contemporary/subscription_plans/', views.subscription_plans, name='subscription_plans'),
    # Add this to your templates_app/urls.py if you don't already have a home URL
    path('contemporary/', views.home, name='home'),

    # path('resume/editor/', views.resume_editor, name='resume_editor'),

    # Add these to your urls.py
    path('resume/section/<int:section_id>/', views.get_section, name='get_section'),
    path('resume/section/<int:section_id>/update/', views.update_section, name='update_section'),
    path('resume/<int:resume_id>/update-order/', views.update_section_order, name='update_section_order'),
    path('resume/<int:resume_id>/update-color/', views.update_color_scheme, name='update_color_scheme'),
    path('resume/<int:resume_id>/save/', views.save_resume, name='save_resume'),
    path('resume/<int:resume_id>/preview/', views.preview_resume, name='preview_resume'),
    path('resumes/<int:resume_id>/design/', views.resume_design, name='resume_design'),
    path('resumes/<int:resume_id>/download/', views.resume_download, name='resume_download'),

    path('my-resumes/', views.my_resumes, name='my_resumes'),
    path('templates/', views.ResumeTemplateListView.as_view(), name='resume_templates'),
    path('templates/professional/', views.ProfessionalTemplatesView.as_view(), name='professional_templates'),
    path('templates/<slug:template_slug>/create/', views.create_resume, name='create_resume_with_template'),
    path('create/', views.create_resume, name='create_resume'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resume/<uuid:uuid>/edit/', views.resume_edit, name='resume_edit'),
    path('resume/<uuid:uuid>/preview/', views.resume_preview, name='resume_preview'),
    path('resume/<uuid:uuid>/download/<str:format>/', views.download_resume, name='download_resume'),
    path('resume/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<uuid:resume_uuid>/add-section/', views.add_section, name='add_section'),
    path('resume/<uuid:uuid>/save/', views.save_resume, name='save_resume'),
    path('api/templates/', views.template_api, name='template_api'),

    path('templates/category/<slug:category_slug>/', views.category_showcase, name='category_showcase'),
    path('templates/compare/', views.compare_templates, name='compare_templates'),
    path('templates/<slug:template_slug>/', views.template_detail, name='latest_template_detail'),

    path('templates/professional/', views.ProfessionalTemplatesView.as_view(), name='professional_templates'),
    path('templates/simple/', views.SimpleTemplatesView.as_view(), name='simple_templates'),
    path('templates/modern/', views.ModernTemplatesView.as_view(), name='modern_templates'),
    path('templates/creative/', views.CreativeTemplatesView.as_view(), name='creative_templates'),
    path('templates/', views.AllTemplatesView.as_view(), name='all_templates'),

]

