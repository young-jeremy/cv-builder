from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from resume.models import TemplateCategory, ResumeTemplate
import os
import base64
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates sample resume templates for each category'

    def handle(self, *args, **options):
        # Ensure categories exist
        categories = TemplateCategory.objects.all()
        if not categories.exists():
            self.stdout.write(
                self.style.WARNING('No template categories found. Run create_template_categories command first.'))
            return

        # Create templates for each category
        self._create_simple_templates()
        self._create_modern_templates()
        self._create_classical_templates()
        self._create_creative_templates()

        self.stdout.write(self.style.SUCCESS('Successfully created resume templates'))

    def _create_simple_templates(self):
        category = TemplateCategory.objects.get(slug='simple')

        # Simple Clean template
        simple_clean = {
            'name': 'Simple Clean',
            'slug': 'simple-clean',
            'description': 'A clean, minimalist design that puts your content front and center.',
            'html_structure': '''
<div class="resume simple-clean">
    <header class="resume-header">
        <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
        <p class="job-title">{{ resume.personal_info.job_title }}</p>
        <div class="contact-info">
            {% if resume.personal_info.email %}<span>{{ resume.personal_info.email }}</span>{% endif %}
            {% if resume.personal_info.phone %}<span>{{ resume.personal_info.phone }}</span>{% endif %}
            {% if resume.personal_info.address %}<span>{{ resume.personal_info.address }}</span>{% endif %}
            {% if resume.personal_info.website %}<span>{{ resume.personal_info.website }}</span>{% endif %}
        </div>
    </header>

    {% if resume.personal_info.summary %}
    <section class="resume-section">
        <h2 class="section-title">Summary</h2>
        <div class="section-content">
            <p>{{ resume.personal_info.summary }}</p>
        </div>
    </section>
    {% endif %}

    {% if resume.experiences.exists %}
    <section class="resume-section">
        <h2 class="section-title">Experience</h2>
        <div class="section-content">
            {% for experience in resume.experiences.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ experience.position }}</h3>
                    <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                    <div class="item-date">
                        {{ experience.start_date|date:"M Y" }} - 
                        {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                    </div>
                </div>
                {% if experience.description %}
                <div class="item-description">
                    {{ experience.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.educations.exists %}
    <section class="resume-section">
        <h2 class="section-title">Education</h2>
        <div class="section-content">
            {% for education in resume.educations.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                    <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                    <div class="item-date">
                        {{ education.start_date|date:"M Y" }} - 
                        {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                    </div>
                </div>
                {% if education.description %}
                <div class="item-description">
                    {{ education.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.skills.exists %}
    <section class="resume-section">
        <h2 class="section-title">Skills</h2>
        <div class="section-content">
            <div class="skills-list">
                {% for skill in resume.skills.all %}
                <div class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-level">
                        {% for i in "12345" %}
                            {% if forloop.counter <= skill.level %}
                            <span class="skill-dot active"></span>
                            {% else %}
                            <span class="skill-dot"></span>
                            {% endif %}
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if resume.projects.exists %}
    <section class="resume-section">
        <h2 class="section-title">Projects</h2>
        <div class="section-content">
            {% for project in resume.projects.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ project.title }}</h3>
                    {% if project.start_date %}
                    <div class="item-date">
                        {{ project.start_date|date:"M Y" }}
                        {% if project.end_date %} - {{ project.end_date|date:"M Y" }}{% endif %}
                    </div>
                    {% endif %}
                </div>
                {% if project.description %}
                <div class="item-description">
                    {{ project.description|linebreaks }}
                </div>
                {% endif %}
                {% if project.url %}
                <div class="item-link">
                    <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.certifications.exists %}
    <section class="resume-section">
        <h2 class="section-title">Certifications</h2>
        <div class="section-content">
            {% for certification in resume.certifications.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ certification.name }}</h3>
                    <div class="item-subtitle">{{ certification.issuing_organization }}</div>
                    {% if certification.issue_date %}
                    <div class="item-date">
                        {{ certification.issue_date|date:"M Y" }}
                        {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                    </div>
                    {% endif %}
                </div>
                {% if certification.credential_url %}
                <div class="item-link">
                    <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.languages.exists %}
    <section class="resume-section">
        <h2 class="section-title">Languages</h2>
        <div class="section-content">
            <div class="languages-list">
                {% for language in resume.languages.all %}
                <div class="language-item">
                    <span class="language-name">{{ language.name }}</span>
                    <span class="language-proficiency">{{ language.get_proficiency_display }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}
</div>
            ''',
            'css_styles': '''
/* Simple Clean Template */
.resume.simple-clean {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    color: #333;
    line-height: 1.6;
}

.resume.simple-clean .resume-header {
    text-align: center;
    margin-bottom: 30px;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
}

.resume.simple-clean .full-name {
    font-size: 28px;
    font-weight: bold;
    margin: 0 0 5px;
}

.resume.simple-clean .job-title {
    font-size: 18px;
    color: #666;
    margin: 0 0 15px;
}

.resume.simple-clean .contact-info {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
}

.resume.simple-clean .resume-section {
    margin-bottom: 25px;
}

.resume.simple-clean .section-title {
    font-size: 18px;
    font-weight: bold;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
    margin-bottom: 15px;
}

.resume.simple-clean .item {
    margin-bottom: 20px;
}

.resume.simple-clean .item-title {
    font-size: 16px;
    font-weight: bold;
    margin: 0 0 5px;
}

.resume.simple-clean .item-subtitle {
    font-size: 14px;
    color: #666;
    margin: 0 0 5px;
}

.resume.simple-clean .item-date {
    font-size: 14px;
    color: #888;
    margin-bottom: 10px;
}

.resume.simple-clean .item-description {
    font-size: 14px;
}

.resume.simple-clean .skills-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
}

.resume.simple-clean .skill-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.resume.simple-clean .skill-level {
    display: flex;
    gap: 3px;
}

.resume.simple-clean .skill-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #eee;
}

.resume.simple-clean .skill-dot.active {
    background-color: #333;
}

.resume.simple-clean .languages-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
}

.resume.simple-clean .language-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.resume.simple-clean .language-proficiency {
    color: #666;
    font-size: 14px;
}
            ''',
            'is_premium': False,
            'is_active': True,
            'display_order': 1
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=simple_clean['slug'],
            defaults={
                **simple_clean,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            # This would be a base64 encoded image in a real implementation
            # For simplicity, we're creating a placeholder
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

        # Simple Professional template
        simple_professional = {
            'name': 'Simple Professional',
            'slug': 'simple-professional',
            'description': 'A professional, no-nonsense template that works well in traditional industries.',
            'html_structure': '''
<div class="resume simple-professional">
    <header class="resume-header">
        <div class="header-main">
            <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
            <p class="job-title">{{ resume.personal_info.job_title }}</p>
        </div>
        <div class="contact-info">
            {% if resume.personal_info.email %}<div class="contact-item"><i class="icon-email"></i>{{ resume.personal_info.email }}</div>{% endif %}
            {% if resume.personal_info.phone %}<div class="contact-item"><i class="icon-phone"></i>{{ resume.personal_info.phone }}</div>{% endif %}
            {% if resume.personal_info.address %}<div class="contact-item"><i class="icon-location"></i>{{ resume.personal_info.address }}</div>{% endif %}
            {% if resume.personal_info.linkedin %}<div class="contact-item"><i class="icon-linkedin"></i>{{ resume.personal_info.linkedin }}</div>{% endif %}
        </div>
    </header>

    {% if resume.personal_info.summary %}
    <section class="resume-section">
        <h2 class="section-title">Professional Summary</h2>
        <div class="section-content">
            <p>{{ resume.personal_info.summary }}</p>
        </div>
    </section>
    {% endif %}

    {% if resume.experiences.exists %}
    <section class="resume-section">
        <h2 class="section-title">Work Experience</h2>
        <div class="section-content">
            {% for experience in resume.experiences.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-header-left">
                        <h3 class="item-title">{{ experience.position }}</h3>
                        <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                    </div>
                    <div class="item-header-right">
                        <div class="item-date">
                            {{ experience.start_date|date:"M Y" }} - 
                            {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                        </div>
                    </div>
                </div>
                {% if experience.description %}
                <div class="item-description">
                    {{ experience.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.educations.exists %}
    <section class="resume-section">
        <h2 class="section-title">Education</h2>
        <div class="section-content">
            {% for education in resume.educations.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-header-left">
                        <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                        <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                    </div>
                    <div class="item-header-right">
                        <div class="item-date">
                            {{ education.start_date|date:"M Y" }} - 
                            {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                        </div>
                    </div>
                </div>
                {% if education.description %}
                <div class="item-description">
                    {{ education.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.skills.exists %}
    <section class="resume-section">
        <h2 class="section-title">Skills</h2>
        <div class="section-content">
            <div class="skills-list">
                {% for skill in resume.skills.all %}
                <div class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-bar">
                        <div class="skill-progress" style="width: {{ skill.level|multiply:20 }}%;"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if resume.certifications.exists %}
    <section class="resume-section">
        <h2 class="section-title">Certifications</h2>
        <div class="section-content">
            {% for certification in resume.certifications.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-header-left">
                        <h3 class="item-title">{{ certification.name }}</h3>
                        <div class="item-subtitle">{{ certification.issuing_organization }}</div>
                    </div>
                    <div class="item-header-right">
                        {% if certification.issue_date %}
                        <div class="item-date">
                            {{ certification.issue_date|date:"M Y" }}
                            {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% if certification.credential_url %}
                <div class="item-link">
                    <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.languages.exists %}
    <section class="resume-section">
        <h2 class="section-title">Languages</h2>
        <div class="section-content">
            <div class="languages-list">
                {% for language in resume.languages.all %}
                <div class="language-item">
                    <span class="language-name">{{ language.name }}</span>
                    <span class="language-proficiency">{{ language.get_proficiency_display }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}
</div>
            ''',
            'css_styles': '''
/* Simple Professional Template */
.resume.simple-professional {
    font-family: 'Calibri', 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 30px;
    color: #333;
    line-height: 1.5;
}

.resume.simple-professional .resume-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    border-bottom: 2px solid #2a5885;
    padding-bottom: 20px;
}

.resume.simple-professional .header-main {
    flex: 1;
}

.resume.simple-professional .contact-info {
    text-align: right;
    min-width: 200px;
}

.resume.simple-professional .full-name {
    font-size: 28px;
    font-weight: bold;
    color: #2a5885;
    margin: 0 0 5px;
}

.resume.simple-professional .job-title {
    font-size: 18px;
    color: #555;
    margin: 0;
}

.resume.simple-professional .contact-item {
    margin-bottom: 5px;
    font-size: 14px;
}

.resume.simple-professional .resume-section {
    margin-bottom: 25px;
}

.resume.simple-professional .section-title {
    font-size: 18px;
    font-weight: bold;
    color: #2a5885;
    border-bottom: 1px solid #ddd;
    padding-bottom: 5px;
    margin-bottom: 15px;
}

.resume.simple-professional .item {
    margin-bottom: 20px;
}

.resume.simple-professional .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.resume.simple-professional .item-title {
    font-size: 16px;
    font-weight: bold;
    margin: 0 0 5px;
}

.resume.simple-professional .item-subtitle {
    font-size: 14px;
    color: #555;
    margin: 0;
}

.resume.simple-professional .item-date {
    font-size: 14px;
    color: #777;
    text-align: right;
}

.resume.simple-professional .item-description {
    font-size: 14px;
}

.resume.simple-professional .skills-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
}

.resume.simple-professional .skill-item {
    margin-bottom: 10px;
}

.resume.simple-professional .skill-name {
    display: block;
    margin-bottom: 5px;
    font-size: 14px;
}

.resume.simple-professional .skill-bar {
    height: 8px;
    background-color: #eee;
    border-radius: 4px;
    overflow: hidden;
}

.resume.simple-professional .skill-progress {
    height: 100%;
    background-color: #2a5885;
}

.resume.simple-professional .languages-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
}

.resume.simple-professional .language-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.resume.simple-professional .language-proficiency {
    color: #555;
    font-size: 14px;
}

/* Icons */
.resume.simple-professional .icon-email:before {
    content: "✉ ";
}

.resume.simple-professional .icon-phone:before {
    content: "☎ ";
}

.resume.simple-professional .icon-location:before {
    content: "📍 ";
}

.resume.simple-professional .icon-linkedin:before {
    content: "🔗 ";
}
            ''',
            'is_premium': False,
            'is_active': True,
            'display_order': 2
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=simple_professional['slug'],
            defaults={
                **simple_professional,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

    def _create_modern_templates(self):
        category = TemplateCategory.objects.get(slug='modern')

        # Modern Sleek template
        modern_sleek = {
            'name': 'Modern Sleek',
            'slug': 'modern-sleek',
            'description': 'A sleek, modern design with a clean layout and subtle color accents.',
            'html_structure': '''
<div class="resume modern-sleek">
    <div class="sidebar">
        {% if resume.personal_info.profile_image %}
        <div class="profile-image">
            <img src="{{ resume.personal_info.profile_image.url }}" alt="{{ resume.personal_info.full_name }}">
        </div>
        {% endif %}

        <div class="sidebar-section contact-info">
            <h2 class="sidebar-title">Contact</h2>
            <ul class="contact-list">
                {% if resume.personal_info.email %}
                <li class="contact-item">
                    <span class="contact-icon">✉</span>
                    <span class="contact-text">{{ resume.personal_info.email }}</span>
                </li>
                {% endif %}
                {% if resume.personal_info.phone %}
                <li class="contact-item">
                    <span class="contact-icon">☎</span>
                    <span class="contact-text">{{ resume.personal_info.phone }}</span>
                </li>
                {% endif %}
                {% if resume.personal_info.address %}
                <li class="contact-item">
                    <span class="contact-icon">📍</span>
                    <span class="contact-text">{{ resume.personal_info.address }}</span>
                </li>
                {% endif %}
                {% if resume.personal_info.website %}
                <li class="contact-item">
                    <span class="contact-icon">🌐</span>
                    <span class="contact-text">{{ resume.personal_info.website }}</span>
                </li>
                {% endif %}
                {% if resume.personal_info.linkedin %}
                <li class="contact-item">
                    <span class="contact-icon">🔗</span>
                    <span class="contact-text">{{ resume.personal_info.linkedin }}</span>
                </li>
                {% endif %}
            </ul>
        </div>

        {% if resume.skills.exists %}
        <div class="sidebar-section skills">
            <h2 class="sidebar-title">Skills</h2>
            <div class="skills-list">
                {% for skill in resume.skills.all %}
                <div class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-bar">
                        <div class="skill-progress" style="width: {{ skill.level|multiply:20 }}%;"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        {% if resume.languages.exists %}
        <div class="sidebar-section languages">
            <h2 class="sidebar-title">Languages</h2>
            <div class="languages-list">
                {% for language in resume.languages.all %}
                <div class="language-item">
                    <span class="language-name">{{ language.name }}</span>
                    <span class="language-proficiency">{{ language.get_proficiency_display }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>

    <div class="main-content">
        <header class="resume-header">
            <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
            <p class="job-title">{{ resume.personal_info.job_title }}</p>
        </header>

        {% if resume.personal_info.summary %}
        <section class="resume-section">
            <h2 class="section-title">Profile</h2>
            <div class="section-content">
                <p>{{ resume.personal_info.summary }}</p>
            </div>
        </section>
        {% endif %}

        {% if resume.experiences.exists %}
        <section class="resume-section">
            <h2 class="section-title">Experience</h2>
            <div class="section-content">
                {% for experience in resume.experiences.all %}
                <div class="item">
                    <div class="item-header">
                        <div class="item-header-left">
                            <h3 class="item-title">{{ experience.position }}</h3>
                            <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                        </div>
                        <div class="item-header-right">
                            <div class="item-date">
                                {{ experience.start_date|date:"M Y" }} - 
                                {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                            </div>
                        </div>
                    </div>
                    {% if experience.description %}
                    <div class="item-description">
                        {{ experience.description|linebreaks }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.educations.exists %}
        <section class="resume-section">
            <h2 class="section-title">Education</h2>
            <div class="section-content">
                {% for education in resume.educations.all %}
                <div class="item">
                    <div class="item-header">
                        <div class="item-header-left">
                            <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                            <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                        </div>
                        <div class="item-header-right">
                            <div class="item-date">
                                {{ education.start_date|date:"M Y" }} - 
                                {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                            </div>
                        </div>
                    </div>
                    {% if education.description %}
                    <div class="item-description">
                        {{ education.description|linebreaks }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.projects.exists %}
        <section class="resume-section">
            <h2 class="section-title">Projects</h2>
            <div class="section-content">
                {% for project in resume.projects.all %}
                <div class="item">
                    <div class="item-header">
                        <div class="item-header-left">
                            <h3 class="item-title">{{ project.title }}</h3>
                        </div>
                        <div class="item-header-right">
                            {% if project.start_date %}
                            <div class="item-date">
                                {{ project.start_date|date:"M Y" }}
                                {% if project.end_date %} - {{ project.end_date|date:"M Y" }}{% endif %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    {% if project.description %}
                    <div class="item-description">
                        {{ project.description|linebreaks }}
                    </div>
                    {% endif %}
                    {% if project.url %}
                    <div class="item-link">
                        <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.certifications.exists %}
        <section class="resume-section">
            <h2 class="section-title">Certifications</h2>
            <div class="section-content">
                {% for certification in resume.certifications.all %}
                <div class="item">
                    <div class="item-header">
                        <div class="item-header-left">
                            <h3 class="item-title">{{ certification.name }}</h3>
                            <div class="item-subtitle">{{ certification.issuing_organization }}</div>
                        </div>
                        <div class="item-header-right">
                            {% if certification.issue_date %}
                            <div class="item-date">
                                {{ certification.issue_date|date:"M Y" }}
                                {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    {% if certification.credential_url %}
                    <div class="item-link">
                        <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}
    </div>
</div>
            ''',
            'css_styles': '''
/* Modern Sleek Template */
.resume.modern-sleek {
    font-family: 'Roboto', 'Arial', sans-serif;
    display: flex;
    max-width: 1000px;
    margin: 0 auto;
    color: #333;
    line-height: 1.6;
    background-color: #fff;
}

.resume.modern-sleek .sidebar {
    width: 30%;
    background-color: #f8f9fa;
    padding: 30px;
}

.resume.modern-sleek .main-content {
    width: 70%;
    padding: 30px;
}

.resume.modern-sleek .profile-image {
    text-align: center;
    margin-bottom: 20px;
}

.resume.modern-sleek .profile-image img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #fff;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.resume.modern-sleek .sidebar-section {
    margin-bottom: 30px;
}

.resume.modern-sleek .sidebar-title {
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 15px;
    color: #3498db;
    border-bottom: 2px solid #3498db;
    padding-bottom: 5px;
}

.resume.modern-sleek .contact-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.resume.modern-sleek .contact-item {
    display: flex;
    margin-bottom: 10px;
    align-items: flex-start;
}

.resume.modern-sleek .contact-icon {
    margin-right: 10px;
    color: #3498db;
    font-size: 16px;
    min-width: 20px;
    text-align: center;
}

.resume.modern-sleek .contact-text {
    font-size: 14px;
    word-break: break-word;
}

.resume.modern-sleek .skill-item {
    margin-bottom: 15px;
}

.resume.modern-sleek .skill-name {
    display: block;
    margin-bottom: 5px;
    font-size: 14px;
}

.resume.modern-sleek .skill-bar {
    height: 6px;
    background-color: #e9ecef;
    border-radius: 3px;
    overflow: hidden;
}

.resume.modern-sleek .skill-progress {
    height: 100%;
    background-color: #3498db;
}

.resume.modern-sleek .language-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.resume.modern-sleek .language-proficiency {
    color: #6c757d;
    font-size: 14px;
}

.resume.modern-sleek .resume-header {
    margin-bottom: 30px;
}

.resume.modern-sleek .full-name {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 5px;
    color: #3498db;
}

.resume.modern-sleek .job-title {
    font-size: 18px;
    color: #6c757d;
    margin: 0;
}

.resume.modern-sleek .resume-section {
    margin-bottom: 30px;
}

.resume.modern-sleek .section-title {
    font-size: 20px;
    font-weight: 500;
    color: #3498db;
    margin-bottom: 15px;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 5px;
}

.resume.modern-sleek .item {
    margin-bottom: 20px;
}

.resume.modern-sleek .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.resume.modern-sleek .item-title {
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 5px;
    color: #333;
}

.resume.modern-sleek .item-subtitle {
    font-size: 14px;
    color: #6c757d;
}

.resume.modern-sleek .item-date {
    font-size: 14px;
    color: #6c757d;
    text-align: right;
}

.resume.modern-sleek .item-description {
    font-size: 14px;
}

.resume.modern-sleek .item-link a {
    color: #3498db;
    text-decoration: none;
}

.resume.modern-sleek .item-link a:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .resume.modern-sleek {
        flex-direction: column;
    }

    .resume.modern-sleek .sidebar,
    .resume.modern-sleek .main-content {
        width: 100%;
    }
}
            ''',
            'is_premium': True,
            'is_active': True,
            'display_order': 1
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=modern_sleek['slug'],
            defaults={
                **modern_sleek,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

        # Modern Minimal template
        modern_minimal = {
            'name': 'Modern Minimal',
            'slug': 'modern-minimal',
            'description': 'A minimalist design with a focus on typography and whitespace.',
            'html_structure': '''
<div class="resume modern-minimal">
    <header class="resume-header">
        <div class="header-content">
            <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
            <p class="job-title">{{ resume.personal_info.job_title }}</p>

            <div class="contact-info">
                {% if resume.personal_info.email %}<span class="contact-item">{{ resume.personal_info.email }}</span>{% endif %}
                {% if resume.personal_info.phone %}<span class="contact-item">{{ resume.personal_info.phone }}</span>{% endif %}
                {% if resume.personal_info.address %}<span class="contact-item">{{ resume.personal_info.address }}</span>{% endif %}
                {% if resume.personal_info.website %}<span class="contact-item">{{ resume.personal_info.website }}</span>{% endif %}
            </div>
        </div>
    </header>

    <main class="resume-content">
        {% if resume.personal_info.summary %}
        <section class="resume-section">
            <h2 class="section-title">About Me</h2>
            <div class="section-content">
                <p>{{ resume.personal_info.summary }}</p>
            </div>
        </section>
        {% endif %}

        {% if resume.experiences.exists %}
        <section class="resume-section">
            <h2 class="section-title">Experience</h2>
            <div class="section-content">
                {% for experience in resume.experiences.all %}
                <div class="item">
                    <div class="item-header">
                        <h3 class="item-title">{{ experience.position }}</h3>
                        <span class="item-date">
                            {{ experience.start_date|date:"M Y" }} - 
                            {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                        </span>
                    </div>
                    <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                    {% if experience.description %}
                    <div class="item-description">
                        {{ experience.description|linebreaks }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.educations.exists %}
        <section class="resume-section">
            <h2 class="section-title">Education</h2>
            <div class="section-content">
                {% for education in resume.educations.all %}
                <div class="item">
                    <div class="item-header">
                        <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                        <span class="item-date">
                            {{ education.start_date|date:"M Y" }} - 
                            {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                        </span>
                    </div>
                    <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                    {% if education.description %}
                    <div class="item-description">
                        {{ education.description|linebreaks }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        <div class="two-column-section">
            {% if resume.skills.exists %}
            <section class="resume-section">
                <h2 class="section-title">Skills</h2>
                <div class="section-content">
                    <ul class="skills-list">
                        {% for skill in resume.skills.all %}
                        <li class="skill-item">
                            <span class="skill-name">{{ skill.name }}</span>
                            <div class="skill-level">
                                {% for i in "12345" %}
                                    {% if forloop.counter <= skill.level %}
                                    <span class="skill-dot active"></span>
                                    {% else %}
                                    <span class="skill-dot"></span>
                                    {% endif %}
                                {% endfor %}
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </section>
            {% endif %}

            {% if resume.languages.exists %}
            <section class="resume-section">
                <h2 class="section-title">Languages</h2>
                <div class="section-content">
                    <ul class="languages-list">
                        {% for language in resume.languages.all %}
                        <li class="language-item">
                            <span class="language-name">{{ language.name }}</span>
                            <span class="language-proficiency">{{ language.get_proficiency_display }}</span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </section>
            {% endif %}
        </div>

        {% if resume.projects.exists %}
        <section class="resume-section">
            <h2 class="section-title">Projects</h2>
            <div class="section-content">
                {% for project in resume.projects.all %}
                <div class="item">
                    <div class="item-header">
                        <h3 class="item-title">{{ project.title }}</h3>
                        {% if project.start_date %}
                        <span class="item-date">
                            {{ project.start_date|date:"M Y" }}
                            {% if project.end_date %} - {{ project.end_date|date:"M Y" }}{% endif %}
                        </span>
                        {% endif %}
                    </div>
                    {% if project.description %}
                    <div class="item-description">
                        {{ project.description|linebreaks }}
                    </div>
                    {% endif %}
                    {% if project.url %}
                    <div class="item-link">
                        <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.certifications.exists %}
        <section class="resume-section">
            <h2 class="section-title">Certifications</h2>
            <div class="section-content">
                {% for certification in resume.certifications.all %}
                <div class="item">
                    <div class="item-header">
                        <h3 class="item-title">{{ certification.name }}</h3>
                        {% if certification.issue_date %}
                        <span class="item-date">
                            {{ certification.issue_date|date:"M Y" }}
                            {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                        </span>
                        {% endif %}
                    </div>
                    <div class="item-subtitle">{{ certification.issuing_organization }}</div>
                    {% if certification.credential_url %}
                    <div class="item-link">
                        <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}
    </main>
</div>
            ''',
            'css_styles': '''
/* Modern Minimal Template */
.resume.modern-minimal {
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    color: #333;
    line-height: 1.6;
    background-color: #fff;
}

.resume.modern-minimal .resume-header {
    margin-bottom: 40px;
    border-bottom: 1px solid #eee;
    padding-bottom: 30px;
}

.resume.modern-minimal .full-name {
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0 0 5px;
    color: #000;
}

.resume.modern-minimal .job-title {
    font-size: 18px;
    color: #666;
    margin: 0 0 20px;
    font-weight: 400;
}

.resume.modern-minimal .contact-info {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    font-size: 14px;
    color: #666;
}

.resume.modern-minimal .contact-item:not(:last-child)::after {
    content: "•";
    margin-left: 15px;
}

.resume.modern-minimal .resume-section {
    margin-bottom: 35px;
}

.resume.modern-minimal .section-title {
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
    color: #000;
    position: relative;
}

.resume.modern-minimal .section-title::after {
    content: "";
    display: block;
    width: 30px;
    height: 2px;
    background-color: #000;
    margin-top: 5px;
}

.resume.modern-minimal .item {
    margin-bottom: 25px;
}

.resume.modern-minimal .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    align-items: baseline;
}

.resume.modern-minimal .item-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: #000;
}

.resume.modern-minimal .item-date {
    font-size: 14px;
    color: #666;
}

.resume.modern-minimal .item-subtitle {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
}

.resume.modern-minimal .item-description {
    font-size: 14px;
    color: #333;
}

.resume.modern-minimal .two-column-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 35px;
}

.resume.modern-minimal .skills-list,
.resume.modern-minimal .languages-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.resume.modern-minimal .skill-item,
.resume.modern-minimal .language-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    align-items: center;
}

.resume.modern-minimal .skill-level {
    display: flex;
    gap: 3px;
}

.resume.modern-minimal .skill-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #eee;
}

.resume.modern-minimal .skill-dot.active {
    background-color: #000;
}

.resume.modern-minimal .language-proficiency {
    font-size: 12px;
    color: #666;
}

.resume.modern-minimal .item-link a {
    color: #000;
    text-decoration: none;
    border-bottom: 1px solid #000;
    padding-bottom: 1px;
    transition: border-color 0.3s;
}

.resume.modern-minimal .item-link a:hover {
    border-color: transparent;
}

@media (max-width: 768px) {
    .resume.modern-minimal .two-column-section {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .resume.modern-minimal .item-header {
        flex-direction: column;
    }

    .resume.modern-minimal .item-date {
        margin-top: 5px;
    }
}
            ''',
            'is_premium': True,
            'is_active': True,
            'display_order': 2
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=modern_minimal['slug'],
            defaults={
                **modern_minimal,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

    def _create_classical_templates(self):
        category = TemplateCategory.objects.get(slug='classical')

        # Classical Elegant template
        classical_elegant = {
            'name': 'Classical Elegant',
            'slug': 'classical-elegant',
            'description': 'A timeless, elegant design with traditional formatting.',
            'html_structure': '''
<div class="resume classical-elegant">
    <header class="resume-header">
        <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
        <p class="job-title">{{ resume.personal_info.job_title }}</p>

        <div class="contact-info">
            {% if resume.personal_info.email %}<div class="contact-item"><i class="icon-email"></i>{{ resume.personal_info.email }}</div>{% endif %}
            {% if resume.personal_info.phone %}<div class="contact-item"><i class="icon-phone"></i>{{ resume.personal_info.phone }}</div>{% endif %}
            {% if resume.personal_info.address %}<div class="contact-item"><i class="icon-location"></i>{{ resume.personal_info.address }}</div>{% endif %}
            {% if resume.personal_info.linkedin %}<div class="contact-item"><i class="icon-linkedin"></i>{{ resume.personal_info.linkedin }}</div>{% endif %}
            {% if resume.personal_info.website %}<div class="contact-item"><i class="icon-website"></i>{{ resume.personal_info.website }}</div>{% endif %}
        </div>
    </header>

    {% if resume.personal_info.summary %}
    <section class="resume-section">
        <h2 class="section-title">Professional Summary</h2>
        <div class="section-content">
            <p>{{ resume.personal_info.summary }}</p>
        </div>
    </section>
    {% endif %}

    {% if resume.experiences.exists %}
    <section class="resume-section">
        <h2 class="section-title">Professional Experience</h2>
        <div class="section-content">
            {% for experience in resume.experiences.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-title-group">
                        <h3 class="item-title">{{ experience.position }}</h3>
                        <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                    </div>
                    <div class="item-date">
                        {{ experience.start_date|date:"F Y" }} - 
                        {% if experience.current %}Present{% else %}{{ experience.end_date|date:"F Y" }}{% endif %}
                    </div>
                </div>
                {% if experience.description %}
                <div class="item-description">
                    {{ experience.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.educations.exists %}
    <section class="resume-section">
        <h2 class="section-title">Education</h2>
        <div class="section-content">
            {% for education in resume.educations.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-title-group">
                        <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                        <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                    </div>
                    <div class="item-date">
                        {{ education.start_date|date:"F Y" }} - 
                        {% if education.current %}Present{% else %}{{ education.end_date|date:"F Y" }}{% endif %}
                    </div>
                </div>
                {% if education.description %}
                <div class="item-description">
                    {{ education.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.skills.exists %}
    <section class="resume-section">
        <h2 class="section-title">Skills</h2>
        <div class="section-content">
            <div class="skills-list">
                {% for skill in resume.skills.all %}
                <div class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-rating">
                        {% for i in "12345" %}
                            {% if forloop.counter <= skill.level %}
                            <span class="skill-star filled">★</span>
                            {% else %}
                            <span class="skill-star">☆</span>
                            {% endif %}
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if resume.certifications.exists %}
    <section class="resume-section">
        <h2 class="section-title">Certifications</h2>
        <div class="section-content">
            {% for certification in resume.certifications.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-title-group">
                        <h3 class="item-title">{{ certification.name }}</h3>
                        <div class="item-subtitle">{{ certification.issuing_organization }}</div>
                    </div>
                    {% if certification.issue_date %}
                    <div class="item-date">
                        {{ certification.issue_date|date:"F Y" }}
                        {% if certification.expiration_date %} - {{ certification.expiration_date|date:"F Y" }}{% endif %}
                    </div>
                    {% endif %}
                </div>
                {% if certification.credential_url %}
                <div class="item-link">
                    <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.languages.exists %}
    <section class="resume-section">
        <h2 class="section-title">Languages</h2>
        <div class="section-content">
            <div class="languages-list">
                {% for language in resume.languages.all %}
                <div class="language-item">
                    <span class="language-name">{{ language.name }}</span>
                    <span class="language-proficiency">{{ language.get_proficiency_display }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if resume.projects.exists %}
    <section class="resume-section">
        <h2 class="section-title">Projects</h2>
        <div class="section-content">
            {% for project in resume.projects.all %}
            <div class="item">
                <div class="item-header">
                    <div class="item-title-group">
                        <h3 class="item-title">{{ project.title }}</h3>
                    </div>
                    {% if project.start_date %}
                    <div class="item-date">
                        {{ project.start_date|date:"F Y" }}
                        {% if project.end_date %} - {{ project.end_date|date:"F Y" }}{% endif %}
                    </div>
                    {% endif %}
                </div>
                {% if project.description %}
                <div class="item-description">
                    {{ project.description|linebreaks }}
                </div>
                {% endif %}
                {% if project.url %}
                <div class="item-link">
                    <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
</div>
            ''',
            'css_styles': '''
/* Classical Elegant Template */
.resume.classical-elegant {
    font-family: 'Times New Roman', Times, serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    color: #333;
    line-height: 1.6;
    background-color: #fff;
}

.resume.classical-elegant .resume-header {
    text-align: center;
    margin-bottom: 30px;
    border-bottom: 2px solid #333;
    padding-bottom: 20px;
}

.resume.classical-elegant .full-name {
    font-size: 28px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0 0 5px;
}

.resume.classical-elegant .job-title {
    font-size: 18px;
    font-style: italic;
    margin: 0 0 15px;
}

.resume.classical-elegant .contact-info {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
    font-size: 14px;
}

.resume.classical-elegant .contact-item {
    display: flex;
    align-items: center;
}

.resume.classical-elegant .resume-section {
    margin-bottom: 25px;
}

.resume.classical-elegant .section-title {
    font-size: 18px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid #333;
    padding-bottom: 5px;
    margin-bottom: 15px;
}

.resume.classical-elegant .item {
    margin-bottom: 20px;
}

.resume.classical-elegant .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.resume.classical-elegant .item-title {
    font-size: 16px;
    font-weight: bold;
    margin: 0 0 5px;
}

.resume.classical-elegant .item-subtitle {
    font-size: 14px;
    font-style: italic;
}

.resume.classical-elegant .item-date {
    font-size: 14px;
    text-align: right;
    min-width: 150px;
}

.resume.classical-elegant .item-description {
    font-size: 14px;
    text-align: justify;
}

.resume.classical-elegant .skills-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
}

.resume.classical-elegant .skill-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.resume.classical-elegant .skill-rating {
    display: flex;
    gap: 2px;
}

.resume.classical-elegant .skill-star {
    color: #ccc;
    font-size: 14px;
}

.resume.classical-elegant .skill-star.filled {
    color: #333;
}

.resume.classical-elegant .languages-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
}

.resume.classical-elegant .language-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.resume.classical-elegant .language-proficiency {
    font-style: italic;
    font-size: 14px;
}

.resume.classical-elegant .item-link a {
    color: #333;
    text-decoration: none;
    border-bottom: 1px dotted #333;
}

.resume.classical-elegant .item-link a:hover {
    border-bottom: 1px solid #333;
}

/* Icons */
.resume.classical-elegant .icon-email:before {
    content: "Email: ";
    font-weight: bold;
}

.resume.classical-elegant .icon-phone:before {
    content: "Phone: ";
    font-weight: bold;
}

.resume.classical-elegant .icon-location:before {
    content: "Address: ";
    font-weight: bold;
}

.resume.classical-elegant .icon-linkedin:before {
    content: "LinkedIn: ";
    font-weight: bold;
}

.resume.classical-elegant .icon-website:before {
    content: "Website: ";
    font-weight: bold;
}

@media (max-width: 768px) {
    .resume.classical-elegant .item-header {
        flex-direction: column;
    }

    .resume.classical-elegant .item-date {
        text-align: left;
        margin-top: 5px;
    }
}
            ''',
            'is_premium': False,
            'is_active': True,
            'display_order': 1
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=classical_elegant['slug'],
            defaults={
                **classical_elegant,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

        # Classical Traditional template
        classical_traditional = {
            'name': 'Classical Traditional',
            'slug': 'classical-traditional',
            'description': 'A traditional resume format that is widely accepted across industries.',
            'html_structure': '''
<div class="resume classical-traditional">
    <header class="resume-header">
        <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>

        <div class="contact-info">
            {% if resume.personal_info.address %}<div class="contact-item">{{ resume.personal_info.address }}</div>{% endif %}
            {% if resume.personal_info.phone %}<div class="contact-item">{{ resume.personal_info.phone }}</div>{% endif %}
            {% if resume.personal_info.email %}<div class="contact-item">{{ resume.personal_info.email }}</div>{% endif %}
            {% if resume.personal_info.linkedin %}<div class="contact-item">{{ resume.personal_info.linkedin }}</div>{% endif %}
        </div>
    </header>

    {% if resume.personal_info.job_title or resume.personal_info.summary %}
    <section class="resume-section">
        <h2 class="section-title">Objective</h2>
        <div class="section-content">
            {% if resume.personal_info.job_title %}<p class="objective-title">{{ resume.personal_info.job_title }}</p>{% endif %}
            {% if resume.personal_info.summary %}<p>{{ resume.personal_info.summary }}</p>{% endif %}
        </div>
    </section>
    {% endif %}

    {% if resume.experiences.exists %}
    <section class="resume-section">
        <h2 class="section-title">Experience</h2>
        <div class="section-content">
            {% for experience in resume.experiences.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ experience.company }}</h3>
                    <div class="item-date">
                        {{ experience.start_date|date:"m/Y" }} - 
                        {% if experience.current %}Present{% else %}{{ experience.end_date|date:"m/Y" }}{% endif %}
                    </div>
                </div>
                <div class="item-subtitle">{{ experience.position }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                {% if experience.description %}
                <div class="item-description">
                    {{ experience.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.educations.exists %}
    <section class="resume-section">
        <h2 class="section-title">Education</h2>
        <div class="section-content">
            {% for education in resume.educations.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ education.institution }}</h3>
                    <div class="item-date">
                        {{ education.start_date|date:"m/Y" }} - 
                        {% if education.current %}Present{% else %}{{ education.end_date|date:"m/Y" }}{% endif %}
                    </div>
                </div>
                <div class="item-subtitle">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}{% if education.location %} | {{ education.location }}{% endif %}</div>
                {% if education.description %}
                <div class="item-description">
                    {{ education.description|linebreaks }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if resume.skills.exists %}
    <section class="resume-section">
        <h2 class="section-title">Skills</h2>
        <div class="section-content">
            <ul class="skills-list">
                {% for skill in resume.skills.all %}
                <li class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    {% if skill.level > 0 %}
                    <span class="skill-level">({{ skill.get_level_display }})</span>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>
    {% endif %}

    {% if resume.certifications.exists %}
    <section class="resume-section">
        <h2 class="section-title">Certifications</h2>
        <div class="section-content">
            <ul class="certifications-list">
                {% for certification in resume.certifications.all %}
                <li class="certification-item">
                    <span class="certification-name">{{ certification.name }}</span>
                    <span class="certification-org">{{ certification.issuing_organization }}</span>
                    {% if certification.issue_date %}
                    <span class="certification-date">
                        {{ certification.issue_date|date:"m/Y" }}
                        {% if certification.expiration_date %} - {{ certification.expiration_date|date:"m/Y" }}{% endif %}
                    </span>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>
    {% endif %}

    {% if resume.languages.exists %}
    <section class="resume-section">
        <h2 class="section-title">Languages</h2>
        <div class="section-content">
            <ul class="languages-list">
                {% for language in resume.languages.all %}
                <li class="language-item">
                    <span class="language-name">{{ language.name }}</span>
                    <span class="language-proficiency">({{ language.get_proficiency_display }})</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>
    {% endif %}

    {% if resume.projects.exists %}
    <section class="resume-section">
        <h2 class="section-title">Projects</h2>
        <div class="section-content">
            {% for project in resume.projects.all %}
            <div class="item">
                <div class="item-header">
                    <h3 class="item-title">{{ project.title }}</h3>
                    {% if project.start_date %}
                    <div class="item-date">
                        {{ project.start_date|date:"m/Y" }}
                        {% if project.end_date %} - {{ project.end_date|date:"m/Y" }}{% endif %}
                    </div>
                    {% endif %}
                </div>
                {% if project.description %}
                <div class="item-description">
                    {{ project.description|linebreaks }}
                </div>
                {% endif %}
                {% if project.url %}
                <div class="item-link">
                    <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}
</div>
            ''',
            'css_styles': '''
/* Classical Traditional Template */
.resume.classical-traditional {
    font-family: 'Times New Roman', Times, serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 30px;
    color: #000;
    line-height: 1.5;
    background-color: #fff;
}

.resume.classical-traditional .resume-header {
    text-align: center;
    margin-bottom: 20px;
}

.resume.classical-traditional .full-name {
    font-size: 24px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0 0 10px;
}

.resume.classical-traditional .contact-info {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
    font-size: 14px;
}

.resume.classical-traditional .contact-item:not(:last-child)::after {
    content: "•";
    margin-left: 15px;
}

.resume.classical-traditional .resume-section {
    margin-bottom: 20px;
}

.resume.classical-traditional .section-title {
    font-size: 16px;
    font-weight: bold;
    text-transform: uppercase;
    border-bottom: 1px solid #000;
    padding-bottom: 3px;
    margin-bottom: 10px;
}

.resume.classical-traditional .item {
    margin-bottom: 15px;
}

.resume.classical-traditional .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.resume.classical-traditional .item-title {
    font-size: 15px;
    font-weight: bold;
    margin: 0;
}

.resume.classical-traditional .item-subtitle {
    font-size: 14px;
    font-style: italic;
    margin-bottom: 5px;
}

.resume.classical-traditional .item-date {
    font-size: 14px;
}

.resume.classical-traditional .item-description {
    font-size: 14px;
}

.resume.classical-traditional .objective-title {
    font-weight: bold;
    margin-bottom: 5px;
}

.resume.classical-traditional .skills-list,
.resume.classical-traditional .languages-list,
.resume.classical-traditional .certifications-list {
    list-style-type: none;
    padding-left: 0;
    margin: 0;
    columns: 2;
}

.resume.classical-traditional .skill-item,
.resume.classical-traditional .language-item,
.resume.classical-traditional .certification-item {
    margin-bottom: 5px;
    break-inside: avoid;
}

.resume.classical-traditional .skill-level,
.resume.classical-traditional .language-proficiency {
    font-style: italic;
}

.resume.classical-traditional .certification-org {
    font-style: italic;
    margin-left: 5px;
}

.resume.classical-traditional .certification-date {
    display: block;
    font-size: 12px;
    color: #666;
}

.resume.classical-traditional .item-link a {
    color: #000;
    text-decoration: none;
}

.resume.classical-traditional .item-link a:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .resume.classical-traditional .skills-list,
    .resume.classical-traditional .languages-list,
    .resume.classical-traditional .certifications-list {
        columns: 1;
    }

    .resume.classical-traditional .item-header {
        flex-direction: column;
    }

    .resume.classical-traditional .item-date {
        margin-top: 3px;
    }
}
            ''',
            'is_premium': False,
            'is_active': True,
            'display_order': 2
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=classical_traditional['slug'],
            defaults={
                **classical_traditional,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

    def _create_creative_templates(self):
        category = TemplateCategory.objects.get(slug='creative')

        # Creative Bold template
        creative_bold = {
            'name': 'Creative Bold',
            'slug': 'creative-bold',
            'description': 'A bold, eye-catching design for creative professionals.',
            'html_structure': '''
<div class="resume creative-bold">
    <div class="header-section">
        <div class="header-content">
            <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
            <p class="job-title">{{ resume.personal_info.job_title }}</p>

            {% if resume.personal_info.summary %}
            <div class="summary">
                <p>{{ resume.personal_info.summary }}</p>
            </div>
            {% endif %}
        </div>

        <div class="contact-section">
            <div class="contact-container">
                {% if resume.personal_info.email %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-email"></i></div>
                    <div class="contact-text">{{ resume.personal_info.email }}</div>
                </div>
                {% endif %}

                {% if resume.personal_info.phone %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-phone"></i></div>
                    <div class="contact-text">{{ resume.personal_info.phone }}</div>
                </div>
                {% endif %}

                {% if resume.personal_info.address %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-location"></i></div>
                    <div class="contact-text">{{ resume.personal_info.address }}</div>
                </div>
                {% endif %}

                {% if resume.personal_info.website %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-website"></i></div>
                    <div class="contact-text">{{ resume.personal_info.website }}</div>
                </div>
                {% endif %}

                {% if resume.personal_info.linkedin %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-linkedin"></i></div>
                    <div class="contact-text">{{ resume.personal_info.linkedin }}</div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <div class="main-content">
        <div class="left-column">
            {% if resume.experiences.exists %}
            <section class="resume-section">
                <h2 class="section-title">Experience</h2>
                <div class="section-content">
                    {% for experience in resume.experiences.all %}
                    <div class="item">
                        <div class="item-header">
                            <h3 class="item-title">{{ experience.position }}</h3>
                            <div class="item-subtitle">{{ experience.company }}</div>
                            <div class="item-meta">
                                {% if experience.location %}<span class="item-location">{{ experience.location }}</span>{% endif %}
                                <span class="item-date">
                                    {{ experience.start_date|date:"M Y" }} - 
                                    {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                                </span>
                            </div>
                        </div>
                        {% if experience.description %}
                        <div class="item-description">
                            {{ experience.description|linebreaks }}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}

            {% if resume.educations.exists %}
            <section class="resume-section">
                <h2 class="section-title">Education</h2>
                <div class="section-content">
                    {% for education in resume.educations.all %}
                    <div class="item">
                        <div class="item-header">
                            <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                            <div class="item-subtitle">{{ education.institution }}</div>
                            <div class="item-meta">
                                {% if education.location %}<span class="item-location">{{ education.location }}</span>{% endif %}
                                <span class="item-date">
                                    {{ education.start_date|date:"M Y" }} - 
                                    {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                                </span>
                            </div>
                        </div>
                        {% if education.description %}
                        <div class="item-description">
                            {{ education.description|linebreaks }}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}

            {% if resume.projects.exists %}
            <section class="resume-section">
                <h2 class="section-title">Projects</h2>
                <div class="section-content">
                    {% for project in resume.projects.all %}
                    <div class="item">
                        <div class="item-header">
                            <h3 class="item-title">{{ project.title }}</h3>
                            {% if project.start_date %}
                            <div class="item-meta">
                                <span class="item-date">
                                    {{ project.start_date|date:"M Y" }}
                                    {% if project.end_date %} - {{ project.end_date|date:"M Y" }}{% endif %}
                                </span>
                            </div>
                            {% endif %}
                        </div>
                        {% if project.description %}
                        <div class="item-description">
                            {{ project.description|linebreaks }}
                        </div>
                        {% endif %}
                        {% if project.url %}
                        <div class="item-link">
                            <a href="{{ project.url }}" target="_blank">{{ project.url }}</a>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}
        </div>

        <div class="right-column">
            {% if resume.skills.exists %}
            <section class="resume-section">
                <h2 class="section-title">Skills</h2>
                <div class="section-content">
                    <div class="skills-list">
                        {% for skill in resume.skills.all %}
                        <div class="skill-item">
                            <div class="skill-name">{{ skill.name }}</div>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: {{ skill.level|multiply:20 }}%;"></div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </section>
            {% endif %}

            {% if resume.languages.exists %}
            <section class="resume-section">
                <h2 class="section-title">Languages</h2>
                <div class="section-content">
                    <div class="languages-list">
                        {% for language in resume.languages.all %}
                        <div class="language-item">
                            <div class="language-name">{{ language.name }}</div>
                            <div class="language-proficiency">{{ language.get_proficiency_display }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </section>
            {% endif %}

            {% if resume.certifications.exists %}
            <section class="resume-section">
                <h2 class="section-title">Certifications</h2>
                <div class="section-content">
                    {% for certification in resume.certifications.all %}
                    <div class="certification-item">
                        <div class="certification-name">{{ certification.name }}</div>
                        <div class="certification-org">{{ certification.issuing_organization }}</div>
                        {% if certification.issue_date %}
                        <div class="certification-date">
                            {{ certification.issue_date|date:"M Y" }}
                            {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                        </div>
                        {% endif %}
                        {% if certification.credential_url %}
                        <div class="certification-link">
                            <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}
        </div>
    </div>
</div>
            ''',
            'css_styles': '''
/* Creative Bold Template */
.resume.creative-bold {
    font-family: 'Montserrat', 'Helvetica Neue', sans-serif;
    max-width: 1000px;
    margin: 0 auto;
    color: #333;
    line-height: 1.6;
    background-color: #fff;
}

.resume.creative-bold .header-section {
    display: flex;
    background-color: #ff5722;
    color: white;
    padding: 40px;
}

.resume.creative-bold .header-content {
    flex: 2;
    padding-right: 40px;
}

.resume.creative-bold .contact-section {
    flex: 1;
    background-color: rgba(0, 0, 0, 0.1);
    padding: 20px;
    border-radius: 5px;
}

.resume.creative-bold .full-name {
    font-size: 36px;
    font-weight: 700;
    margin: 0 0 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.resume.creative-bold .job-title {
    font-size: 18px;
    font-weight: 400;
    margin: 0 0 20px;
    opacity: 0.9;
}

.resume.creative-bold .summary {
    font-size: 14px;
    line-height: 1.6;
    opacity: 0.9;
}

.resume.creative-bold .contact-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.resume.creative-bold .contact-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.resume.creative-bold .contact-icon {
    width: 30px;
    height: 30px;
    background-color: white;
    color: #ff5722;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.resume.creative-bold .contact-text {
    font-size: 14px;
    word-break: break-word;
}

.resume.creative-bold .main-content {
    display: flex;
    padding: 40px;
    gap: 40px;
}

.resume.creative-bold .left-column {
    flex: 2;
}

.resume.creative-bold .right-column {
    flex: 1;
}

.resume.creative-bold .resume-section {
    margin-bottom: 30px;
}

.resume.creative-bold .section-title {
    font-size: 20px;
    font-weight: 700;
    text-transform: uppercase;
    color: #ff5722;
    margin-bottom: 20px;
    position: relative;
    padding-bottom: 10px;
}

.resume.creative-bold .section-title::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 3px;
    background-color: #ff5722;
}

.resume.creative-bold .item {
    margin-bottom: 25px;
    position: relative;
    padding-left: 20px;
}

.resume.creative-bold .item::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background-color: #ff5722;
    opacity: 0.3;
}

.resume.creative-bold .item-header {
    margin-bottom: 10px;
}

.resume.creative-bold .item-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 5px;
    color: #333;
}

.resume.creative-bold .item-subtitle {
    font-size: 14px;
    font-weight: 500;
    margin: 0 0 5px;
    color: #666;
}

.resume.creative-bold .item-meta {
    font-size: 12px;
    color: #888;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.resume.creative-bold .item-description {
    font-size: 14px;
    color: #555;
}

.resume.creative-bold .skill-item {
    margin-bottom: 15px;
}

.resume.creative-bold .skill-name {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 5px;
}

.resume.creative-bold .skill-bar {
    height: 6px;
    background-color: #eee;
    border-radius: 3px;
    overflow: hidden;
}

.resume.creative-bold .skill-progress {
    height: 100%;
    background-color: #ff5722;
}

.resume.creative-bold .language-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px dashed #eee;
}

.resume.creative-bold .language-name {
    font-weight: 500;
}

.resume.creative-bold .language-proficiency {
    font-size: 12px;
    color: #888;
}

.resume.creative-bold .certification-item {
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px dashed #eee;
}

.resume.creative-bold .certification-name {
    font-weight: 500;
    margin-bottom: 5px;
}

.resume.creative-bold .certification-org {
    font-size: 13px;
    color: #666;
    margin-bottom: 5px;
}

.resume.creative-bold .certification-date {
    font-size: 12px;
    color: #888;
    margin-bottom: 5px;
}

.resume.creative-bold .item-link a,
.resume.creative-bold .certification-link a {
    color: #ff5722;
    text-decoration: none;
    font-size: 13px;
    display: inline-block;
    margin-top: 5px;
}

.resume.creative-bold .item-link a:hover,
.resume.creative-bold .certification-link a:hover {
    text-decoration: underline;
}

/* Icons */
.resume.creative-bold .icon-email::before {
    content: "✉";
}

.resume.creative-bold .icon-phone::before {
    content: "☎";
}

.resume.creative-bold .icon-location::before {
    content: "📍";
}

.resume.creative-bold .icon-website::before {
    content: "🌐";
}

.resume.creative-bold .icon-linkedin::before {
    content: "🔗";
}

@media (max-width: 768px) {
    .resume.creative-bold .header-section {
        flex-direction: column;
        padding: 30px;
    }

    .resume.creative-bold .header-content {
        padding-right: 0;
        margin-bottom: 20px;
    }

    .resume.creative-bold .main-content {
        flex-direction: column;
        padding: 30px;
    }

    .resume.creative-bold .left-column,
    .resume.creative-bold .right-column {
        flex: auto;
    }
}
            ''',
            'is_premium': True,
            'is_active': True,
            'display_order': 1
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=creative_bold['slug'],
            defaults={
                **creative_bold,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)

        # Creative Infographic template
        creative_infographic = {
            'name': 'Creative Infographic',
            'slug': 'creative-infographic',
            'description': 'A visually engaging design with infographic elements for creative professionals.',
            'html_structure': '''
<div class="resume creative-infographic">
    <div class="sidebar">
        {% if resume.personal_info.profile_image %}
        <div class="profile-image">
            <img src="{{ resume.personal_info.profile_image.url }}" alt="{{ resume.personal_info.full_name }}">
        </div>
        {% endif %}

        <div class="name-title-section">
            <h1 class="full-name">{{ resume.personal_info.full_name }}</h1>
            <p class="job-title">{{ resume.personal_info.job_title }}</p>
        </div>

        <div class="sidebar-section contact-info">
            <h2 class="sidebar-title">Contact</h2>
            <div class="contact-list">
                {% if resume.personal_info.email %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-email"></i></div>
                    <div class="contact-text">{{ resume.personal_info.email }}</div>
                </div>
                {% endif %}
                {% if resume.personal_info.phone %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-phone"></i></div>
                    <div class="contact-text">{{ resume.personal_info.phone }}</div>
                </div>
                {% endif %}
                {% if resume.personal_info.address %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-location"></i></div>
                    <div class="contact-text">{{ resume.personal_info.address }}</div>
                </div>
                {% endif %}
                {% if resume.personal_info.website %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-website"></i></div>
                    <div class="contact-text">{{ resume.personal_info.website }}</div>
                </div>
                {% endif %}
                {% if resume.personal_info.linkedin %}
                <div class="contact-item">
                    <div class="contact-icon"><i class="icon-linkedin"></i></div>
                    <div class="contact-text">{{ resume.personal_info.linkedin }}</div>
                </div>
                {% endif %}
            </div>
        </div>

        {% if resume.skills.exists %}
        <div class="sidebar-section skills">
            <h2 class="sidebar-title">Skills</h2>
            <div class="skills-list">
                {% for skill in resume.skills.all %}
                <div class="skill-item">
                    <div class="skill-info">
                        <span class="skill-name">{{ skill.name }}</span>
                        <span class="skill-level-text">{{ skill.get_level_display }}</span>
                    </div>
                    <div class="skill-chart">
                        <div class="skill-chart-fill" style="width: {{ skill.level|multiply:20 }}%;"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        {% if resume.languages.exists %}
        <div class="sidebar-section languages">
            <h2 class="sidebar-title">Languages</h2>
            <div class="languages-list">
                {% for language in resume.languages.all %}
                <div class="language-item">
                    <div class="language-name">{{ language.name }}</div>
                    <div class="language-level">
                        {% if language.proficiency == 'elementary' %}
                        <div class="language-circle filled"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        {% elif language.proficiency == 'limited' %}
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        {% elif language.proficiency == 'professional' %}
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle"></div>
                        <div class="language-circle"></div>
                        {% elif language.proficiency == 'full_professional' %}
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle"></div>
                        {% elif language.proficiency == 'native' %}
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        <div class="language-circle filled"></div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>

    <div class="main-content">
        {% if resume.personal_info.summary %}
        <section class="resume-section">
            <h2 class="section-title">About Me</h2>
            <div class="section-content">
                <p>{{ resume.personal_info.summary }}</p>
            </div>
        </section>
        {% endif %}

        {% if resume.experiences.exists %}
        <section class="resume-section">
            <h2 class="section-title">Experience</h2>
            <div class="section-content timeline">
                {% for experience in resume.experiences.all %}
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="item-header">
                            <h3 class="item-title">{{ experience.position }}</h3>
                            <div class="item-subtitle">{{ experience.company }}{% if experience.location %} | {{ experience.location }}{% endif %}</div>
                            <div class="item-date">
                                {{ experience.start_date|date:"M Y" }} - 
                                {% if experience.current %}Present{% else %}{{ experience.end_date|date:"M Y" }}{% endif %}
                            </div>
                        </div>
                        {% if experience.description %}
                        <div class="item-description">
                            {{ experience.description|linebreaks }}
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.educations.exists %}
        <section class="resume-section">
            <h2 class="section-title">Education</h2>
            <div class="section-content timeline">
                {% for education in resume.educations.all %}
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="item-header">
                            <h3 class="item-title">{{ education.degree }}{% if education.field_of_study %} in {{ education.field_of_study }}{% endif %}</h3>
                            <div class="item-subtitle">{{ education.institution }}{% if education.location %} | {{ education.location }}{% endif %}</div>
                            <div class="item-date">
                                {{ education.start_date|date:"M Y" }} - 
                                {% if education.current %}Present{% else %}{{ education.end_date|date:"M Y" }}{% endif %}
                            </div>
                        </div>
                        {% if education.description %}
                        <div class="item-description">
                            {{ education.description|linebreaks }}
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.projects.exists %}
        <section class="resume-section">
            <h2 class="section-title">Projects</h2>
            <div class="section-content projects-grid">
                {% for project in resume.projects.all %}
                <div class="project-item">
                    <h3 class="item-title">{{ project.title }}</h3>
                    {% if project.start_date %}
                    <div class="item-date">
                        {{ project.start_date|date:"M Y" }}
                        {% if project.end_date %} - {{ project.end_date|date:"M Y" }}{% endif %}
                    </div>
                    {% endif %}
                    {% if project.description %}
                    <div class="item-description">
                        {{ project.description|linebreaks }}
                    </div>
                    {% endif %}
                    {% if project.url %}
                    <div class="item-link">
                        <a href="{{ project.url }}" target="_blank">View Project</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if resume.certifications.exists %}
        <section class="resume-section">
            <h2 class="section-title">Certifications</h2>
            <div class="section-content certifications-list">
                {% for certification in resume.certifications.all %}
                <div class="certification-item">
                    <div class="certification-icon">
                        <i class="icon-certificate"></i>
                    </div>
                    <div class="certification-details">
                        <h3 class="certification-name">{{ certification.name }}</h3>
                        <div class="certification-org">{{ certification.issuing_organization }}</div>
                        {% if certification.issue_date %}
                        <div class="certification-date">
                            {{ certification.issue_date|date:"M Y" }}
                            {% if certification.expiration_date %} - {{ certification.expiration_date|date:"M Y" }}{% endif %}
                        </div>
                        {% endif %}
                        {% if certification.credential_url %}
                        <div class="certification-link">
                            <a href="{{ certification.credential_url }}" target="_blank">View Credential</a>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}
    </div>
</div>
            ''',
            'css_styles': '''
/* Creative Infographic Template */
.resume.creative-infographic {
    font-family: 'Poppins', 'Helvetica Neue', sans-serif;
    display: flex;
    max-width: 1000px;
    margin: 0 auto;
    color: #333;
    line-height: 1.6;
    background-color: #fff;
}

.resume.creative-infographic .sidebar {
    width: 35%;
    background-color: #6c5ce7;
    color: white;
    padding: 40px 30px;
}

.resume.creative-infographic .main-content {
    width: 65%;
    padding: 40px;
}

.resume.creative-infographic .profile-image {
    text-align: center;
    margin-bottom: 20px;
}

.resume.creative-infographic .profile-image img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid rgba(255, 255, 255, 0.2);
}

.resume.creative-infographic .name-title-section {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.resume.creative-infographic .full-name {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.resume.creative-infographic .job-title {
    font-size: 16px;
    font-weight: 400;
    margin: 0;
    opacity: 0.9;
}

.resume.creative-infographic .sidebar-section {
    margin-bottom: 30px;
}

.resume.creative-infographic .sidebar-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    padding-bottom: 10px;
}

.resume.creative-infographic .sidebar-title::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 30px;
    height: 2px;
    background-color: white;
}

.resume.creative-infographic .contact-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.resume.creative-infographic .contact-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.resume.creative-infographic .contact-icon {
    width: 30px;
    height: 30px;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.resume.creative-infographic .contact-text {
    font-size: 14px;
    word-break: break-word;
}

.resume.creative-infographic .skill-item {
    margin-bottom: 15px;
}

.resume.creative-infographic .skill-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.resume.creative-infographic .skill-name {
    font-size: 14px;
    font-weight: 500;
}

.resume.creative-infographic .skill-level-text {
    font-size: 12px;
    opacity: 0.8;
}

.resume.creative-infographic .skill-chart {
    height: 6px;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    overflow: hidden;
}

.resume.creative-infographic .skill-chart-fill {
    height: 100%;
    background-color: white;
}

.resume.creative-infographic .language-item {
    margin-bottom: 15px;
}

.resume.creative-infographic .language-name {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 5px;
}

.resume.creative-infographic .language-level {
    display: flex;
    gap: 5px;
}

.resume.creative-infographic .language-circle {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.2);
}

.resume.creative-infographic .language-circle.filled {
    background-color: white;
}

.resume.creative-infographic .resume-section {
    margin-bottom: 35px;
}

.resume.creative-infographic .section-title {
    font-size: 20px;
    font-weight: 600;
    color: #6c5ce7;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    padding-bottom: 10px;
}

.resume.creative-infographic .section-title::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 40px;
    height: 3px;
    background-color: #6c5ce7;
}

.resume.creative-infographic .timeline {
    position: relative;
    padding-left: 30px;
}

.resume.creative-infographic .timeline::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 2px;
    background-color: #e0e0e0;
}

.resume.creative-infographic .timeline-item {
    position: relative;
    margin-bottom: 25px;
}

.resume.creative-infographic .timeline-marker {
    position: absolute;
    top: 0;
    left: -30px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #6c5ce7;
    border: 3px solid white;
    box-shadow: 0 0 0 2px #6c5ce7;
}

.resume.creative-infographic .item-header {
    margin-bottom: 10px;
}

.resume.creative-infographic .item-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 5px;
    color: #333;
}

.resume.creative-infographic .item-subtitle {
    font-size: 14px;
    color: #666;
    margin: 0 0 5px;
}

.resume.creative-infographic .item-date {
    font-size: 12px;
    color: #888;
    font-style: italic;
}

.resume.creative-infographic .item-description {
    font-size: 14px;
    color: #555;
}

.resume.creative-infographic .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.resume.creative-infographic .project-item {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s, box-shadow 0.3s;
}

.resume.creative-infographic .project-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.resume.creative-infographic .certifications-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.resume.creative-infographic .certification-item {
    display: flex;
    gap: 15px;
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.resume.creative-infographic .certification-icon {
    width: 40px;
    height: 40px;
    background-color: #6c5ce7;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.resume.creative-infographic .certification-details {
    flex: 1;
}

.resume.creative-infographic .certification-name {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 5px;
}

.resume.creative-infographic .certification-org {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
}

.resume.creative-infographic .certification-date {
    font-size: 12px;
    color: #888;
    font-style: italic;
    margin-bottom: 5px;
}

.resume.creative-infographic .item-link a,
.resume.creative-infographic .certification-link a {
    color: #6c5ce7;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
}

.resume.creative-infographic .item-link a:hover,
.resume.creative-infographic .certification-link a:hover {
    text-decoration: underline;
}

/* Icons */
.resume.creative-infographic .icon-email::before {
    content: "✉";
}

.resume.creative-infographic .icon-phone::before {
    content: "☎";
}

.resume.creative-infographic .icon-location::before {
    content: "📍";
}

.resume.creative-infographic .icon-website::before {
    content: "🌐";
}

.resume.creative-infographic .icon-linkedin::before {
    content: "🔗";
}

.resume.creative-infographic .icon-certificate::before {
    content: "🏆";
}

@media (max-width: 768px) {
    .resume.creative-infographic {
        flex-direction: column;
    }

    .resume.creative-infographic .sidebar,
    .resume.creative-infographic .main-content {
        width: 100%;
    }

    .resume.creative-infographic .projects-grid {
        grid-template-columns: 1fr;
    }
}
            ''',
            'is_premium': True,
            'is_active': True,
            'display_order': 2
        }

        # Create the template
        template, created = ResumeTemplate.objects.get_or_create(
            slug=creative_infographic['slug'],
            defaults={
                **creative_infographic,
                'category': category
            }
        )

        # Add a sample preview image
        if created:
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{template.slug}.png", image_content)