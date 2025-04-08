from django.db import models

from django.conf import settings
from django.utils.text import slugify
from colorfield.fields import ColorField
import uuid

from phonenumber_field.formfields import PhoneNumberField


class TemplateCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Template Categories"
        ordering = ['display_order', 'name']


class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name='templates')
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to='template_previews/')
    html_structure = models.TextField()
    css_styles = models.TextField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        ordering = ['display_order', 'name']


class PersonalInfo(models.Model):
    resume = models.OneToOneField(ResumeTemplate, on_delete=models.CASCADE, related_name='personal_info')
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"Personal Info for {self.resume.title}"


class Experience(models.Model):
    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.position} at {self.company}"

    class Meta:
        ordering = ['order', '-start_date']


class Education(models.Model):
    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

    class Meta:
        ordering = ['order', '-start_date']


class Skill(models.Model):
    LEVEL_CHOICES = (
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
        (5, 'Master'),
    )

    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=3)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']


class Project(models.Model):
    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']


class Language(models.Model):
    PROFICIENCY_CHOICES = (
        ('elementary', 'Elementary'),
        ('limited', 'Limited Working'),
        ('professional', 'Professional Working'),
        ('full_professional', 'Full Professional'),
        ('native', 'Native/Bilingual'),
    )

    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='professional')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']


class Certification(models.Model):
    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    is_premium = models.BooleanField(default=False)
    subscription_expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class TemplateColor(models.Model):
    resume = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50)
    color_code = ColorField()

    def __str__(self):
        return f"{self.name}: {self.color_code}"

