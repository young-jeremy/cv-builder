from django.contrib import admin
from .models import (
    Testimonial, Feature, Pricing, FAQ,
    Contact, TeamMember, CompanyStats
)
from django.contrib import admin
from .models import FAQCategory, FAQArticle

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FAQArticle)
class FAQArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_popular', 'updated_at')
    list_filter = ('category', 'is_popular')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


from .models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    Education, Skill, Language, Certification, Project, SavedSection
)
from django.contrib import admin
from .models import CareerCategory, CareerArticle, NewsletterSubscription

@admin.register(CareerCategory)
class CareerCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CareerArticle)
class CareerArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email', 'name')


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_premium', 'is_featured')
    list_filter = ('category', 'is_premium', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'created_at', 'updated_at')
    list_filter = ('template', 'is_public', 'created_at')
    search_fields = ('title', 'user__username')

@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'type', 'order', 'is_visible')
    list_filter = ('type', 'is_visible')
    search_fields = ('title', 'resume__title')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('company', 'position')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'gpa')
    list_filter = ('degree', 'is_current')
    search_fields = ('institution', 'field_of_study', 'location')
    ordering = ('-start_date', 'institution')
    date_hierarchy = 'start_date'

from django.contrib import admin
from .models import Language, Skill

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'section')  # Changed 'proficiency' to 'level' and removed 'order'
    list_filter = ('level',)  # Changed 'proficiency' to 'level'
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'section')  # Removed 'order'
    list_filter = ('level',)
    search_fields = ('name',)
    ordering = ('name',)
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'expiry_date')
    search_fields = ('name', 'issuing_organization')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('title', 'technologies')

@admin.register(SavedSection)
class SavedSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'section_type', 'created_at')
    list_filter = ('section_type',)
    search_fields = ('title', 'user__username')

admin.site.register(Testimonial)
admin.site.register(Feature)
admin.site.register(Pricing)
admin.site.register(FAQ)
admin.site.register(Contact)
admin.site.register(TeamMember)
admin.site.register(CompanyStats)