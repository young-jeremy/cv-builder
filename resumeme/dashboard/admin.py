from django.contrib import admin
from .models import ResumeTemplate, UserTemplateSelection

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_premium', 'is_active', 'usage_count')
    list_filter = ('category', 'is_premium', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'preview_image', 'category')
        }),
        ('Template Content', {
            'fields': ('html_structure', 'css'),
            'classes': ('collapse',),
        }),
        ('Features', {
            'fields': ('has_photo', 'is_premium', 'is_active', 'allows_color_customization',
                      'allows_font_customization', 'allows_section_reordering')
        }),
        ('Default Colors', {
            'fields': ('primary_color', 'secondary_color', 'text_color')
        }),
        ('Statistics', {
            'fields': ('usage_count',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('usage_count',)

@admin.register(UserTemplateSelection)
class UserTemplateSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'selected_at')
    list_filter = ('template', 'selected_at')
    search_fields = ('user__email', 'template__name')
    date_hierarchy = 'selected_at'

