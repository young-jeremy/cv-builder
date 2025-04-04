from django.core.management.base import BaseCommand
from templates_app.models import ResumeTemplate


class Command(BaseCommand):
    help = 'Checks and lists all available resume templates'

    def handle(self, *args, **options):
        templates = ResumeTemplate.objects.all()

        if not templates:
            self.stdout.write(self.style.WARNING('No templates found in the database.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {templates.count()} templates:'))

        for template in templates:
            self.stdout.write(f"- {template.name} (slug: {template.slug})")
            self.stdout.write(f"  Style: {template.style}, Color: {template.color_scheme}")
            self.stdout.write(f"  Premium: {'Yes' if template.is_premium else 'No'}")
            self.stdout.write("")