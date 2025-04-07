from django.urls import path
from . import views
from .views import (BlogListView, ResumeExamplesView, CareerAdviceListView, CareerAdviceDetailView, BlogDetailView, \
                    CVTemplateListView, CVTemplateListView, CVTemplateDetailView, CVTemplateSelectView,
                    CoverLetterListView,
                    CoverLetterDetailView,
                    CoverLetterCreateView,
                    CoverLetterEditView,
                    CoverLetterDeleteView,
                    CoverLetterTemplateListView,
                    CoverLetterTemplateDetailView, HomePageView, ResourceHomeView, ResourceCategoryView,
                    ResourceArticleDetailView, CoverLetterTipsView, BlogCommentCreateView)

from .views import (
    ResourceHomeView,
    ResourceCategoryView,
    ResourceArticleDetailView,
    CoverLetterTipsView,
    BlogHomeView,
    BlogPostDetailView,
    BlogCategoryView,
    BlogTagView,
    BlogAuthorView,
    BlogSearchView,
)

app_name = 'home'

urlpatterns = [
   # path('', views.landing_page, name='landing'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('', HomePageView.as_view(), name='landing'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    # path('features/resume/', views.ResumeFeatureView.as_view(), name='features_resume'),
    path('features/resume/', views.features_resume, name='features_resume'),

    # path('features/cv/', views.CVFeatureView.as_view(), name='features_cv'),
    path('features/cover-letter/', views.CoverLetterFeatureView.as_view(), name='features_cover'),
    path('help/', views.HelpCenterView.as_view(), name='help'),
    path('templates/', views.TemplateListView.as_view(), name='templates'),

    # Template Routes
    path('template/<slug:slug>/', views.TemplateDetailView.as_view(), name='template_detail'),

    # Builder Routes
    # path('create/<slug:template_slug>/', views.ResumeCreateView.as_view(), name='create_resume'),
    path('edit/<uuid:uuid>/', views.ResumeEditView.as_view(), name='edit_resume'),
    path('preview/<uuid:uuid>/', views.ResumePreviewView.as_view(), name='preview_resume'),

    # Section Management
    path('section/add/', views.AddSectionView.as_view(), name='add_section'),
    path('section/update/<int:pk>/', views.UpdateSectionView.as_view(), name='update_section'),
    path('section/delete/<int:pk>/', views.DeleteSectionView.as_view(), name='delete_section'),
    path('section/reorder/', views.ReorderSectionsView.as_view(), name='reorder_sections'),

    # Content Management
    path('content/save/', views.SaveContentView.as_view(), name='save_content'),
    path('content/autosave/', views.AutoSaveView.as_view(), name='autosave'),

    # Export Options
    path('export/<uuid:uuid>/pdf/', views.ExportPDFView.as_view(), name='export_pdf'),
    path('export/<uuid:uuid>/word/', views.ExportWordView.as_view(), name='export_word'),
    path('export/<uuid:uuid>/txt/', views.ExportTextView.as_view(), name='export_text'),

    # AI Features
    path('ai/improve/', views.AIImproveView.as_view(), name='ai_improve'),
    path('ai/suggest/', views.AISuggestView.as_view(), name='ai_suggest'),
    path('ai/analyze/', views.AIAnalyzeView.as_view(), name='ai_analyze'),

    # Template Customization
    path('customize/colors/', views.CustomizeColorsView.as_view(), name='customize_colors'),
    path('customize/fonts/', views.CustomizeFontsView.as_view(), name='customize_fonts'),
    path('customize/layout/', views.CustomizeLayoutView.as_view(), name='customize_layout'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),

    # Resume Examples URLs
    path('resume-examples/', ResumeExamplesView.as_view(), name='resume_examples'),
    path('resume-examples/<str:category>/', ResumeExamplesView.as_view(), name='resume_examples_category'),

    # Career Advice URLs
    path('career-advice/', CareerAdviceListView.as_view(), name='career_advice'),
    path('career-advice/<slug:slug>/', CareerAdviceDetailView.as_view(), name='career_advice_detail'),
    path('cv-templates/', CVTemplateListView.as_view(), name='cv_templates'),
    path('cv-templates/<slug:slug>/', CVTemplateDetailView.as_view(), name='cv_template_detail'),
    path('cv-templates/<slug:slug>/select/', CVTemplateSelectView.as_view(), name='cv_template_select'),
    path('cover-letters/', CoverLetterListView.as_view(), name='cover_letter'),
    path('cover-letters/create/', CoverLetterCreateView.as_view(), name='cover_letter_create'),
    path('cover-letters/<uuid:uuid>/', CoverLetterDetailView.as_view(), name='cover_letter_detail'),
    path('cover-letters/<uuid:uuid>/edit/', CoverLetterEditView.as_view(), name='cover_letter_edit'),
    path('cover-letters/<uuid:uuid>/delete/', CoverLetterDeleteView.as_view(), name='cover_letter_delete'),

    # Cover Letter Templates
    path('cover-letter-templates/', CoverLetterTemplateListView.as_view(), name='cover_letter_templates'),
    path('cover-letter-templates/<slug:slug>/', CoverLetterTemplateDetailView.as_view(),
         name='cover_letter_template_detail'),
    # path('features/cv/', FeaturesCVView.as_view(), name='features_cv'),
    path('features/cv/', views.features_cv, name='features_cv'),

    path('', views.dashboard, name='dashboard'),
    path('resumes/', views.resume_list, name='resume_list'),
    #path('resumes/create/', views.create_resume, name='create_resume'),
    path('resumes/<int:resume_id>/edit/', views.resume_edit, name='edit_resume'),
    path('resumes/<int:resume_id>/download/', views.download_resume, name='download_resume'),
    path('applications/', views.job_applications, name='job_applications'),
    path('applications/add/', views.add_application, name='add_application'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('subscription/', views.subscription_details, name='subscription_details'),
    path('job-matching/', views.job_matching, name='job_matching'),
    path('resume/tips/', views.resume_tips, name='resume_tips'),
    path('resume/formats/', views.resume_formats, name='resume_formats'),
    # path('resume/builder/', views.resume_builder, name='resume_builder'),
    path('cover-letter/examples/', views.CoverLetterExamplesView.as_view(), name='cover_letter_examples'),
    path('job-search/', views.job_search, name='job_search'),
    path('interview-tips/', views.interview_tips, name='interview_tips'),
    path('salary-negotiation/', views.salary_negotiation, name='salary_negotiation'),
    path('career-development/', views.career_development, name='career_development'),
    path('choose-template/', views.choose_template, name='choose_template'),
    path('create', views.create_resume, name='create_resume'),
    path('my-resumes/', views.my_resumes, name='my_resumes'),
    path('resume/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),

    path('career-advice/', views.career_advice_list, name='career_advice'),
    path('career-advice/search/', views.career_advice_search, name='career_advice_search'),
    path('career-advice/category/<slug:category_slug>/', views.career_advice_category, name='career_advice_category'),
    path('career-advice/<slug:slug>/', views.career_advice_detail, name='career_advice_detail'),

    # Newsletter subscription
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    path('career-advice/', views.career_advice_list, name='career_advice'),
    path('career-advice/search/', views.career_advice_search, name='career_advice_search'),
    path('career-advice/category/<slug:category_slug>/', views.career_advice_category, name='career_advice_category'),
    path('career-advice/<slug:slug>/', views.career_advice_detail, name='career_advice_detail'),

    # Newsletter subscription
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    path('faq/', views.faq_home, name='faq_home'),
    path('category/<slug:slug>/', views.faq_category, name='category'),
    path('article/<slug:slug>/', views.faq_article, name='article'),
    path('search/', views.faq_search, name='search'),

    path('resources', ResourceHomeView.as_view(), name='resource_view'),
    path('category/<slug:slug>/', ResourceCategoryView.as_view(), name='category'),
    path('article/<slug:slug>/', ResourceArticleDetailView.as_view(), name='article_detail'),
    path('cover-letter-tips/', CoverLetterTipsView.as_view(), name='cover_letter_tips'),

    # Blog URLs
    path('blog/', BlogHomeView.as_view(), name='career_blog'),
    path('blog/post/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog/category/<slug:slug>/', BlogCategoryView.as_view(), name='blog_category'),
    path('blog/tag/<slug:slug>/', BlogTagView.as_view(), name='blog_tag'),
    path('blog/author/<int:pk>/', BlogAuthorView.as_view(), name='blog_author'),
    path('blog/search/', BlogSearchView.as_view(), name='blog_search'),
    path('blog/post/<slug:slug>/comment/', BlogCommentCreateView.as_view(), name='blog_comment_create'),

    path('resume-examples/', views.resume_examples_home, name='resume_examples'),

    # Industry pages
    path('resume-examples/industries/', views.IndustryListView.as_view(), name='resume_examples_industries'),
    path('resume-examples/industry/<slug:slug>/', views.IndustryDetailView.as_view(), name='resume_examples_industry'),

    # Job title pages
    path('resume-examples/job-titles/', views.JobTitleListView.as_view(), name='resume_examples_jobs'),
    path('resume-examples/job-title/<slug:slug>/', views.JobTitleDetailView.as_view(), name='resume_examples_job'),

    # Level pages
    path('resume-examples/level/<str:level>/', views.resume_examples_by_level, name='resume_examples_level'),

]