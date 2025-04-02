from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Count, Q
from django.contrib import messages
from django.urls import reverse

from .models import ResumeTemplate, TemplateCategory, TemplateColor, UserTemplateSelection
from .forms import TemplateFilterForm

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResumeTemplate, UserTemplateSelection
from resume.models import  Resume, ResumeSection

# Add these to your views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.shortcuts import render, get_object_or_404
from home.models import Resume  # Assuming you have a Resume model

# templates_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
from django.template.loader import get_template
from xhtml2pdf import pisa  # You'll need to install this: pip install xhtml2pdf


def resume_download(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    # Set the context for the template
    context = {
        'resume': resume,
        'active_tab': 'download',
    }

    # If the user is just viewing the download page
    if request.method == 'GET':
        return render(request, 'templates_app/resume_download.html', context)

    # If the user has submitted the form to actually download the PDF
    elif request.method == 'POST':
        # Get the selected format
        selected_format = request.POST.get('format', 'pdf')

        if selected_format == 'pdf':
            # Create a PDF from the resume
            template = get_template('templates_app/resume_pdf_template.html')
            html = template.render({'resume': resume})

            # Create a file-like buffer to receive PDF data
            buffer = io.BytesIO()

            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(html, dest=buffer)

            # If error creating PDF
            if pisa_status.err:
                return HttpResponse('We had some errors with creating the PDF <pre>' + html + '</pre>')

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)

            # Create the HTTP response with PDF
            response = HttpResponse(buffer, content_type='application/pdf')
            filename = f"{resume.title.replace(' ', '_')}_resume.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        elif selected_format == 'docx':
            # This is a placeholder for DOCX generation
            # You would implement actual DOCX generation here
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            filename = f"{resume.title.replace(' ', '_')}_resume.docx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.write(b'DOCX content would go here')  # Placeholder
            return response

        elif selected_format == 'txt':
            # Simple text version of the resume
            # Since we don't know the exact structure, we'll create a basic text file
            # with the information we do know
            content = f"""
RESUME: {resume.title}
Created: {resume.created_at.strftime('%B %d, %Y')}
Last Updated: {resume.updated_at.strftime('%B %d, %Y')}

"""

            # Try to get personal information if it exists
            try:
                # Check if there's a related personal_info model
                if hasattr(resume, 'personal_info'):
                    personal_info = resume.personal_info
                    content += "PERSONAL INFORMATION\n"
                    for field in personal_info._meta.fields:
                        if field.name not in ['id', 'resume', 'created_at', 'updated_at']:
                            value = getattr(personal_info, field.name, '')
                            if value:
                                content += f"{field.verbose_name}: {value}\n"
                    content += "\n"
            except Exception as e:
                # If there's an error, just continue without this section
                pass

            # Try to get sections if they exist
            try:
                # Check if there's a related sections queryset
                if hasattr(resume, 'sections'):
                    sections = resume.sections.all()
                    for section in sections:
                        section_title = getattr(section, 'title', 'Section')
                        content += f"{section_title.upper()}\n"

                        # Try to get section content
                        section_content = getattr(section, 'content', '')
                        if section_content:
                            content += f"{section_content}\n"

                        # Try to get items if this is a list-type section
                        try:
                            if hasattr(section, 'items'):
                                items = section.items.all()
                                for item in items:
                                    # Try common field names for items
                                    for field_name in ['title', 'subtitle', 'date_range', 'description']:
                                        value = getattr(item, field_name, '')
                                        if value:
                                            content += f"{value}\n"
                                    content += "\n"
                        except Exception:
                            pass

                        content += "\n"
            except Exception as e:
                # If there's an error, just continue without this section
                pass

            # Add a note about the resume design
            content += f"""
DESIGN INFORMATION
Template: {resume.template.name if resume.template else 'Custom'}
Primary Color: {resume.primary_color}
Font Family: {resume.get_font_family_display()}
Font Size: {resume.get_font_size_display()}
"""

            response = HttpResponse(content, content_type='text/plain')
            filename = f"{resume.title.replace(' ', '_')}_resume.txt"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        else:
            # Default case - return to the download page with an error message
            context['error'] = f"Unsupported format: {selected_format}"
            return render(request, 'templates_app/resume_download.html', context)


def resume_design(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    # Add any other context data you need
    context = {
        'resume': resume,
        'active_tab': 'design',
    }
    return render(request, 'templates_app/resume_design.html', context)


@login_required
def get_section(request, section_id):
    """Get section data for editing"""
    section = get_object_or_404(ResumeSection, id=section_id)

    # Check if user owns this section
    if section.resume.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Generate form HTML based on section type
    form_html = generate_section_form(section)

    return JsonResponse({
        'section': {
            'id': section.id,
            'name': section.name,
            'content': section.content
        },
        'form_html': form_html
    })


@login_required
@require_POST
def update_section(request, section_id):
    """Update section content"""
    section = get_object_or_404(ResumeSection, id=section_id)

    # Check if user owns this section
    if section.resume.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Process form data based on section type
    if section.name == 'Contact Information':
        section.content = {
            'name': request.POST.get('name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'location': request.POST.get('location', '')
        }
    elif section.name == 'Professional Summary':
        section.content = {
            'summary': request.POST.get('summary', '')
        }
    elif section.name == 'Work Experience':
        # Process multiple job entries
        jobs = []
        job_count = int(request.POST.get('job_count', 0))

        for i in range(job_count):
            jobs.append({
                'title': request.POST.get(f'job_title_{i}', ''),
                'company': request.POST.get(f'job_company_{i}', ''),
                'dates': request.POST.get(f'job_dates_{i}', ''),
                'description': request.POST.get(f'job_description_{i}', '')
            })

        section.content = {'jobs': jobs}
    elif section.name == 'Education':
        # Process multiple education entries
        education = []
        edu_count = int(request.POST.get('edu_count', 0))

        for i in range(edu_count):
            education.append({
                'degree': request.POST.get(f'edu_degree_{i}', ''),
                'institution': request.POST.get(f'edu_institution_{i}', ''),
                'dates': request.POST.get(f'edu_dates_{i}', ''),
                'description': request.POST.get(f'edu_description_{i}', '')
            })

        section.content = {'education': education}
    elif section.name == 'Skills':
        # Process skills as a list
        skills_text = request.POST.get('skills', '')
        skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
        section.content = {'skills': skills}
    else:
        # Generic section
        section.content = {
            'text': request.POST.get('content', '')
        }

    section.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
def update_section_order(request, resume_id):
    """Update the order of resume sections"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    section_order = json.loads(request.POST.get('section_order', '[]'))

    # Update order for each section
    for index, section_id in enumerate(section_order):
        section = get_object_or_404(ResumeSection, id=section_id, resume=resume)
        section.order = index + 1
        section.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
def update_color_scheme(request, resume_id):
    """Update resume color scheme"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    color_id = request.POST.get('color_id')
    color_scheme = get_object_or_404(TemplateColor, id=color_id, template=resume.template)

    resume.color_scheme = color_scheme
    resume.save()

    return JsonResponse({
        'success': True,
        'primary_color': color_scheme.primary_color,
        'secondary_color': color_scheme.secondary_color
    })


@login_required
@require_POST
def save_resume(request, resume_id):
    """Save resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Update last_updated timestamp
    resume.save()

    return JsonResponse({'success': True})


@login_required
def preview_resume(request, resume_id):
    """Preview resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Get all sections for this resume
    sections = resume.sections.all().order_by('order')

    return render(request, 'templates_app/resume_preview.html', {
        'resume': resume,
        'template': resume.template,
        'color_scheme': resume.color_scheme,
        'sections': sections,
    })


def generate_section_form(section):
    """Generate HTML form for editing a section based on its type"""
    if section.name == 'Contact Information':
        return f"""
        <form id="section-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="">
            <div class="form-group">
                <label for="name">Full Name</label>
                <input type="text" id="name" name="name" class="form-control" 
                       value="{section.content.get('name', '')}">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" class="form-control"
                       value="{section.content.get('email', '')}">
            </div>
            <div class="form-group">
                <label for="phone">Phone</label>
                <input type="text" id="phone" name="phone" class="form-control"
                       value="{section.content.get('phone', '')}">
            </div>
            <div class="form-group">
                <label for="location">Location</label>
                <input type="text" id="location" name="location" class="form-control"
                       value="{section.content.get('location', '')}">
            </div>
        </form>
        """
    elif section.name == 'Professional Summary':
        return f"""
        <form id="section-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="">
            <div class="form-group">
                <label for="summary">Professional Summary</label>
                <textarea id="summary" name="summary" class="form-control" rows="5">{section.content.get('summary', '')}</textarea>
            </div>
        </form>
        """
    elif section.name == 'Work Experience':
        jobs = section.content.get('jobs', [])
        if not jobs:
            jobs = [{'title': '', 'company': '', 'dates': '', 'description': ''}]

        jobs_html = ""
        for i, job in enumerate(jobs):
            jobs_html += f"""
            <div class="job-entry-form" data-index="{i}">
                <h4>Job #{i + 1}</h4>
                <div class="form-group">
                    <label for="job_title_{i}">Job Title</label>
                    <input type="text" id="job_title_{i}" name="job_title_{i}" class="form-control" 
                           value="{job.get('title', '')}">
                </div>
                <div class="form-group">
                    <label for="job_company_{i}">Company</label>
                    <input type="text" id="job_company_{i}" name="job_company_{i}" class="form-control"
                           value="{job.get('company', '')}">
                </div>
                <div class="form-group">
                    <label for="job_dates_{i}">Dates</label>
                    <input type="text" id="job_dates_{i}" name="job_dates_{i}" class="form-control"
                           value="{job.get('dates', '')}">
                </div>
                <div class="form-group">
                    <label for="job_description_{i}">Description</label>
                    <textarea id="job_description_{i}" name="job_description_{i}" class="form-control" rows="3">{job.get('description', '')}</textarea>
                </div>
                <button type="button" class="btn btn-outline btn-sm remove-job">Remove</button>
            </div>
            """

        return f"""
        <form id="section-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="">
            <input type="hidden" name="job_count" value="{len(jobs)}" id="job_count">
            <div id="jobs-container">
                {jobs_html}
            </div>
            <button type="button" id="add-job" class="btn btn-outline btn-sm">Add Another Job</button>
        </form>
        <script>
            $(document).ready(function() {{
                // Add job
                $("#add-job").click(function() {{
                    const index = $(".job-entry-form").length;
                    const newJob = `
                        <div class="job-entry-form" data-index="${{index}}">
                            <h4>Job #${{index+1}}</h4>
                            <div class="form-group">
                                <label for="job_title_${{index}}">Job Title</label>
                                <input type="text" id="job_title_${{index}}" name="job_title_${{index}}" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="job_company_${{index}}">Company</label>
                                <input type="text" id="job_company_${{index}}" name="job_company_${{index}}" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="job_dates_${{index}}">Dates</label>
                                <input type="text" id="job_dates_${{index}}" name="job_dates_${{index}}" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="job_description_${{index}}">Description</label>
                                <textarea id="job_description_${{index}}" name="job_description_${{index}}" class="form-control" rows="3"></textarea>
                            </div>
                            <button type="button" class="btn btn-outline btn-sm remove-job">Remove</button>
                        </div>
                    `;
                    $("#jobs-container").append(newJob);
                    $("#job_count").val(index + 1);
                }});

                // Remove job
                $(document).on("click", ".remove-job", function() {{
                    $(this).closest(".job-entry-form").remove();
                    // Update job count
                    $("#job_count").val($(".job-entry-form").length);
                    // Renumber jobs
                    $(".job-entry-form").each(function(index) {{
                        $(this).find("h4").text(`Job #${{index+1}}`);
                    }});
                }});
            }});
        </script>
        """
    # Add similar form generators for other section types

    # Default generic form
    return f"""
    <form id="section-form">
        <input type="hidden" name="csrfmiddlewaretoken" value="">
        <div class="form-group">
            <label for="content">Content</label>
            <textarea id="content" name="content" class="form-control" rows="5">{section.content.get('text', '')}</textarea>
        </div>
    </form>
    """


@login_required
def resume_editor(request):
    """Resume editor view"""
    # Get template from query parameter
    template_slug = request.GET.get('template')
    if not template_slug:
        messages.error(request, "No template selected.")
        return redirect('template_list')

    # Import the correct ResumeTemplate model
    from dashboard.models import ResumeTemplate

    # Get the template object using the slug
    try:
        template = ResumeTemplate.objects.get(slug=template_slug)
    except ResumeTemplate.DoesNotExist:
        messages.error(request, f"Template '{template_slug}' not found.")
        return redirect('templates_app:template_list')

    # Get or create a resume for this user and template
    try:
        # Make sure to query using the template instance, not a string
        resume = Resume.objects.get(
            user=request.user,
            template=template  # This should be a ResumeTemplate instance
        )
    except Resume.DoesNotExist:
        # Create a new resume with the template
        resume = Resume.objects.create(
            user=request.user,
            template=template,
            title=f"My {template.name} Resume",
            full_name=request.user.get_full_name() or request.user.username,
            email=request.user.email,
            primary_color=template.default_primary_color if hasattr(template, 'default_primary_color') else '#2D9CDB',
            secondary_color=template.default_secondary_color if hasattr(template,
                                                                        'default_secondary_color') else '#3498DB'
        )

    # Get sections data (assuming you have related models for sections)
    # Adjust this based on your actual models
    education_entries = resume.education_entries.all() if hasattr(resume, 'education_entries') else []
    experience_entries = resume.experience_entries.all() if hasattr(resume, 'experience_entries') else []
    skill_entries = resume.skill_entries.all() if hasattr(resume, 'skill_entries') else []

    return render(request, 'resume_editor.html', {
        'resume': resume,
        'template': template,
        'education_entries': education_entries,
        'experience_entries': experience_entries,
        'skill_entries': skill_entries,
    })


class TemplateListView(ListView):
    """Display all resume templates with filtering options"""
    model = ResumeTemplate
    template_name = 'templates_app/template_list.html'
    context_object_name = 'templates'
    paginate_by = 12

    def get_queryset(self):
        queryset = ResumeTemplate.objects.all()

        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filter by ATS-friendly
        ats_friendly = self.request.GET.get('ats_friendly')
        if ats_friendly == 'true':
            queryset = queryset.filter(is_ats_friendly=True)

        # Filter by photo option
        has_photo = self.request.GET.get('has_photo')
        if has_photo == 'true':
            queryset = queryset.filter(has_photo=True)
        elif has_photo == 'false':
            queryset = queryset.filter(has_photo=False)

        # Filter by premium status
        premium = self.request.GET.get('premium')
        if premium == 'true':
            queryset = queryset.filter(is_premium=True)
        elif premium == 'false':
            queryset = queryset.filter(is_premium=False)

        # Search by name
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TemplateCategory.objects.all()
        context['filter_form'] = TemplateFilterForm(self.request.GET)

        # Get active category for highlighting
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['active_category'] = get_object_or_404(TemplateCategory, slug=category_slug)

        return context


class TemplateDetailView(DetailView):
    """Display details of a specific template"""
    model = ResumeTemplate
    template_name = 'templates_app/template_detail.html'
    context_object_name = 'template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = self.get_object()

        # Get color schemes
        context['colors'] = template.colors.all()

        # Get default color scheme
        context['default_color'] = template.colors.filter(is_default=True).first()

        # Get template sections
        context['sections'] = template.sections.all()

        # Check if user has used this template before
        if self.request.user.is_authenticated:
            context['user_has_used'] = UserTemplateSelection.objects.filter(
                user=self.request.user,
                template=template
            ).exists()

        return context


@login_required
def select_template(request, slug):
    """Select a template to create a resume"""
    template = get_object_or_404(ResumeTemplate, slug=slug)

    # Check if template is premium and user has access
    if template.is_premium and not request.user.profile.has_premium_access:
        messages.error(request, "This is a premium template. Please upgrade to access it.")
        return redirect('template_list')

    # Get color scheme if provided
    color_scheme = None
    color_id = request.POST.get('color_scheme')
    if color_id:
        color_scheme = get_object_or_404(TemplateColor, id=color_id, template=template)
    else:
        # Use default color scheme
        color_scheme = template.colors.filter(is_default=True).first()

    # Create or update user template selection
    selection, created = UserTemplateSelection.objects.update_or_create(
        user=request.user,
        template=template,
        defaults={'color_scheme': color_scheme}
    )

    # Increment template popularity
    template.increment_popularity()

    # Redirect to resume editor with the selected template
    return redirect(reverse('templates_app:resume_editor') + f'?template={template.slug}')


def template_preview(request, slug):
    """Preview a template with sample data"""
    template = get_object_or_404(ResumeTemplate, slug=slug)

    # Get color scheme if provided
    color_id = request.GET.get('color')
    if color_id:
        color = get_object_or_404(TemplateColor, id=color_id, template=template)
    else:
        # Use default color scheme
        color = template.colors.filter(is_default=True).first()

    context = {
        'template': template,
        'color': color,
        'is_preview': True,
    }

    return render(request, 'templates_app/template_preview.html', context)


def template_filter_ajax(request):
    """AJAX endpoint for filtering templates"""
    category_slug = request.GET.get('category')
    ats_friendly = request.GET.get('ats_friendly')
    has_photo = request.GET.get('has_photo')
    premium = request.GET.get('premium')
    search_query = request.GET.get('q')

    templates = ResumeTemplate.objects.all()

    # Apply filters
    if category_slug:
        templates = templates.filter(categories__slug=category_slug)

    if ats_friendly == 'true':
        templates = templates.filter(is_ats_friendly=True)

    if has_photo == 'true':
        templates = templates.filter(has_photo=True)
    elif has_photo == 'false':
        templates = templates.filter(has_photo=False)

    if premium == 'true':
        templates = templates.filter(is_premium=True)
    elif premium == 'false':
        templates = templates.filter(is_premium=False)

    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Render template list partial
    html = render(request, 'templates_app/partials/template_grid.html', {
        'templates': templates
    }).content.decode('utf-8')

    return JsonResponse({
        'html': html,
        'count': templates.count()
    })


def subscription_plans(request):
    # Sample subscription plans data
    plans = [
        {
            'name': 'Basic',
            'price': '$9.99',
            'period': 'month',
            'features': [
                'Access to basic templates',
                'Email support',
                'Up to 3 projects',
                '1GB storage'
            ],
            'is_popular': False,
            'button_text': 'Get Started'
        },
        {
            'name': 'Pro',
            'price': '$19.99',
            'period': 'month',
            'features': [
                'Access to all templates',
                'Priority email support',
                'Up to 10 projects',
                '10GB storage',
                'Custom branding'
            ],
            'is_popular': True,
            'button_text': 'Get Pro'
        },
        {
            'name': 'Enterprise',
            'price': '$49.99',
            'period': 'month',
            'features': [
                'Access to all templates',
                'Phone and email support',
                'Unlimited projects',
                '100GB storage',
                'Custom branding',
                'API access',
                'Dedicated account manager'
            ],
            'is_popular': False,
            'button_text': 'Contact Sales'
        }
    ]

    return render(request, 'templates_app/contemporary/subscription_plans.html', {
        'plans': plans,
        'title': 'Subscription Plans'
    })



# Add this to your templates_app/views.py if you don't already have a home view
def home(request):
    return render(request, 'templates_app/contemporary/home.html')