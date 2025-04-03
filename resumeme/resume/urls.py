from django.urls import path
from . import views

app_name = 'resume'


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/<slug:template_slug>/', views.template_detail, name='template_detail'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path('resume/create/<slug:template_slug>/', views.create_resume, name='create_resume_with_template'),
    path('resume/<uuid:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<uuid:resume_id>/preview/', views.preview_resume, name='preview_resume'),
    path('resume/<uuid:resume_id>/export/', views.export_resume, name='export_resume'),
    path('resume/<uuid:resume_id>/delete/', views.delete_resume, name='delete_resume'),

    # Personal Info
    path('resume/<uuid:resume_id>/personal-info/update/', views.update_personal_info, name='update_personal_info'),

    # Experience
    path('resume/<uuid:resume_id>/experience/add/', views.add_experience, name='add_experience'),
    path('resume/<uuid:resume_id>/experience/<int:experience_id>/update/', views.update_experience,
         name='update_experience'),
    path('resume/<uuid:resume_id>/experience/<int:experience_id>/delete/', views.delete_experience,
         name='delete_experience'),

    # Education
    path('resume/<uuid:resume_id>/education/add/', views.add_education, name='add_education'),
    path('resume/<uuid:resume_id>/education/<int:education_id>/update/', views.update_education,
         name='update_education'),
    path('resume/<uuid:resume_id>/education/<int:education_id>/delete/', views.delete_education,
         name='delete_education'),

    # Skill
    path('resume/<uuid:resume_id>/skill/add/', views.add_skill, name='add_skill'),
    path('resume/<uuid:resume_id>/skill/<int:skill_id>/update/', views.update_skill, name='update_skill'),
    path('resume/<uuid:resume_id>/skill/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),

    # Project
    path('resume/<uuid:resume_id>/project/add/', views.add_project, name='add_project'),
    path('resume/<uuid:resume_id>/project/<int:project_id>/update/', views.update_project, name='update_project'),
    path('resume/<uuid:resume_id>/project/<int:project_id>/delete/', views.delete_project, name='delete_project'),

    # Language
    path('resume/<uuid:resume_id>/language/add/', views.add_language, name='add_language'),
    path('resume/<uuid:resume_id>/language/<int:language_id>/update/', views.update_language, name='update_language'),
    path('resume/<uuid:resume_id>/language/<int:language_id>/delete/', views.delete_language, name='delete_language'),

    # Certification
    path('resume/<uuid:resume_id>/certification/add/', views.add_certification, name='add_certification'),
    path('resume/<uuid:resume_id>/certification/<int:certification_id>/update/', views.update_certification,
         name='update_certification'),
    path('resume/<uuid:resume_id>/certification/<int:certification_id>/delete/', views.delete_certification,
         name='delete_certification'),

    # Color
    path('resume/<uuid:resume_id>/color/add/', views.add_color, name='add_color'),
    path('resume/<uuid:resume_id>/color/<int:color_id>/update/', views.update_color, name='update_color'),
    path('resume/<uuid:resume_id>/color/<int:color_id>/delete/', views.delete_color, name='delete_color'),

    # Reordering
    path('resume/<uuid:resume_id>/reorder/', views.reorder_items, name='reorder_items'),
]

