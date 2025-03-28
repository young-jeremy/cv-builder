from django.db import models
from django.conf import settings
from django.utils.text import slugify
from colorfield.fields import ColorField
import uuid


class Resume(models.Model):
    """Main resume model that contains user's resume data."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, default="My Resume")
    slug = models.SlugField(unique=True, blank=True)

    # Selected template
    template = models.ForeignKey('dashboard.ResumeTemplate', on_delete=models.SET_NULL,
                                 null=True, related_name='resumes')

    # Basic information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Professional summary
    headline = models.CharField(max_length=100, blank=True, help_text="Your professional title")
    summary = models.TextField(blank=True, help_text="A brief professional summary")

    # Profile photo
    profile_photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)

    # Customization
    primary_color = ColorField(default='#2D9CDB')
    secondary_color = ColorField(default='#3498DB')
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    public_url = models.CharField(max_length=100, blank=True, unique=True)

    # Stats
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.full_name}'s Resume - {self.title}"

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if slug exists and append random string if needed
            if Resume.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"

        # Generate public URL if resume is public and URL not set
        if self.is_public and not self.public_url:
            self.public_url = uuid.uuid4().hex[:10]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('resume:detail', kwargs={'slug': self.slug})

    def get_public_url(self):
        from django.urls import reverse
        return reverse('resume:public', kwargs={'public_url': self.public_url})

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Education(models.Model):
    """Education entries for a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-end_date', '-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    """Work experience entries for a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-end_date', '-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Skill(models.Model):
    """Skills listed on a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    # Optional skill level (1-5)
    LEVEL_CHOICES = [
        (1, 'Novice'),
        (2, 'Beginner'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    ]
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, null=True, blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects listed on a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-end_date', '-start_date']

    def __str__(self):
        return self.title


class Certification(models.Model):
    """Certifications listed on a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-issue_date']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"


class Language(models.Model):
    """Languages listed on a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)

    PROFICIENCY_CHOICES = [
        ('elementary', 'Elementary'),
        ('limited', 'Limited Working'),
        ('professional', 'Professional Working'),
        ('full_professional', 'Full Professional'),
        ('native', 'Native/Bilingual'),
    ]
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Reference(models.Model):
    """References listed on a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    reference_text = models.TextField(blank=True)

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class CustomSection(models.Model):
    """Custom sections for a resume."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='custom_sections')
    title = models.CharField(max_length=100)
    content = models.TextField()

    # For ordering in the resume
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ResumeExport(models.Model):
    """Track resume exports."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='exports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('txt', 'Plain Text'),
    ]
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resume_exports/')

    def __str__(self):
        return f"{self.resume.title} - {self.format} - {self.created_at}"


class CoverLetter(models.Model):
    """Cover letter model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cover_letters')
    title = models.CharField(max_length=100, default="My Cover Letter")
    slug = models.SlugField(unique=True, blank=True)

    # Associated resume
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True, related_name='cover_letters')

    # Content
    recipient_name = models.CharField(max_length=100, blank=True)
    recipient_company = models.CharField(max_length=100, blank=True)
    recipient_address = models.TextField(blank=True)
    greeting = models.CharField(max_length=100, blank=True, default="Dear Hiring Manager,")
    body = models.TextField()
    closing = models.CharField(max_length=100, blank=True, default="Sincerely,")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if slug exists and append random string if needed
            if CoverLetter.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"

        super().save(*args, **kwargs)


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
