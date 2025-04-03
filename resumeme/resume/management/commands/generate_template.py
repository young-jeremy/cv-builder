from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from resume.models import TemplateCategory, ResumeTemplate
import os
import argparse


class Command(BaseCommand):
    help = 'Generate a new resume template'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Template name')
        parser.add_argument('category', type=str, help='Template category (simple, modern, classical, creative)')
        parser.add_argument('--premium', action='store_true', help='Mark as premium template')
        parser.add_argument('--description', type=str, default='', help='Template description')
        parser.add_argument('--html', type=str, help='Path to HTML structure file')
        parser.add_argument('--css', type=str, help='Path to CSS styles file')
        parser.add_argument('--preview', type=str, help='Path to preview image file')

    def handle(self, *args, **options):
        name = options['name']
        category_slug = options['category'].lower()
        is_premium = options['premium']
        description = options['description'] or f'A {category_slug} resume template.'

        # Check if category exists
        try:
            category = TemplateCategory.objects.get(slug=category_slug)
        except TemplateCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category "{category_slug}" does not exist.'))
            return

        # Generate slug from name
        slug = name.lower().replace(' ', '-')

        # Check if template with this slug already exists
        if ResumeTemplate.objects.filter(slug=slug).exists():
            self.stdout.write(self.style.ERROR(f'Template with slug "{slug}" already exists.'))
            return

        # Read HTML structure
        html_structure = ''
        if options['html'] and os.path.exists(options['html']):
            with open(options['html'], 'r') as f:
                html_structure = f.read()
        else:
            self.stdout.write(
                self.style.WARNING('HTML structure file not provided or does not exist. Using empty structure.'))

        # Read CSS styles
        css_styles = ''
        if options['css'] and os.path.exists(options['css']):
            with open(options['css'], 'r') as f:
                css_styles = f.read()
        else:
            self.stdout.write(self.style.WARNING('CSS styles file not provided or does not exist. Using empty styles.'))

        # Create template
        template = ResumeTemplate.objects.create(
            name=name,
            slug=slug,
            category=category,
            description=description,
            html_structure=html_structure,
            css_styles=css_styles,
            is_premium=is_premium,
            is_active=True,
            display_order=0
        )

        # Add preview image if provided
        if options['preview'] and os.path.exists(options['preview']):
            with open(options['preview'], 'rb') as f:
                image_content = ContentFile(f.read())
                template.preview_image.save(f"{slug}.{options['preview'].split('.')[-1]}", image_content)
        else:
            self.stdout.write(self.style.WARNING('Preview image not provided or does not exist. Using placeholder.'))
            image_content = ContentFile(b'placeholder image data')
            template.preview_image.save(f"{slug}.png", image_content)

        self.stdout.write(self.style.SUCCESS(f'Successfully created template "{name}" in category "{category.name}"'))

