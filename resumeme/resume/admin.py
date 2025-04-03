from django.contrib import admin
from .models import (
    TemplateCategory, ResumeTemplate, Resume, PersonalInfo,
    Experience, Education, Skill, Project, Language, Certification,
    UserProfile, TemplateColor
)

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('display_order', 'name')

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_premium', 'is_active', 'display_order')
    list_filter = ('category', 'is_premium', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')

class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo
    can_delete = False

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'template__category', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    inlines = [PersonalInfoInline, ExperienceInline, EducationInline, SkillInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_premium', 'subscription_expires')
    list_filter = ('is_premium',)
    search_fields = ('user__username', 'user__email')

# Register other models
admin.site.register(Project)
admin.site.register(Language)
admin.site.register(Certification)
admin.site.register(TemplateColor)

