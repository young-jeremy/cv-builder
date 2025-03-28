from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from colorfield.fields import ColorField
from django import forms
# from .models import Resume, ResumeSection

"""class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'primary_color', 'font_family']
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
        }"""

class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label='Upload your existing resume',
        help_text='Supported formats: PDF, DOCX, TXT',
        widget=forms.FileInput(attrs={'accept': '.pdf,.docx,.txt'})
    )
"""
class ResumeSectionForm(forms.ModelForm):
    class Meta:
        model = ResumeSection
        fields = ['title', 'content']
        widgets = {
            'content': forms.HiddenInput(),
        }"""


class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='template_previews/')
    html_structure = models.TextField(help_text="HTML structure with placeholders for resume data")
    css = models.TextField(help_text="CSS styles for the template")

    # Template categorization
    CATEGORY_CHOICES = [
        ('professional', 'Professional'),
        ('creative', 'Creative'),
        ('simple', 'Simple'),
        ('modern', 'Modern'),
        ('executive', 'Executive'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Template features
    has_photo = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Template customization options
    allows_color_customization = models.BooleanField(default=True)
    allows_font_customization = models.BooleanField(default=True)
    allows_section_reordering = models.BooleanField(default=True)

    # Default colors
    primary_color = ColorField(default='#2D3E50')
    secondary_color = ColorField(default='#3498DB')
    text_color = ColorField(default='#333333')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Stats
    usage_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserTemplateSelection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)

    # User customizations
    primary_color = ColorField(null=True, blank=True)
    secondary_color = ColorField(null=True, blank=True)
    text_color = ColorField(null=True, blank=True)
    font_family = models.CharField(max_length=100, null=True, blank=True)

    # Metadata
    selected_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'template')


class UserDashboardSettings(models.Model):
    """User preferences for dashboard appearance and functionality."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_settings', blank=True, null=True)

    # Layout preferences
    LAYOUT_CHOICES = [
        ('grid', 'Grid View'),
        ('list', 'List View'),
        ('compact', 'Compact View'),
    ]
    default_layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='grid')

    # Display preferences
    show_resume_stats = models.BooleanField(default=True, help_text="Show resume view and download statistics")
    show_job_applications = models.BooleanField(default=True, help_text="Show job application tracking")
    show_ai_suggestions = models.BooleanField(default=True, help_text="Show AI-powered suggestions")

    # Notification settings
    email_notifications = models.BooleanField(default=True)
    application_reminders = models.BooleanField(default=True)
    resume_update_reminders = models.BooleanField(default=True, help_text="Remind to update resume periodically")
    notification_enabled = models.BooleanField(default=True, help_text="Master toggle for all notifications")

    # Theme preference
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    # Customization
    accent_color = ColorField(default='#2D9CDB')

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Dashboard Settings"


class JobApplication(models.Model):
    """Track job applications submitted by users."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications', blank=True, null=True)

    # Job details
    job_title = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    job_description = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    job_url = models.URLField(blank=True)

    # Application details
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='saved')

    # Resume used
    # resume = models.ForeignKey('resume.Resume', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    # cover_letter = models.ForeignKey('resume.CoverLetter', on_delete=models.SET_NULL, null=True, blank=True,related_name='applications')

    # Dates
    date_saved = models.DateTimeField(default=timezone.now)
    date_applied = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Follow-up
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_reminder = models.BooleanField(default=False)

    # Notes
    notes = models.TextField(blank=True)

    # Contact information
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return f"{self.job_title} at {self.company}"

    def days_since_application(self):
        """Calculate days since application was submitted."""
        if self.date_applied:
            from django.utils import timezone
            delta = timezone.now() - self.date_applied
            return delta.days
        return None



