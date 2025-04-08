# management/commands/create_sample_templates.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.conf import settings
import os
from resume_app.models import ResumeTemplate
import random


class Command(BaseCommand):
    help = 'Creates sample resume templates with images'

    def handle(self, *args, **options):
        # Sample template data
        templates = [
            {
                'name': 'Stockholm',
                'description': 'A clean, professional template with a two-column layout perfect for corporate roles.',
                'style': 'professional',
                'color': 'blue',
                'is_premium': False,
                'is_featured': True,
            },
            # Add more templates...
        ]

        # Path to sample images
        sample_images_dir = os.path.join(settings.BASE_DIR, 'sample_images', 'templates')

        for template_data in templates:
            # Create template
            template = ResumeTemplate(
                name=template_data['name'],
                slug=slugify(template_data['name']),
                description=template_data['description'],
                style=template_data['style'],
                color=template_data['color'],
                is_premium=template_data['is_premium'],
                is_featured=template_data['is_featured'],
                popularity=random.randint(10, 100),
                category='professional',
            )

            # Try to find a matching image file
            image_path = os.path.join(sample_images_dir, f"{slugify(template_data['name'])}.jpg")
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    template.preview_image.save(
                        f"{slugify(template_data['name'])}.jpg",
                        ContentFile(f.read()),
                        save=False
                    )
            else:
                self.stdout.write(self.style.WARNING(f"No image found for {template_data['name']}"))

            template.save()
            self.stdout.write(self.style.SUCCESS(f"Created template: {template.name}"))