from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [

    # Resume CRUD
    path('', views.resume_list, name='list'),
    path('create/', views.create_resume, name='create'),
    path('<slug:slug>/', views.resume_detail, name='detail'),
    path('<slug:slug>/edit/', views.edit_resume, name='edit'),
    path('<slug:slug>/delete/', views.delete_resume, name='delete'),
    path('<slug:slug>/duplicate/', views.duplicate_resume, name='duplicate'),

    # Resume export
    path('<slug:slug>/export/pdf/', views.export_resume, {'format': 'pdf'}, name='export_pdf'),
    path('<slug:slug>/export/docx/', views.export_resume, {'format': 'docx'}, name='export_docx'),

    # Resume sharing
    path('<slug:slug>/share/', views.share_resume, name='share'),
    path('public/<str:public_url>/', views.public_resume, name='public'),

    # Resume search
    path('search/', views.search_resumes, name='search'),

    # AJAX endpoints for resume sections
    path('<slug:slug>/education/add/', views.add_education, name='add_education'),
    path('education/<int:id>/update/', views.update_education, name='update_education'),
    path('education/<int:id>/delete/', views.delete_education, name='delete_education'),

    # Similar endpoints would be added for other section types
    # (experiences, skills, projects, etc.)

    # Reordering sections
    path('<slug:slug>/reorder/', views.reorder_sections, name='reorder_sections'),
#     path('templates/', views.ResumeTemplateListView.as_view(), name='resume_templates'),
    path('templates/<slug:template_slug>/create/', views.create_resume, name='create_resume_with_template'),
    # path('create/', views.create_resume, name='create_resume'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('my_resumes/', views.my_resumes, name='my_resumes'),
    path('upload_resume/', views.upload_resume, name='upload'),

    path('my-resumes/', views.my_resumes, name='my_resumes'),
    path('templates/', views.ResumeTemplateListView.as_view(), name='resume_templates'),
    path('templates/<slug:template_slug>/create/', views.create_resume, name='create_resume_with_template'),
    path('create/', views.create_resume, name='create_resume'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resume/<uuid:uuid>/edit/', views.resume_edit, name='resume_edit'),
    path('resume/<uuid:uuid>/preview/', views.resume_preview, name='resume_preview'),
    path('resume/<uuid:uuid>/download/<str:format>/', views.download_resume, name='download_resume'),
    path('resume/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<uuid:resume_uuid>/add-section/', views.add_section, name='add_section'),
    path('resume/<uuid:uuid>/save/', views.save_resume, name='save_resume'),


]

