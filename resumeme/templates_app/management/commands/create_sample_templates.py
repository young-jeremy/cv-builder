from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from templates_app.models import TemplateCategory, ResumeTemplate, TemplateColor, TemplateSection
import os
import requests
from io import BytesIO
from PIL import Image


class Command(BaseCommand):
    help = 'Creates sample resume templates for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample resume templates...')

        # Create template categories
        categories = [
            {
                'name': 'All templates',
                'icon': 'fas fa-th-large',
                'order': 1
            },
            {
                'name': 'Picture',
                'icon': 'fas fa-image',
                'order': 2
            },
            {
                'name': 'Word',
                'icon': 'fas fa-file-word',
                'order': 3
            },
            {
                'name': 'Simple',
                'icon': 'fas fa-feather',
                'order': 4
            },
            {
                'name': 'ATS',
                'icon': 'fas fa-check-circle',
                'order': 5
            },
            {
                'name': 'Two-column',
                'icon': 'fas fa-columns',
                'order': 6
            },
            {
                'name': 'Google Docs',
                'icon': 'fas fa-file-alt',
                'order': 7
            },
        ]

        for category_data in categories:
            category, created = TemplateCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'icon': category_data['icon'],
                    'order': category_data['order'],
                    'slug': slugify(category_data['name'])
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get category objects for assignment
        all_templates = TemplateCategory.objects.get(slug='all-templates')
        picture = TemplateCategory.objects.get(slug='picture')
        word = TemplateCategory.objects.get(slug='word')
        simple = TemplateCategory.objects.get(slug='simple')
        ats = TemplateCategory.objects.get(slug='ats')
        two_column = TemplateCategory.objects.get(slug='two-column')
        google_docs = TemplateCategory.objects.get(slug='google-docs')

        # Create sample templates
        templates = [
            {
                'name': 'Professional',
                'description': 'A clean and professional template ideal for corporate roles and traditional industries.',
                'categories': [all_templates, ats, simple],
                'is_ats_friendly': True,
                'is_featured': True,
                'has_photo': False,
                'is_premium': False,
                'colors': [
                    {'name': 'Blue', 'primary_color': '#2D9CDB', 'is_default': True},
                    {'name': 'Green', 'primary_color': '#27AE60'},
                    {'name': 'Gray', 'primary_color': '#4F4F4F'},
                    {'name': 'Red', 'primary_color': '#EB5757'},
                ]
            },
            {
                'name': 'Executive',
                'description': 'An elegant template designed for senior positions and executive roles.',
                'categories': [all_templates, ats, word],
                'is_ats_friendly': True,
                'is_featured': False,
                'has_photo': True,
                'is_premium': True,
                'colors': [
                    {'name': 'Navy', 'primary_color': '#2F80ED', 'is_default': True},
                    {'name': 'Burgundy', 'primary_color': '#9B2C2C'},
                    {'name': 'Dark Gray', 'primary_color': '#333333'},
                ]
            },
            {
                'name': 'Creative',
                'description': 'A modern and creative template perfect for design, marketing, and creative roles.',
                'categories': [all_templates, picture],
                'is_ats_friendly': False,
                'is_featured': True,
                'has_photo': True,
                'is_premium': False,
                'colors': [
                    {'name': 'Purple', 'primary_color': '#9B51E0', 'is_default': True},
                    {'name': 'Teal', 'primary_color': '#2D9CDB'},
                    {'name': 'Orange', 'primary_color': '#F2994A'},
                ]
            },
            {
                'name': 'Minimalist',
                'description': 'A clean and minimalist template that focuses on content with subtle design elements.',
                'categories': [all_templates, simple, ats],
                'is_ats_friendly': True,
                'is_featured': False,
                'has_photo': False,
                'is_premium': False,
                'colors': [
                    {'name': 'Black', 'primary_color': '#333333', 'is_default': True},
                    {'name': 'Gray', 'primary_color': '#828282'},
                    {'name': 'Blue', 'primary_color': '#2D9CDB'},
                ]
            },
            {
                'name': 'Modern',
                'description': 'A contemporary template with a balanced layout suitable for most industries.',
                'categories': [all_templates, two_column, word],
                'is_ats_friendly': True,
                'is_featured': True,
                'has_photo': True,
                'is_premium': False,
                'colors': [
                    {'name': 'Blue', 'primary_color': '#2D9CDB', 'is_default': True},
                    {'name': 'Green', 'primary_color': '#27AE60'},
                    {'name': 'Red', 'primary_color': '#EB5757'},
                ]
            },
            {
                'name': 'Technical',
                'description': 'Designed specifically for technical roles with sections for skills and projects.',
                'categories': [all_templates, ats, google_docs],
                'is_ats_friendly': True,
                'is_featured': False,
                'has_photo': False,
                'is_premium': False,
                'colors': [
                    {'name': 'Dark Blue', 'primary_color': '#2F80ED', 'is_default': True},
                    {'name': 'Gray', 'primary_color': '#4F4F4F'},
                    {'name': 'Black', 'primary_color': '#333333'},
                ]
            },
            {
                'name': 'Graduate',
                'description': 'Perfect for recent graduates and entry-level professionals with emphasis on education.',
                'categories': [all_templates, simple, google_docs],
                'is_ats_friendly': True,
                'is_featured': False,
                'has_photo': False,
                'is_premium': False,
                'colors': [
                    {'name': 'Green', 'primary_color': '#27AE60', 'is_default': True},
                    {'name': 'Blue', 'primary_color': '#2D9CDB'},
                    {'name': 'Purple', 'primary_color': '#9B51E0'},
                ]
            },
            {
                'name': 'Elegant',
                'description': 'A sophisticated template with elegant typography and layout for professionals.',
                'categories': [all_templates, picture, two_column],
                'is_ats_friendly': False,
                'is_featured': True,
                'has_photo': True,
                'is_premium': True,
                'colors': [
                    {'name': 'Gold', 'primary_color': '#F2C94C', 'is_default': True},
                    {'name': 'Burgundy', 'primary_color': '#9B2C2C'},
                    {'name': 'Navy', 'primary_color': '#2F80ED'},
                ]
            },
            {
                'name': 'Compact',
                'description': 'A space-efficient template that fits more content while maintaining readability.',
                'categories': [all_templates, ats, word],
                'is_ats_friendly': True,
                'is_featured': False,
                'has_photo': False,
                'is_premium': False,
                'colors': [
                    {'name': 'Blue', 'primary_color': '#2D9CDB', 'is_default': True},
                    {'name': 'Gray', 'primary_color': '#4F4F4F'},
                    {'name': 'Green', 'primary_color': '#27AE60'},
                ]
            },
            {
                'name': 'Contemporary',
                'description': 'A fresh and contemporary design with modern typography and layout.',
                'categories': [all_templates, two_column, picture],
                'is_ats_friendly': False,
                'is_featured': True,
                'has_photo': True,
                'is_premium': True,
                'colors': [
                    {'name': 'Teal', 'primary_color': '#219653', 'is_default': True},
                    {'name': 'Orange', 'primary_color': '#F2994A'},
                    {'name': 'Purple', 'primary_color': '#9B51E0'},
                ]
            }
        ]

        # Create sample templates
        for template_data in templates:
            template, created = ResumeTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'slug': slugify(template_data['name']),
                    'description': template_data['description'],
                    'is_ats_friendly': template_data['is_ats_friendly'],
                    'is_featured': template_data['is_featured'],
                    'has_photo': template_data['has_photo'],
                    'is_premium': template_data['is_premium'],
                    'html_structure': '<div class="resume">Sample HTML structure</div>',
                    'css_template': '.resume { font-family: Arial, sans-serif; }',
                }
            )

            if created:
                # Add categories
                for category in template_data['categories']:
                    template.categories.add(category)

                # Create a placeholder image
                img = Image.new('RGB', (800, 1100), color=(255, 255, 255))
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                template.preview_image.save(f"{template.slug}.jpg", ContentFile(img_io.getvalue()))

                # Create color schemes
                for color_data in template_data['colors']:
                    TemplateColor.objects.create(
                        template=template,
                        name=color_data['name'],
                        primary_color=color_data['primary_color'],
                        is_default=color_data.get('is_default', False)
                    )

                # Create template sections
                sections = [
                    {'type': 'contact', 'name': 'Contact Information', 'required': True},
                    {'type': 'summary', 'name': 'Professional Summary', 'required': False},
                    {'type': 'experience', 'name': 'Work Experience', 'required': True},
                    {'type': 'education', 'name': 'Education', 'required': True},
                    {'type': 'skills', 'name': 'Skills', 'required': False},
                    {'type': 'languages', 'name': 'Languages', 'required': False},
                    {'type': 'certifications', 'name': 'Certifications', 'required': False},
                ]

                for i, section in enumerate(sections):
                    TemplateSection.objects.create(
                        template=template,
                        section_type=section['type'],
                        name=section['name'],
                        is_required=section['required'],
                        order=i
                    )

                self.stdout.write(f'Created template: {template.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample templates!'))