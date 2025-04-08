from django.contrib import admin
from .models import TemplateCategory, ResumeTemplate, TemplateColor, TemplateSection, UserTemplateSelection

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class TemplateColorInline(admin.TabularInline):
    model = TemplateColor
    extra = 1

class TemplateSectionInline(admin.TabularInline):
    model = TemplateSection
    extra = 1

@admin.register(TemplateColor)
class TemplateColorAdmin(admin.ModelAdmin):
    list_display = ('template', 'name', 'primary_color', 'is_default')
    list_filter = ('template', 'is_default')
    search_fields = ('name', 'template__name')

@admin.register(TemplateSection)
class TemplateSectionAdmin(admin.ModelAdmin):
    list_display = ('template', 'section_type', 'name', 'is_required', 'order')
    list_filter = ('template', 'section_type', 'is_required')
    search_fields = ('name', 'template__name')

@admin.register(UserTemplateSelection)
class UserTemplateSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'selected_at')
    list_filter = ('template', 'selected_at')
    search_fields = ('user__username', 'template__name')
    date_hierarchy = 'selected_at'

