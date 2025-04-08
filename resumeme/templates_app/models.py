import uuid
from allauth.socialaccount.providers.mediawiki.provider import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from colorfield.fields import ColorField
from django.conf import settings
from django.core.files.base import ContentFile
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from weasyprint import HTML
import tempfile
import uuid as uuid_module  # Import as uuid_module to avoid name conflict
import uuid as uuid_module
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Resume(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    uuid = models.UUIDField(default=uuid_module.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey('ResumeTemplate', on_delete=models.SET_NULL, null=True, related_name='resumes')
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    content = models.JSONField(default=dict)
    custom_css = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Personal information fields
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    headline = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        ordering = ['-created_at']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('templates_app:resume_preview', kwargs={'uuid': self.uuid})

    def save(self, *args, **kwargs):
        # Ensure we have a title
        if not self.title and self.content and 'personal_info' in self.content:
            personal_info = self.content.get('personal_info', {})
            first_name = personal_info.get('first_name', '')
            last_name = personal_info.get('last_name', '')
            if first_name or last_name:
                self.title = f"{first_name} {last_name}'s Resume".strip()
            else:
                self.title = "Untitled Resume"

        # Call the parent save method
        super().save(*args, **kwargs)


class TemplateCategory(models.Model):
    """Categories for resume templates (e.g., Simple, ATS, Two-column)"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Template Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ResumeTemplate(models.Model):
    # ... existing fields ...
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    CATEGORY_CHOICES = (
        ('simple', 'Simple'),
        ('professional', 'Professional'),
        ('modern', 'Modern'),
        ('creative', 'Creative'),
    )

    STYLE_CHOICES = (
        ('executive', 'Executive'),
        ('corporate', 'Corporate'),
        ('classic', 'Classic'),
        ('minimalist', 'Minimalist'),
        ('elegant', 'Elegant'),
        ('bold', 'Bold'),
        ('modern-executive', 'Modern Executive'),
        ('two-column', 'Two Column'),
    )

    COLOR_CHOICES = (
        ('blue', 'Blue'),
        ('black', 'Black'),
        ('gray', 'Gray'),
        ('green', 'Green'),
        ('burgundy', 'Burgundy'),
        ('navy', 'Navy'),
    )
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes_users', blank=True, null=True)
    template = models.ForeignKey('ResumeTemplate', on_delete=models.SET_NULL, null=True, related_name='resume_template')
    title = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', blank=True, null=True)
    content = models.JSONField(default=dict)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='simple')
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='classic')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue')
    popularity = models.IntegerField(default=0)  # For sorting by popularity
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    preview_image = ProcessedImageField(
        upload_to='template_previews',
        processors=[ResizeToFill(400, 600)],
        format='JPEG',
        options={'quality': 85},
        null=True,
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html_content = None
        self.css_content = None

    def generate_preview(self):
        # Combine HTML and CSS
        html_content = f"""
            <html>
            <head>
                <style>{self.css_content}</style>
            </head>
            <body>
                {self.html_content}
            </body>
            </html>
            """

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            # Render HTML to PNG
            HTML(string=html_content).write_png(tmp.name)

            # Save to model field
            with open(tmp.name, 'rb') as f:
                self.preview_image.save(f"{self.name.lower().replace(' ', '-')}.png", ContentFile(f.read()), save=False)

        self.save()

    thumbnail = models.ImageField(upload_to='template_thumbnails/', blank=True)
    categories = models.ManyToManyField(TemplateCategory, related_name='templates')
    color_scheme = models.CharField(max_length=50, default='blue')  # Add a default value



    # Template features
    has_photo = models.BooleanField(default=True)
    is_ats_friendly = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')

    # Template structure
    html_structure = models.TextField(help_text="HTML structure with placeholders")
    css_template = models.TextField(help_text="CSS styles for the template")

    # Stats
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-popularity', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.thumbnail and self.preview_image:
            # Logic to create thumbnail from preview_image could go here
            pass
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('templates_app:template_detail', args=[self.slug])

    def increment_popularity(self):
        """Increment the popularity counter when template is used"""
        self.popularity += 1
        self.save(update_fields=['popularity'])


class TemplateColor(models.Model):
    """Color schemes for resume templates"""
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50)
    primary_color = ColorField(default='#2D9CDB')
    secondary_color = ColorField(default='#333333')
    accent_color = ColorField(default='#F2F2F2')
    text_color = ColorField(default='#333333')
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_default', 'name']
        unique_together = ['template', 'name']

    def __str__(self):
        return f"{self.template.name} - {self.name}"


class TemplateSection(models.Model):
    """Sections available in a resume template"""
    SECTION_TYPES = [
        ('contact', 'Contact Information'),
        ('summary', 'Professional Summary'),
        ('experience', 'Work Experience'),
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('languages', 'Languages'),
        ('certifications', 'Certifications'),
        ('projects', 'Projects'),
        ('awards', 'Awards'),
        ('publications', 'Publications'),
        ('references', 'References'),
        ('custom', 'Custom Section'),
    ]

    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['template', 'section_type']

    def __str__(self):
        return f"{self.template.name} - {self.name}"


class UserTemplateSelection(models.Model):
    """Tracks which templates users have selected/used"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)
    color_scheme = models.ForeignKey(TemplateColor, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-selected_at']

    def __str__(self):
        return f"{self.user.username} - {self.template.name}"

