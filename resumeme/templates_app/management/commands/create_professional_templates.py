from django.core.management.base import BaseCommand
from django.utils.text import slugify
from templates_app.models import ResumeTemplate, TemplateCategory
import random


class Command(BaseCommand):
    help = 'Creates professional resume templates'

    def handle(self, *args, **options):
        # Ensure the professional category exists
        professional_category, created = TemplateCategory.objects.get_or_create(
            name='Professional',
            slug='professional'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Professional category'))

        # Define template data
        professional_templates = [
            {
                'name': 'Executive',
                'description': 'A sophisticated template with a clean layout, perfect for senior executives and leadership roles.',
                'style': 'executive',
                'color': 'navy',
                'is_premium': True,
                'is_featured': True,
                'difficulty_level': 'intermediate',
                'html_structure': self.get_executive_html(),
                'css_template': self.get_executive_css(),
            },
            {
                'name': 'Corporate',
                'description': 'A traditional corporate template with a professional look, ideal for business and finance roles.',
                'style': 'corporate',
                'color': 'blue',
                'is_premium': False,
                'is_featured': True,
                'difficulty_level': 'beginner',
                'html_structure': self.get_corporate_html(),
                'css_template': self.get_corporate_css(),
            },
            {
                'name': 'Professional Classic',
                'description': 'A timeless classic template with a traditional layout, suitable for all professional roles.',
                'style': 'classic',
                'color': 'black',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'beginner',
                'html_structure': self.get_classic_html(),
                'css_template': self.get_classic_css(),
            },
            {
                'name': 'Minimalist Pro',
                'description': 'A clean, minimalist design that lets your experience speak for itself.',
                'style': 'minimalist',
                'color': 'gray',
                'is_premium': False,
                'is_featured': True,
                'difficulty_level': 'beginner',
                'html_structure': self.get_minimalist_html(),
                'css_template': self.get_minimalist_css(),
            },
            {
                'name': 'Elegant',
                'description': 'An elegant template with refined typography and subtle design elements.',
                'style': 'elegant',
                'color': 'burgundy',
                'is_premium': True,
                'is_featured': True,
                'difficulty_level': 'intermediate',
                'html_structure': self.get_elegant_html(),
                'css_template': self.get_elegant_css(),
            },
            {
                'name': 'Bold Professional',
                'description': 'A bold template with strong headings and clear sections, perfect for making an impact.',
                'style': 'bold',
                'color': 'blue',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'beginner',
                'html_structure': self.get_bold_html(),
                'css_template': self.get_bold_css(),
            },
            {
                'name': 'Modern Executive',
                'description': 'A modern take on the executive resume with clean lines and strategic use of color.',
                'style': 'executive',
                'color': 'green',
                'is_premium': True,
                'is_featured': False,
                'difficulty_level': 'advanced',
                'html_structure': self.get_modern_executive_html(),
                'css_template': self.get_modern_executive_css(),
            },
            {
                'name': 'Classic Blue',
                'description': 'A classic template with blue accents, perfect for traditional industries.',
                'style': 'classic',
                'color': 'blue',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'beginner',
                'html_structure': self.get_classic_blue_html(),
                'css_template': self.get_classic_blue_css(),
            },
            {
                'name': 'Corporate Gray',
                'description': 'A subtle gray corporate template that exudes professionalism and reliability.',
                'style': 'corporate',
                'color': 'gray',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'beginner',
                'html_structure': self.get_corporate_gray_html(),
                'css_template': self.get_corporate_gray_css(),
            },
            {
                'name': 'Minimalist Black',
                'description': 'A stark black and white minimalist template for a bold professional statement.',
                'style': 'minimalist',
                'color': 'black',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'intermediate',
                'html_structure': self.get_minimalist_black_html(),
                'css_template': self.get_minimalist_black_css(),
            },
            {
                'name': 'Elegant Navy',
                'description': 'An elegant template with navy accents for a sophisticated professional look.',
                'style': 'elegant',
                'color': 'navy',
                'is_premium': True,
                'is_featured': False,
                'difficulty_level': 'intermediate',
                'html_structure': self.get_elegant_navy_html(),
                'css_template': self.get_elegant_navy_css(),
            },
            {
                'name': 'Bold Green',
                'description': 'A bold template with green accents, perfect for making a statement while maintaining professionalism.',
                'style': 'bold',
                'color': 'green',
                'is_premium': False,
                'is_featured': False,
                'difficulty_level': 'intermediate',
                'html_structure': self.get_bold_green_html(),
                'css_template': self.get_bold_green_css(),
            },
        ]

        # Create templates
        templates_created = 0
        for template_data in professional_templates:
            slug = slugify(template_data['name'])

            # Check if template already exists
            if not ResumeTemplate.objects.filter(slug=slug).exists():
                # Set default values for fields that might not be in the data
                template_data.setdefault('is_premium', False)
                template_data.setdefault('is_featured', False)
                template_data.setdefault('has_photo', False)
                template_data.setdefault('is_ats_friendly', True)
                template_data.setdefault('difficulty_level', 'beginner')

                # Set category to professional
                template_data['category'] = 'professional'

                # Generate a random popularity score for sorting
                template_data['popularity'] = random.randint(10, 1000)

                # Create a placeholder for preview_image
                # In a real scenario, you would need to provide actual images
                preview_image = None

                # Create the template
                template = ResumeTemplate.objects.create(
                    name=template_data['name'],
                    slug=slug,
                    description=template_data['description'],
                    category=template_data['category'],
                    style=template_data['style'],
                    color=template_data['color'],
                    is_premium=template_data['is_premium'],
                    is_featured=template_data['is_featured'],
                    has_photo=template_data['has_photo'],
                    is_ats_friendly=template_data['is_ats_friendly'],
                    difficulty_level=template_data['difficulty_level'],
                    popularity=template_data['popularity'],
                    html_structure=template_data['html_structure'],
                    css_template=template_data['css_template'],
                    preview_image=preview_image,  # This will need to be updated with actual images
                )

                # Add the professional category
                template.categories.add(professional_category)

                templates_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created template: {template.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Template already exists: {template_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {templates_created} professional templates'))

    # Template HTML and CSS methods remain the same...
    def get_executive_html(self):
        return '''
<div class="resume executive">
  <header class="resume-header">
    <h1 class="resume-name">{first_name} {last_name}</h1>
    <div class="resume-contact">
      <div class="contact-item"><i class="icon-email"></i>{email}</div>
      <div class="contact-item"><i class="icon-phone"></i>{phone}</div>
      <div class="contact-item"><i class="icon-location"></i>{address}, {city}, {state} {zip_code}</div>
      <div class="contact-item"><i class="icon-linkedin"></i>{linkedin}</div>
      <div class="contact-item"><i class="icon-website"></i>{website}</div>
    </div>
  </header>

  <section class="resume-summary">
    <h2 class="section-title">Executive Summary</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Professional Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Core Competencies</h2>
    <div class="section-content skills-grid">
      <!-- Skills will be populated dynamically -->
    </div>
  </section>
</div>
'''

    def get_executive_css(self):
        return '''
.resume.executive {
  font-family: 'Georgia', serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.resume.executive .resume-header {
  border-bottom: 2px solid #1a365d;
  padding-bottom: 20px;
  margin-bottom: 30px;
}

.resume.executive .resume-name {
  font-size: 28px;
  font-weight: 700;
  color: #1a365d;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.resume.executive .resume-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 14px;
}

.resume.executive .contact-item {
  display: flex;
  align-items: center;
}

.resume.executive .section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a365d;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 30px 0 15px 0;
  border-bottom: 1px solid #ccc;
  padding-bottom: 5px;
}

.resume.executive .section-content {
  margin-bottom: 25px;
}

.resume.executive .skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.resume.executive .experience-item,
.resume.executive .education-item {
  margin-bottom: 20px;
}

.resume.executive .job-title,
.resume.executive .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
}

.resume.executive .employer,
.resume.executive .institution {
  font-weight: 700;
  font-style: italic;
}

.resume.executive .date {
  font-style: italic;
  color: #666;
  margin-bottom: 10px;
}

.resume.executive .description {
  font-size: 14px;
}
'''

    def get_corporate_html(self):
        return '''
<div class="resume corporate">
  <header class="resume-header">
    <h1 class="resume-name">{first_name} {last_name}</h1>
    <div class="resume-contact">
      <div>{email} | {phone}</div>
      <div>{address}, {city}, {state} {zip_code}</div>
      <div>{linkedin} | {website}</div>
    </div>
  </header>

  <section class="resume-summary">
    <h2 class="section-title">Professional Summary</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Work Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Skills</h2>
    <div class="section-content">
      <ul class="skills-list">
        <!-- Skills will be populated dynamically -->
      </ul>
    </div>
  </section>
</div>
'''

    def get_corporate_css(self):
        return '''
.resume.corporate {
  font-family: 'Arial', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.corporate .resume-header {
  text-align: center;
  margin-bottom: 30px;
}

.resume.corporate .resume-name {
  font-size: 24px;
  font-weight: 700;
  color: #2b6cb0;
  margin: 0 0 10px 0;
}

.resume.corporate .resume-contact {
  font-size: 14px;
  line-height: 1.6;
}

.resume.corporate .section-title {
  font-size: 16px;
  font-weight: 700;
  color: #2b6cb0;
  text-transform: uppercase;
  margin: 25px 0 15px 0;
  border-bottom: 1px solid #2b6cb0;
  padding-bottom: 5px;
}

.resume.corporate .section-content {
  margin-bottom: 20px;
}

.resume.corporate .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.corporate .skills-list li {
  background-color: #edf2f7;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 14px;
}

.resume.corporate .experience-item,
.resume.corporate .education-item {
  margin-bottom: 20px;
}

.resume.corporate .job-title,
.resume.corporate .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
}

.resume.corporate .employer,
.resume.corporate .institution {
  font-weight: 700;
}

.resume.corporate .date {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.corporate .description {
  font-size: 14px;
}
'''

    # Add methods for other templates...
    def get_classic_html(self):
        return '''
<div class="resume classic">
  <header class="resume-header">
    <h1 class="resume-name">{first_name} {last_name}</h1>
    <div class="resume-contact">
      <div>{email} | {phone}</div>
      <div>{address}, {city}, {state} {zip_code}</div>
      <div>{linkedin} | {website}</div>
    </div>
  </header>

  <hr class="divider">

  <section class="resume-summary">
    <h2 class="section-title">Professional Summary</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Skills</h2>
    <div class="section-content">
      <ul class="skills-list">
        <!-- Skills will be populated dynamically -->
      </ul>
    </div>
  </section>
</div>
'''

    def get_classic_css(self):
        return '''
.resume.classic {
  font-family: 'Times New Roman', serif;
  color: #000;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.classic .resume-header {
  text-align: center;
  margin-bottom: 20px;
}

.resume.classic .resume-name {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 10px 0;
}

.resume.classic .resume-contact {
  font-size: 14px;
  line-height: 1.6;
}

.resume.classic .divider {
  border: none;
  border-top: 1px solid #000;
  margin: 15px 0;
}

.resume.classic .section-title {
  font-size: 18px;
  font-weight: 700;
  margin: 20px 0 15px 0;
  text-transform: uppercase;
}

.resume.classic .section-content {
  margin-bottom: 20px;
}

.resume.classic .skills-list {
  columns: 2;
  list-style-type: disc;
  padding-left: 20px;
  margin: 0;
}

.resume.classic .experience-item,
.resume.classic .education-item {
  margin-bottom: 20px;
}

.resume.classic .job-title,
.resume.classic .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
}

.resume.classic .employer,
.resume.classic .institution {
  font-weight: 700;
}

.resume.classic .date {
  font-style: italic;
  margin-bottom: 10px;
}

.resume.classic .description {
  font-size: 14px;
}
'''

    def get_minimalist_html(self):
        return '''
<div class="resume minimalist">
  <header class="resume-header">
    <h1 class="resume-name">{first_name} {last_name}</h1>
    <div class="resume-contact">
      <span>{email}</span>
      <span>{phone}</span>
      <span>{city}, {state}</span>
      <span>{linkedin}</span>
    </div>
  </header>

  <section class="resume-summary">
    <h2 class="section-title">Summary</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Skills</h2>
    <div class="section-content">
      <ul class="skills-list">
        <!-- Skills will be populated dynamically -->
      </ul>
    </div>
  </section>
</div>
'''

    def get_minimalist_css(self):
        return '''
.resume.minimalist {
  font-family: 'Helvetica', 'Arial', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.resume.minimalist .resume-header {
  margin-bottom: 40px;
}

.resume.minimalist .resume-name {
  font-size: 28px;
  font-weight: 300;
  margin: 0 0 15px 0;
  letter-spacing: 1px;
}

.resume.minimalist .resume-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.resume.minimalist .section-title {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 30px 0 15px 0;
  color: #999;
}

.resume.minimalist .section-content {
  margin-bottom: 30px;
}

.resume.minimalist .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.minimalist .skills-list li {
  font-size: 14px;
  border-bottom: 1px solid #eee;
  padding-bottom: 3px;
}

.resume.minimalist .experience-item,
.resume.minimalist .education-item {
  margin-bottom: 25px;
}

.resume.minimalist .job-title,
.resume.minimalist .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
}

.resume.minimalist .employer,
.resume.minimalist .institution {
  font-weight: 400;
}

.resume.minimalist .date {
  color: #999;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.minimalist .description {
  font-size: 14px;
  color: #555;
}
'''

    def get_elegant_html(self):
        return '''
<div class="resume elegant">
  <header class="resume-header">
    <div class="header-main">
      <h1 class="resume-name">{first_name} {last_name}</h1>
      <p class="resume-title">Professional Title</p>
    </div>
    <div class="resume-contact">
      <div class="contact-item"><i class="icon-email"></i>{email}</div>
      <div class="contact-item"><i class="icon-phone"></i>{phone}</div>
      <div class="contact-item"><i class="icon-location"></i>{city}, {state}</div>
      <div class="contact-item"><i class="icon-linkedin"></i>{linkedin}</div>
    </div>
  </header>

  <section class="resume-summary">
    <h2 class="section-title">Profile</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Expertise</h2>
    <div class="section-content">
      <ul class="skills-list">
        <!-- Skills will be populated dynamically -->
      </ul>
    </div>
  </section>
</div>
'''

    def get_elegant_css(self):
        return '''
.resume.elegant {
  font-family: 'Garamond', 'Georgia', serif;
  color: #333;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.resume.elegant .resume-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  border-bottom: 1px solid #8b0000;
  padding-bottom: 20px;
}

.resume.elegant .resume-name {
  font-size: 32px;
  font-weight: 400;
  color: #8b0000;
  margin: 0 0 5px 0;
  letter-spacing: 1px;
}

.resume.elegant .resume-title {
  font-size: 18px;
  font-style: italic;
  color: #666;
  margin: 0;
}

.resume.elegant .resume-contact {
  font-size: 14px;
  line-height: 1.8;
  text-align: right;
}

.resume.elegant .contact-item {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.resume.elegant .section-title {
  font-size: 20px;
  font-weight: 400;
  color: #8b0000;
  margin: 30px 0 15px 0;
  letter-spacing: 1px;
}

.resume.elegant .section-content {
  margin-bottom: 30px;
}

.resume.elegant .skills-list {
  columns: 2;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.elegant .skills-list li {
  margin-bottom: 8px;
  position: relative;
  padding-left: 15px;
}

.resume.elegant .skills-list li:before {
  content: "•";
  color: #8b0000;
  position: absolute;
  left: 0;
}

.resume.elegant .experience-item,
.resume.elegant .education-item {
  margin-bottom: 25px;
}

.resume.elegant .job-title,
.resume.elegant .degree {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 5px;
}

.resume.elegant .employer,
.resume.elegant .institution {
  font-style: italic;
}

.resume.elegant .date {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.elegant .description {
  font-size: 15px;
}
'''

    def get_bold_html(self):
        return '''
<div class="resume bold">
  <header class="resume-header">
    <h1 class="resume-name">{first_name} {last_name}</h1>
    <div class="resume-contact">
      <div class="contact-item">{email}</div>
      <div class="contact-item">{phone}</div>
      <div class="contact-item">{city}, {state}</div>
      <div class="contact-item">{linkedin}</div>
    </div>
  </header>

  <section class="resume-summary">
    <h2 class="section-title">Professional Summary</h2>
    <div class="section-content">
      <p>{summary}</p>
    </div>
  </section>

  <section class="resume-experience">
    <h2 class="section-title">Work Experience</h2>
    <div class="section-content">
      <!-- Experience items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-education">
    <h2 class="section-title">Education</h2>
    <div class="section-content">
      <!-- Education items will be populated dynamically -->
    </div>
  </section>

  <section class="resume-skills">
    <h2 class="section-title">Skills & Expertise</h2>
    <div class="section-content">
      <ul class="skills-list">
        <!-- Skills will be populated dynamically -->
      </ul>
    </div>
  </section>
</div>
'''

    def get_bold_css(self):
        return '''
.resume.bold {
  font-family: 'Arial', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.bold .resume-header {
  background-color: #0066cc;
  color: white;
  padding: 30px;
  margin: -30px -30px 30px -30px;
  text-align: center;
}

.resume.bold .resume-name {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.resume.bold .resume-contact {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 14px;
}

.resume.bold .section-title {
  font-size: 20px;
  font-weight: 700;
  color: #0066cc;
  text-transform: uppercase;
  margin: 30px 0 15px 0;
  border-bottom: 2px solid #0066cc;
  padding-bottom: 5px;
}

.resume.bold .section-content {
  margin-bottom: 25px;
}

.resume.bold .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.bold .skills-list li {
  background-color: #f0f0f0;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.resume.bold .experience-item,
.resume.bold .education-item {
  margin-bottom: 25px;
}

.resume.bold .job-title,
.resume.bold .degree {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 5px;
  color: #0066cc;
}

.resume.bold .employer,
.resume.bold .institution {
  font-weight: 600;
  font-size: 16px;
}

.resume.bold .date {
  font-weight: 600;
  color: #666;
  margin-bottom: 10px;
}

.resume.bold .description {
  font-size: 14px;
}
'''

    def get_modern_executive_html(self):
        return '''
<div class="resume modern-executive">
  <div class="resume-sidebar">
    <div class="profile-img"></div>
    <div class="sidebar-content">
      <div class="contact-info">
        <h3>Contact</h3>
        <div class="contact-item"><i class="icon-email"></i>{email}</div>
        <div class="contact-item"><i class="icon-phone"></i>{phone}</div>
        <div class="contact-item"><i class="icon-location"></i>{city}, {state}</div>
        <div class="contact-item"><i class="icon-linkedin"></i>{linkedin}</div>
      </div>

      <div class="skills-section">
        <h3>Skills</h3>
        <ul class="skills-list">
          <!-- Skills will be populated dynamically -->
        </ul>
      </div>
    </div>
  </div>

  <div class="resume-main">
    <header class="resume-header">
      <h1 class="resume-name">{first_name} {last_name}</h1>
      <p class="resume-title">Executive Professional</p>
    </header>

    <section class="resume-summary">
      <h2 class="section-title">Executive Profile</h2>
      <div class="section-content">
        <p>{summary}</p>
      </div>
    </section>

    <section class="resume-experience">
      <h2 class="section-title">Professional Experience</h2>
      <div class="section-content">
        <!-- Experience items will be populated dynamically -->
      </div>
    </section>

    <section class="resume-education">
      <h2 class="section-title">Education</h2>
      <div class="section-content">
        <!-- Education items will be populated dynamically -->
      </div>
    </section>
  </div>
</div>
'''

    def get_modern_executive_css(self):
        return '''
.resume.modern-executive {
  font-family: 'Calibri', 'Segoe UI', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  background-color: #fff;
}

.resume.modern-executive .resume-sidebar {
  width: 30%;
  background-color: #1e5631;
  color: white;
  padding: 30px 20px;
}

.resume.modern-executive .profile-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  margin: 0 auto 20px;
}

.resume.modern-executive .sidebar-content {
  margin-top: 30px;
}

.resume.modern-executive .contact-info h3,
.resume.modern-executive .skills-section h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 5px;
}

.resume.modern-executive .contact-item {
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.modern-executive .skills-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.modern-executive .skills-list li {
  margin-bottom: 8px;
  font-size: 14px;
  position: relative;
  padding-left: 15px;
}

.resume.modern-executive .skills-list li:before {
  content: "•";
  position: absolute;
  left: 0;
}

.resume.modern-executive .resume-main {
  width: 70%;
  padding: 30px;
}

.resume.modern-executive .resume-header {
  margin-bottom: 30px;
}

.resume.modern-executive .resume-name {
  font-size: 28px;
  font-weight: 700;
  color: #1e5631;
  margin: 0 0 5px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.resume.modern-executive .resume-title {
  font-size: 18px;
  color: #666;
  margin: 0;
}

.resume.modern-executive .section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e5631;
  margin: 25px 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.resume.modern-executive .section-content {
  margin-bottom: 25px;
}

.resume.modern-executive .experience-item,
.resume.modern-executive .education-item {
  margin-bottom: 20px;
}

.resume.modern-executive .job-title,
.resume.modern-executive .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
  color: #1e5631;
}

.resume.modern-executive .employer,
.resume.modern-executive .institution {
  font-weight: 600;
}

.resume.modern-executive .date {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.modern-executive .description {
  font-size: 14px;
}
'''

    # Add the remaining template methods...
    def get_classic_blue_html(self):
        # Similar to classic but with blue accents
        return self.get_classic_html()

    def get_classic_blue_css(self):
        return '''
.resume.classic {
  font-family: 'Times New Roman', serif;
  color: #000;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.classic .resume-header {
  text-align: center;
  margin-bottom: 20px;
}

.resume.classic .resume-name {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #2b6cb0;
}

.resume.classic .resume-contact {
  font-size: 14px;
  line-height: 1.6;
}

.resume.classic .divider {
  border: none;
  border-top: 1px solid #2b6cb0;
  margin: 15px 0;
}

.resume.classic .section-title {
  font-size: 18px;
  font-weight: 700;
  margin: 20px 0 15px 0;
  text-transform: uppercase;
  color: #2b6cb0;
}

.resume.classic .section-content {
  margin-bottom: 20px;
}

.resume.classic .skills-list {
  columns: 2;
  list-style-type: disc;
  padding-left: 20px;
  margin: 0;
}

.resume.classic .experience-item,
.resume.classic .education-item {
  margin-bottom: 20px;
}

.resume.classic .job-title,
.resume.classic .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
  color: #2b6cb0;
}

.resume.classic .employer,
.resume.classic .institution {
  font-weight: 700;
}

.resume.classic .date {
  font-style: italic;
  margin-bottom: 10px;
}

.resume.classic .description {
  font-size: 14px;
}
'''

    def get_corporate_gray_html(self):
        # Similar to corporate but with gray accents
        return self.get_corporate_html()

    def get_corporate_gray_css(self):
        return '''
.resume.corporate {
  font-family: 'Arial', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.corporate .resume-header {
  text-align: center;
  margin-bottom: 30px;
}

.resume.corporate .resume-name {
  font-size: 24px;
  font-weight: 700;
  color: #4a5568;
  margin: 0 0 10px 0;
}

.resume.corporate .resume-contact {
  font-size: 14px;
  line-height: 1.6;
}

.resume.corporate .section-title {
  font-size: 16px;
  font-weight: 700;
  color: #4a5568;
  text-transform: uppercase;
  margin: 25px 0 15px 0;
  border-bottom: 1px solid #4a5568;
  padding-bottom: 5px;
}

.resume.corporate .section-content {
  margin-bottom: 20px;
}

.resume.corporate .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.corporate .skills-list li {
  background-color: #f7fafc;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 14px;
  border: 1px solid #e2e8f0;
}

.resume.corporate .experience-item,
.resume.corporate .education-item {
  margin-bottom: 20px;
}

.resume.corporate .job-title,
.resume.corporate .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
  color: #4a5568;
}

.resume.corporate .employer,
.resume.corporate .institution {
  font-weight: 700;
}

.resume.corporate .date {
  color: #718096;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.corporate .description {
  font-size: 14px;
}
'''

    def get_minimalist_black_html(self):
        # Similar to minimalist but with black accents
        return self.get_minimalist_html()

    def get_minimalist_black_css(self):
        return '''
.resume.minimalist {
  font-family: 'Helvetica', 'Arial', sans-serif;
  color: #000;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.resume.minimalist .resume-header {
  margin-bottom: 40px;
}

.resume.minimalist .resume-name {
  font-size: 28px;
  font-weight: 300;
  margin: 0 0 15px 0;
  letter-spacing: 1px;
}

.resume.minimalist .resume-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 14px;
  color: #000;
}

.resume.minimalist .section-title {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 30px 0 15px 0;
  color: #000;
}

.resume.minimalist .section-content {
  margin-bottom: 30px;
}

.resume.minimalist .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.minimalist .skills-list li {
  font-size: 14px;
  border-bottom: 1px solid #000;
  padding-bottom: 3px;
}

.resume.minimalist .experience-item,
.resume.minimalist .education-item {
  margin-bottom: 25px;
}

.resume.minimalist .job-title,
.resume.minimalist .degree {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 5px;
}

.resume.minimalist .employer,
.resume.minimalist .institution {
  font-weight: 400;
}

.resume.minimalist .date {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.minimalist .description {
  font-size: 14px;
  color: #333;
}
'''

    def get_elegant_navy_html(self):
        # Similar to elegant but with navy accents
        return self.get_elegant_html()

    def get_elegant_navy_css(self):
        return '''
.resume.elegant {
  font-family: 'Garamond', 'Georgia', serif;
  color: #333;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.resume.elegant .resume-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  border-bottom: 1px solid #1a365d;
  padding-bottom: 20px;
}

.resume.elegant .resume-name {
  font-size: 32px;
  font-weight: 400;
  color: #1a365d;
  margin: 0 0 5px 0;
  letter-spacing: 1px;
}

.resume.elegant .resume-title {
  font-size: 18px;
  font-style: italic;
  color: #666;
  margin: 0;
}

.resume.elegant .resume-contact {
  font-size: 14px;
  line-height: 1.8;
  text-align: right;
}

.resume.elegant .contact-item {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.resume.elegant .section-title {
  font-size: 20px;
  font-weight: 400;
  color: #1a365d;
  margin: 30px 0 15px 0;
  letter-spacing: 1px;
}

.resume.elegant .section-content {
  margin-bottom: 30px;
}

.resume.elegant .skills-list {
  columns: 2;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.elegant .skills-list li {
  margin-bottom: 8px;
  position: relative;
  padding-left: 15px;
}

.resume.elegant .skills-list li:before {
  content: "•";
  color: #1a365d;
  position: absolute;
  left: 0;
}

.resume.elegant .experience-item,
.resume.elegant .education-item {
  margin-bottom: 25px;
}

.resume.elegant .job-title,
.resume.elegant .degree {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 5px;
  color: #1a365d;
}

.resume.elegant .employer,
.resume.elegant .institution {
  font-style: italic;
}

.resume.elegant .date {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.resume.elegant .description {
  font-size: 15px;
}
'''

    def get_bold_green_html(self):
        # Similar to bold but with green accents
        return self.get_bold_html()

    def get_bold_green_css(self):
        return '''
.resume.bold {
  font-family: 'Arial', sans-serif;
  color: #333;
  line-height: 1.5;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
}

.resume.bold .resume-header {
  background-color: #2f855a;
  color: white;
  padding: 30px;
  margin: -30px -30px 30px -30px;
  text-align: center;
}

.resume.bold .resume-name {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.resume.bold .resume-contact {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 14px;
}

.resume.bold .section-title {
  font-size: 20px;
  font-weight: 700;
  color: #2f855a;
  text-transform: uppercase;
  margin: 30px 0 15px 0;
  border-bottom: 2px solid #2f855a;
  padding-bottom: 5px;
}

.resume.bold .section-content {
  margin-bottom: 25px;
}

.resume.bold .skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.resume.bold .skills-list li {
  background-color: #f0fff4;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  color: #2f855a;
  border: 1px solid #c6f6d5;
}

.resume.bold .experience-item,
.resume.bold .education-item {
  margin-bottom: 25px;
}

.resume.bold .job-title,
.resume.bold .degree {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 5px;
  color: #2f855a;
}

.resume.bold .employer,
.resume.bold .institution {
  font-weight: 600;
  font-size: 16px;
}

.resume.bold .date {
  font-weight: 600;
  color: #666;
  margin-bottom: 10px;
}

.resume.bold .description {
  font-size: 14px;
}
'''

