from django.core.management.base import BaseCommand
from resume.models import TemplateCategory


class Command(BaseCommand):
    help = 'Creates the default template categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Simple',
                'slug': 'simple',
                'description': 'Clean and straightforward designs that focus on content.',
                'display_order': 1
            },
            {
                'name': 'Modern',
                'slug': 'modern',
                'description': 'Contemporary designs with creative layouts and styling.',
                'display_order': 2
            },
            {
                'name': 'Classical',
                'slug': 'classical',
                'description': 'Traditional designs that are widely accepted across industries.',
                'display_order': 3
            },
            {
                'name': 'Creative',
                'slug': 'creative',
                'description': 'Bold and unique designs that help you stand out.',
                'display_order': 4
            }
        ]

        for category_data in categories:
            TemplateCategory.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully created template categories'))

