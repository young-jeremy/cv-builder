from django.core.management.base import BaseCommand
from django.utils.text import slugify
from dashboard.models import ResumeTemplate
from django.core.files.base import ContentFile
import os


class Command(BaseCommand):
    help = 'Creates default resume templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Professional Classic',
                'description': 'A clean, professional template with a traditional layout.',
                'category': 'professional',
                'html_structure': '''
                <div class="resume professional-classic">
                    <div class="header">
                        <h1>{first_name} {last_name}</h1>
                        <div class="contact-info">
                            <p>{email} | {phone} | {address}, {city}, {state} {zip_code}</p>
                            <p>{linkedin} | {website}</p>
                        </div>
                    </div>

                    <div class="section summary">
                        <h2>Professional Summary</h2>
                        <p>{summary}</p>
                    </div>

                    <div class="section experience">
                        <h2>Work Experience</h2>
                        <!-- Experience items will be dynamically inserted here -->
                    </div>

                    <div class="section education">
                        <h2>Education</h2>
                        <!-- Education items will be dynamically inserted here -->
                    </div>

                    <div class="section skills">
                        <h2>Skills</h2>
                        <ul class="skills-list">
                            <!-- Skills will be dynamically inserted here -->
                        </ul>
                    </div>
                </div>
                ''',
                'css_styles': '''
                .resume.professional-classic {
                    font-family: 'Arial', sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 30px;
                    color: #333;
                }

                .resume.professional-classic .header {
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #0D6EFD;
                    padding-bottom: 20px;
                }

                .resume.professional-classic h1 {
                    font-size: 28px;
                    margin-bottom: 10px;
                    color: #0D6EFD;
                }

                .resume.professional-classic .contact-info {
                    font-size: 14px;
                }

                .resume.professional-classic .section {
                    margin-bottom: 25px;
                }

                .resume.professional-classic h2 {
                    font-size: 18px;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 5px;
                    margin-bottom: 15px;
                    color: #0D6EFD;
                }

                .resume.professional-classic .experience-item,
                .resume.professional-classic .education-item {
                    margin-bottom: 15px;
                }

                .resume.professional-classic .job-title,
                .resume.professional-classic .degree {
                    font-weight: bold;
                }

                .resume.professional-classic .employer,
                .resume.professional-classic .institution {
                    font-style: italic;
                }

                .resume.professional-classic .date {
                    color: #666;
                    font-size: 14px;
                }

                .resume.professional-classic .skills-list {
                    display: flex;
                    flex-wrap: wrap;
                    list-style-type: none;
                    padding: 0;
                }

                .resume.professional-classic .skills-list li {
                    background-color: #f0f0f0;
                    padding: 5px 10px;
                    margin: 0 10px 10px 0;
                    border-radius: 3px;
                }
                '''
            },
            {
                'name': 'Modern Minimal',
                'description': 'A sleek, modern template with minimalist design.',
                'category': 'modern',
                'html_structure': '''
                <div class="resume modern-minimal">
                    <div class="sidebar">
                        <div class="profile">
                            <h1>{first_name}<br>{last_name}</h1>
                        </div>

                        <div class="contact-info">
                            <h2>Contact</h2>
                            <ul>
                                <li><i class="bi bi-envelope"></i> {email}</li>
                                <li><i class="bi bi-telephone"></i> {phone}</li>
                                <li><i class="bi bi-geo-alt"></i> {city}, {state}</li>
                                <li><i class="bi bi-linkedin"></i> {linkedin}</li>
                                <li><i class="bi bi-globe"></i> {website}</li>
                            </ul>
                        </div>

                        <div class="skills-section">
                            <h2>Skills</h2>
                            <div class="skills-container">
                                <!-- Skills will be dynamically inserted here -->
                            </div>
                        </div>
                    </div>

                    <div class="main-content">
                        <div class="section summary">
                            <h2>Profile</h2>
                            <p>{summary}</p>
                        </div>

                        <div class="section experience">
                            <h2>Experience</h2>
                            <!-- Experience items will be dynamically inserted here -->
                        </div>

                        <div class="section education">
                            <h2>Education</h2>
                            <!-- Education items will be dynamically inserted here -->
                        </div>
                    </div>
                </div>
                ''',
                'css_styles': '''
                .resume.modern-minimal {
                    font-family: 'Roboto', sans-serif;
                    display: flex;
                    max-width: 800px;
                    margin: 0 auto;
                    color: #333;
                }

                .resume.modern-minimal .sidebar {
                    width: 30%;
                    background-color: #f8f9fa;
                    padding: 30px;
                }

                .resume.modern-minimal .main-content {
                    width: 70%;
                    padding: 30px;
                }

                .resume.modern-minimal h1 {
                    font-size: 24px;
                    font-weight: 700;
                    margin-bottom: 20px;
                    color: #0D6EFD;
                }

                .resume.modern-minimal h2 {
                    font-size: 18px;
                    font-weight: 600;
                    margin-bottom: 15px;
                    color: #0D6EFD;
                    border-bottom: 2px solid #0D6EFD;
                    padding-bottom: 5px;
                }

                .resume.modern-minimal .contact-info ul {
                    list-style-type: none;
                    padding: 0;
                }

                .resume.modern-minimal .contact-info li {
                    margin-bottom: 10px;
                    font-size: 14px;
                }

                .resume.modern-minimal .contact-info i {
                    margin-right: 10px;
                    color: #0D6EFD;
                }

                .resume.modern-minimal .skills-container {
                    display: flex;
                    flex-wrap: wrap;
                }

                .resume.modern-minimal .skill {
                    background-color: #e9ecef;
                    padding: 5px 10px;
                    margin: 0 5px 5px 0;
                    border-radius: 3px;
                    font-size: 12px;
                }

                .resume.modern-minimal .section {
                    margin-bottom: 25px;
                }

                .resume.modern-minimal .experience-item,
                .resume.modern-minimal .education-item {
                    margin-bottom: 20px;
                }

                .resume.modern-minimal .job-title,
                .resume.modern-minimal .degree {
                    font-weight: bold;
                    font-size: 16px;
                }

                .resume.modern-minimal .employer,
                .resume.modern-minimal .institution {
                    font-style: italic;
                    color: #666;
                }

                .resume.modern-minimal .date {
                    color: #0D6EFD;
                    font-size: 14px;
                    margin: 5px 0;
                }
                '''
            },
            # Add more templates as needed
        ]

        for template_data in templates:
            slug = slugify(template_data['name'])

            # Check if template already exists
            if not ResumeTemplate.objects.filter(slug=slug).exists():
                template = ResumeTemplate(
                    name=template_data['name'],
                    slug=slug,
                    description=template_data['description'],
                    category=template_data['category'],
                    html_structure=template_data['html_structure'],
                    css_styles=template_data['css_styles']
                )

                # Create a placeholder image if needed
                # In a real app, you'd have actual preview images
                image_path = f'dashboard/static/images/templates/{slug}.png'
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        template.preview_image.save(f'{slug}.png', ContentFile(f.read()))

                template.save()
                self.stdout.write(self.style.SUCCESS(f'Created template: {template.name}'))
            else:
                self.stdout.write(f'Template already exists: {template_data["name"]}')

        self.stdout.write(self.style.SUCCESS('Successfully created default templates'))