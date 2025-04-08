from django.contrib import admin
from .models import (
    TemplateCategory, PersonalInfo,
    Experience, Education, Skill, Project, Language, Certification,
    UserProfile, TemplateColor
)

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
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

