from django.core.management.base import BaseCommand
from templates_app.models import ResumeTemplate
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Creates a simple template for testing'

    def handle(self, *args, **options):
        # Check if simple template already exists
        if ResumeTemplate.objects.filter(slug='simple').exists():
            self.stdout.write(self.style.WARNING('Simple template already exists.'))
            return

        # First, let's check what fields are available in the model
        # This is a safer approach than assuming fields exist
        available_fields = [field.name for field in ResumeTemplate._meta.get_fields()
                            if not field.is_relation and not field.auto_created]

        self.stdout.write(f"Available fields in ResumeTemplate model: {', '.join(available_fields)}")

        # Create a dictionary with all possible fields
        template_data = {
            'name': 'Simple Template',
            'slug': 'simple',
            'description': 'A simple resume template for testing purposes.',
        }

        # Add HTML content if the field exists
        if 'html_content' in available_fields:
            template_data['html_content'] = """
            <div class="resume-container">
                <header class="resume-header">
                    <h1 class="name">{{ full_name }}</h1>
                    <p class="title">{{ job_title }}</p>
                    <div class="contact-info">
                        <p>{{ email }}</p>
                        <p>{{ phone }}</p>
                        <p>{{ location }}</p>
                    </div>
                </header>

                <section class="resume-section summary">
                    <h2>Professional Summary</h2>
                    <p>{{ summary }}</p>
                </section>

                <section class="resume-section experience">
                    <h2>Work Experience</h2>
                    {{ experience_content }}
                </section>

                <section class="resume-section education">
                    <h2>Education</h2>
                    {{ education_content }}
                </section>

                <section class="resume-section skills">
                    <h2>Skills</h2>
                    {{ skills_content }}
                </section>
            </div>
            """

        # Add CSS content if the field exists
        if 'css_content' in available_fields:
            template_data['css_content'] = """
            .resume-container {
                font-family: 'Arial', sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 30px;
                color: #333;
            }

            .resume-header {
                margin-bottom: 30px;
            }

            .name {
                color: #1a73e8;
                font-size: 26px;
                margin: 0;
            }

            .title {
                font-size: 16px;
                color: #555;
                margin: 5px 0 15px;
            }

            h2 {
                color: #1a73e8;
                font-size: 20px;
                margin-top: 25px;
                margin-bottom: 15px;
            }

            .resume-section {
                margin-bottom: 25px;
            }
            """

        # Add other fields if they exist
        if 'is_premium' in available_fields:
            template_data['is_premium'] = False

        if 'color_scheme' in available_fields:
            template_data['color_scheme'] = 'blue'

        if 'style' in available_fields:
            template_data['style'] = 'modern'

        if 'layout' in available_fields:
            template_data['layout'] = 'single-column'

        # Filter out any fields that don't exist in the model
        filtered_data = {k: v for k, v in template_data.items() if k in available_fields}

        # Create the template with only the fields that exist in the model
        try:
            template = ResumeTemplate.objects.create(**filtered_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created simple template (ID: {template.id})'))
            self.stdout.write(f'Template URL: /templates_app/templates/{template.slug}/')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating template: {str(e)}'))

            # Try to provide more helpful information
            self.stdout.write(self.style.WARNING('Attempting to create template with minimal fields...'))
            try:
                # Try with just the essential fields
                minimal_template = ResumeTemplate.objects.create(
                    name='Simple Template',
                    slug='simple',
                    description='A simple resume template for testing purposes.'
                )
                self.stdout.write(self.style.SUCCESS(f'Created minimal template (ID: {minimal_template.id})'))
                self.stdout.write(f'Template URL: /templates_app/templates/{minimal_template.slug}/')
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f'Error creating minimal template: {str(e2)}'))
                self.stdout.write(self.style.ERROR('Please check your ResumeTemplate model definition.'))