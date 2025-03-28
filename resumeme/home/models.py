from django.conf import settings
from django.db import models
from accounts.models import User
from colorfield.fields import ColorField
from django.db import models
from django.db import models
from colorfield.fields import ColorField
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
# from .models import CVTemplate, Resume
from .forms import CVTemplateSelectForm
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from django.urls import reverse
import uuid


class CoverLetterTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='cover_letter_templates/')
    html_content = models.TextField()
    css_content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:cover_letter_template_detail', kwargs={'slug': self.slug})

class CoverLetter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100, blank=True)
    recipient_title = models.CharField(max_length=100, blank=True)
    company_address = models.TextField(blank=True)
    content = models.TextField()
    template = models.ForeignKey(CoverLetterTemplate, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company_name}"

    def get_absolute_url(self):
        return reverse('home:cover_letter_detail', kwargs={'uuid': self.uuid})


class CVTemplate(models.Model):
    CATEGORY_CHOICES = [
        ('professional', 'Professional'),
        ('creative', 'Creative'),
        ('modern', 'Modern'),
        ('simple', 'Simple'),
        ('academic', 'Academic'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    preview_image = models.ImageField(upload_to='cv_templates/previews/')
    thumbnail = models.ImageField(upload_to='cv_templates/thumbnails/')
    html_template = models.FileField(upload_to='cv_templates/html/')
    css_template = models.FileField(upload_to='cv_templates/css/')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home:cv_template_detail', kwargs={'slug': self.slug})


class CVTemplateListView(ListView):
#    model = CVTemplate
    template_name = 'home/cv_templates/list.html'
    context_object_name = 'templates'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      #  context['categories'] = CVTemplate.objects.values_list(
         #   'category', flat=True).distinct()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(is_active=True)


class CVTemplateDetailView(DetailView):
#    model = CVTemplate
    template_name = 'home/cv_templates/detail.html'
    context_object_name = 'template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CVTemplateSelectForm()
      #  context['related_templates'] = CVTemplate.objects.filter(
"""            category=self.object.category
        ).exclude(
            id=self.object.id
        ).filter(
            is_active=True
        )[:3]
        return context"""


class CVTemplateSelectView(LoginRequiredMixin, CreateView):
#    model = Resume
    form_class = CVTemplateSelectForm
    template_name = 'home/cv_templates/select.html'
    success_url = reverse_lazy('home:resume_builder')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.template = get_object_or_404(
            CVTemplate,
            slug=self.kwargs['slug']
        )
        return super().form_valid(form)


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home:blog_detail', kwargs={'slug': self.slug})


class ResumeExample(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='resume_examples/')
    pdf_file = models.FileField(upload_to='resume_examples/pdfs/')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CareerAdvice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    featured_image = models.ImageField(upload_to='career_advice/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Career Advice"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home:career_advice_detail', kwargs={'slug': self.slug})



class ResumeTemplate(models.Model):
    CATEGORY_CHOICES = [
        ('professional', 'Professional'),
        ('creative', 'Creative'),
        ('modern', 'Modern'),
        ('simple', 'Simple'),
        ('executive', 'Executive'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    preview_image = models.ImageField(upload_to='template_previews/')
    thumbnail = models.ImageField(upload_to='template_thumbnails/')
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    description = models.TextField()
    color_schemes = models.JSONField(null=True, blank=True)  # Store predefined color combinations
    font_pairs = models.JSONField(null=True, blank=True)     # Store font combinations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TemplateSection(models.Model):
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    html_content = models.TextField()
    css_content = models.TextField()
    order = models.PositiveIntegerField(default=0)



class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company}"

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # For FontAwesome or similar icon classes
    show_on_homepage = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Pricing(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ])
    features = models.TextField()  # Store as JSON or one feature per line
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.billing_cycle}"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'General'),
        ('pricing', 'Pricing'),
        ('technical', 'Technical'),
    ])
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"

class CompanyStats(models.Model):
    users_count = models.IntegerField(default=0)
    resumes_created = models.IntegerField(default=0)
    success_stories = models.IntegerField(default=0)
    countries_reached = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Company Stats'

    def __str__(self):
        return f"Company Stats - Last Updated: {self.last_updated}"


class Template(models.Model):
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='template_previews/')
    is_premium = models.BooleanField(default=False)

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    primary_color = ColorField(default='#1a91f0')
    is_public = models.BooleanField(default=False, help_text="Make this resume visible to others")

    font_family = models.CharField(
        max_length=50,
        choices=[
            ('inter', 'Inter'),
            ('roboto', 'Roboto'),
            ('opensans', 'Open Sans'),
            ('lato', 'Lato')
        ],
        default='inter'
    )
    font_size = models.CharField(
        max_length=20,
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large')
        ],
        default='medium'
    )

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True)
    professional_summary = models.TextField(blank=True)


from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class WorkExperience(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]

    # Basic Information
    company = models.CharField(max_length=100, help_text="Name of the company",  null=True, blank=True)
    position = models.CharField(max_length=100, help_text="Your job title",  null=True, blank=True)
    location = models.CharField(max_length=100, help_text="City, Country or Remote",  null=True, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPES,
        default='full_time'
    )

    # Dates
    start_date = models.DateField(help_text="Start date of employment")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if this is your current position"
    )
    is_current = models.BooleanField(
        default=False,
        help_text="Check if this is your current position"
    )

    # Details
    description = models.TextField(
        help_text="Describe your responsibilities and achievements"
    )
    achievements = models.JSONField(
        default=list,
        blank=True,
        help_text="List of key achievements"
    )
    company_website = models.URLField(
        blank=True,
        help_text="Company website URL (optional)"
    )

    # Organization
    resume = models.ForeignKey(
        'Resume',
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )
    order = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"

    def __str__(self):
        return f"{self.position} at {self.company}"

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date")

        if self.is_current:
            self.end_date = None

        if self.end_date:
            self.is_current = False

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Calculate the duration of employment"""
        from dateutil.relativedelta import relativedelta
        end = self.end_date or timezone.now().date()
        delta = relativedelta(end, self.start_date)
        years = delta.years
        months = delta.months

        if years and months:
            return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"
        elif years:
            return f"{years} year{'s' if years != 1 else ''}"
        elif months:
            return f"{months} month{'s' if months != 1 else ''}"
        else:
            return "Less than a month"


from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Education(models.Model):
    DEGREE_TYPES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('doctorate', 'Doctorate'),
        ('certification', 'Certification'),
        ('diploma', 'Diploma'),
        ('other', 'Other'),
    ]

    # Basic Information
    institution = models.CharField(
        max_length=200,
        help_text="Name of the school or university", null=True, blank=True
    )
    degree = models.CharField(
        max_length=100,
        choices=DEGREE_TYPES,
        help_text="Type of degree received",  null=True, blank=True
    )
    field_of_study = models.CharField(
        max_length=100,
        help_text="Major or field of study",
        blank=True
    )
    location = models.CharField(
        max_length=100,
        help_text="City, State/Province, Country",  null=True, blank=True
    )

    # Dates
    start_date = models.DateField(help_text="Start date of education")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if currently studying"
    )
    is_current = models.BooleanField(
        default=False,
        help_text="Check if currently studying"
    )

    # Academic Details
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Grade Point Average (optional)"
    )
    achievements = models.JSONField(
        default=list,
        blank=True,
        help_text="List of achievements, honors, etc."
    )
    activities = models.TextField(
        blank=True,
        help_text="Extracurricular activities and societies"
    )
    description = models.TextField(
        blank=True,
        help_text="Additional details about your studies"
    )

    # Organization
    resume = models.ForeignKey(
        'Resume',
        on_delete=models.CASCADE,
        related_name='education'
    )
    order = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date")

        if self.is_current:
            self.end_date = None

        if self.end_date:
            self.is_current = False

        if self.gpa is not None and (self.gpa < 0 or self.gpa > 4.0):
            raise ValidationError("GPA must be between 0.0 and 4.0")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Calculate the duration of education"""
        from dateutil.relativedelta import relativedelta
        end = self.end_date or timezone.now().date()
        delta = relativedelta(end, self.start_date)
        years = delta.years
        months = delta.months

        if years and months:
            return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"
        elif years:
            return f"{years} year{'s' if years != 1 else ''}"
        elif months:
            return f"{months} month{'s' if months != 1 else ''}"
        else:
            return "Less than a month"


from django.db import models

class Skill(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    # Basic Information
    name = models.CharField(
        max_length=50,
        help_text="Name of the skill"
    )
    level = models.CharField(
        max_length=20,
        choices=SKILL_LEVELS,
        default='intermediate',
        help_text="Proficiency level"
    )

    # Relationship
    section = models.ForeignKey(
        'ResumeSection',
        on_delete=models.CASCADE,
        related_name='skills', blank=True, null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        unique_together = ['section', 'name']  # Prevent duplicate skills in the same section

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    @property
    def level_percentage(self):
        """Convert skill level to percentage for progress bars"""
        level_percentages = {
            'beginner': 25,
            'intermediate': 50,
            'advanced': 75,
            'expert': 100
        }
        return level_percentages.get(self.level, 0)


from django.db import models

class Language(models.Model):
    PROFICIENCY_LEVELS = [
        ('elementary', 'Elementary'),
        ('limited', 'Limited Working'),
        ('professional', 'Professional Working'),
        ('full', 'Full Professional'),
        ('native', 'Native/Bilingual'),
    ]

    # Basic Information
    name = models.CharField(
        max_length=50,
        help_text="Language name"
    )
    level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_LEVELS,
        default='elementary',
        help_text="Proficiency level"
    )

    # Relationship
    section = models.ForeignKey(
        'ResumeSection',
        on_delete=models.CASCADE,
        related_name='languages', null=True, blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        unique_together = ['section', 'name']  # Prevent duplicate languages in the same section

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    @property
    def level_percentage(self):
        """Convert proficiency level to percentage for progress bars"""
        level_percentages = {
            'elementary': 20,
            'limited': 40,
            'professional': 60,
            'full': 80,
            'native': 100
        }
        return level_percentages.get(self.level, 0)

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class ResumeSection(models.Model):
    SECTION_TYPES = [
        ('personal', 'Personal Information'),
        ('summary', 'Professional Summary'),
        ('experience', 'Work Experience'),
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('languages', 'Languages'),
        ('certifications', 'Certifications'),
        ('projects', 'Projects'),
        ('custom', 'Custom Section'),
    ]

    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='sections')
    type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=100)

    # Work Experience Fields
    company = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the company")
    position = models.CharField(max_length=100, blank=True, null=True, help_text="Your job title")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="City, Country or Remote")
    start_date = models.DateField(null=True, blank=True, help_text="Start date of employment")
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current position")
    is_current = models.BooleanField(default=False, help_text="Check if this is your current position")
    description = models.TextField(blank=True, help_text="Describe your responsibilities and achievements")
    achievements = models.JSONField(default=list, blank=True, help_text="List of key achievements")
    company_website = models.URLField(blank=True, help_text="Company website URL (optional)")
    employment_type = models.CharField(
        max_length=20,
        choices=[
            ('full_time', 'Full-time'),
            ('part_time', 'Part-time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
            ('freelance', 'Freelance'),
        ],
        default='full_time',
        blank=True,
        null=True
    )

    # Common fields
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Resume Section"
        verbose_name_plural = "Resume Sections"

    def __str__(self):
        return f"{self.resume.title} - {self.title}"

    def clean(self):
        super().clean()
        # Validate dates for work experience
        if self.type == 'experience':
            if self.end_date and self.start_date and self.end_date < self.start_date:
                raise ValidationError("End date cannot be earlier than start date")

            if self.is_current:
                self.end_date = None

            if self.end_date:
                self.is_current = False

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Calculate the duration of employment for experience sections"""
        if self.type != 'experience' or not self.start_date:
            return None

        from dateutil.relativedelta import relativedelta
        end = self.end_date or timezone.now().date()
        delta = relativedelta(end, self.start_date)
        years = delta.years
        months = delta.months

        if years and months:
            return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"
        elif years:
            return f"{years} year{'s' if years != 1 else ''}"
        elif months:
            return f"{months} month{'s' if months != 1 else ''}"
        else:
            return "Less than a month"

class Certification(models.Model):
    section = models.ForeignKey(ResumeSection, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-issue_date']


class Project(models.Model):
    section = models.ForeignKey(ResumeSection, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.JSONField(default=list)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']


class SavedSection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.JSONField()
    section_type = models.CharField(max_length=20, choices=ResumeSection.SECTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.title}"