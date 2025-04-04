from allauth.socialaccount.providers.mediawiki.provider import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from colorfield.fields import ColorField
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


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
        ('classic', 'Classic'),
        ('executive', 'Executive'),
        ('corporate', 'Corporate'),
        ('minimalist', 'Minimalist'),
        ('elegant', 'Elegant'),
        ('bold', 'Bold'),
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

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='simple')
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='classic')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue')
    popularity = models.IntegerField(default=0)  # For sorting by popularity
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='template_previews/')
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
    popularity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
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
        return reverse('template_detail', args=[self.slug])

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

