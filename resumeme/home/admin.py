from django.contrib import admin
from .models import (
    Testimonial, Feature, Pricing, FAQ,
    Contact, TeamMember, CompanyStats
)
from django.contrib import admin
from .models import FAQCategory, FAQArticle
from django.contrib import admin
from .models import Statistic, TrustedCompany, ResumeCounter
from django.contrib import admin
from .models import Industry, JobPosition, CoverLetterExample
from django.contrib import admin
from .models import ResourceCategory, ResourceArticle, Tip
from django.contrib import admin
from .models import (
    ResourceCategory, ResourceArticle, Tip,
    BlogCategory, BlogTag, BlogAuthor, BlogPost, BlogComment
)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'job_title')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'job_title')


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('name', 'email', 'website', 'created_at')
    fields = ('name', 'email', 'website', 'content', 'is_approved', 'created_at')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'published_at')
    list_filter = ('status', 'category', 'is_featured', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'summary')
    date_hierarchy = 'published_at'
    filter_horizontal = ('tags',)
    inlines = [BlogCommentInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'featured_image')
        }),
        ('Publication', {
            'fields': ('status', 'is_featured', 'published_at', 'read_time')
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Approve selected comments"


class TipInline(admin.TabularInline):
    model = Tip
    extra = 1

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(ResourceArticle)
class ResourceArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'summary')
    inlines = [TipInline]

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'order')
    list_filter = ('article',)
    search_fields = ('title', 'content')


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title',)

@admin.register(CoverLetterExample)
class CoverLetterExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry', 'job_position', 'is_featured', 'created_at')
    list_filter = ('industry', 'job_position', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_editable = ('is_featured',)



@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('order',)

@admin.register(TrustedCompany)
class TrustedCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(ResumeCounter)
class ResumeCounterAdmin(admin.ModelAdmin):
    list_display = ('count', 'last_updated')


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