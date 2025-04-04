# Run this in Django shell (python manage.py shell)
from templates_app.models import ResumeTemplate

# Check if template exists
template = ResumeTemplate.objects.filter(slug='simple').first()
print(f"Template exists: {template is not None}")

if template:
    print(f"Template details: {template.name}, {template.slug}")
else:
    # List all available templates
    all_templates = ResumeTemplate.objects.all()
    print(f"Available templates: {[t.slug for t in all_templates]}")