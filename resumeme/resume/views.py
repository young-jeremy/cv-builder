from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView

from .models import (
    Resume, Education, Experience, Skill, Project,
    Certification, Language, Reference, CustomSection, ResumeExport
)
from .forms import (
    ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm,
    CertificationForm, LanguageForm, ReferenceForm, CustomSectionForm
)
from dashboard.models import ResumeTemplate

import json
import uuid
# from weasyprint import HTML, CSS
from django.conf import settings
import os
from docx import Document


@login_required
def resume_list(request):
    """Display all user's resumes."""
    resumes = Resume.objects.filter(user=request.user)

    context = {
        'resumes': resumes,
        'resume_count': resumes.count(),
    }
    return render(request, 'resume/resume_list.html', context)


@login_required
def create_resume(request):
    """Create a new resume."""
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            messages.success(request, 'Resume created successfully!')
            return redirect('resume:edit', slug=resume.slug)
    else:
        form = ResumeForm()

    context = {
        'form': form,
        'is_new': True,
    }
    return render(request, 'resume/resume_form.html', context)


@login_required
def resume_detail(request, slug):
    """View a resume."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)
    resume.increment_view_count()

    context = {
        'resume': resume,
    }
    return render(request, 'resume/resume_detail.html', context)


@login_required
def edit_resume(request, slug):
    """Edit a resume."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume updated successfully!')
            return redirect('resume:edit', slug=resume.slug)
    else:
        form = ResumeForm(instance=resume)

    # Get all resume sections
    education = resume.education.all()
    experiences = resume.experiences.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    languages = resume.languages.all()
    references = resume.references.all()
    custom_sections = resume.custom_sections.all()

    # Forms for adding new sections
    education_form = EducationForm()
    experience_form = ExperienceForm()
    skill_form = SkillForm()
    project_form = ProjectForm()
    certification_form = CertificationForm()
    language_form = LanguageForm()
    reference_form = ReferenceForm()
    custom_section_form = CustomSectionForm()

    context = {
        'resume': resume,
        'form': form,
        'education': education,
        'experiences': experiences,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'languages': languages,
        'references': references,
        'custom_sections': custom_sections,
        'education_form': education_form,
        'experience_form': experience_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'certification_form': certification_form,
        'language_form': language_form,
        'reference_form': reference_form,
        'custom_section_form': custom_section_form,
    }
    return render(request, 'resume/resume_edit.html', context)


@login_required
def delete_resume(request, slug):
    """Delete a resume."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)

    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('resume:list')

    context = {
        'resume': resume,
    }
    return render(request, 'resume/resume_confirm_delete.html', context)


@login_required
def duplicate_resume(request, slug):
    """Duplicate a resume."""
    original_resume = get_object_or_404(Resume, slug=slug, user=request.user)

    # Create a new resume with the same data
    new_resume = Resume.objects.create(
        user=request.user,
        title=f"Copy of {original_resume.title}",
        template=original_resume.template,
        full_name=original_resume.full_name,
        email=original_resume.email,
        phone=original_resume.phone,
        location=original_resume.location,
        headline=original_resume.headline,
        summary=original_resume.summary,
        primary_color=original_resume.primary_color,
        secondary_color=original_resume.secondary_color,
        font_family=original_resume.font_family,
    )

    # Copy profile photo if exists
    if original_resume.profile_photo:
        # Create a new file with a unique name
        file_name = os.path.basename(original_resume.profile_photo.name)
        name, ext = os.path.splitext(file_name)
        new_name = f"{name}_{uuid.uuid4().hex[:6]}{ext}"

        # Save the file to the new resume
        from django.core.files.base import ContentFile
        new_resume.profile_photo.save(
            new_name,
            ContentFile(original_resume.profile_photo.read())
        )

    # Duplicate all sections
    for education in original_resume.education.all():
        Education.objects.create(
            resume=new_resume,
            institution=education.institution,
            degree=education.degree,
            field_of_study=education.field_of_study,
            location=education.location,
            start_date=education.start_date,
            end_date=education.end_date,
            current=education.current,
            description=education.description,
            gpa=education.gpa,
            order=education.order,
        )

    for experience in original_resume.experiences.all():
        Experience.objects.create(
            resume=new_resume,
            company=experience.company,
            title=experience.title,
            location=experience.location,
            start_date=experience.start_date,
            end_date=experience.end_date,
            current=experience.current,
            description=experience.description,
            order=experience.order,
        )

    for skill in original_resume.skills.all():
        Skill.objects.create(
            resume=new_resume,
            name=skill.name,
            level=skill.level,
            order=skill.order,
        )

    for project in original_resume.projects.all():
        Project.objects.create(
            resume=new_resume,
            title=project.title,
            description=project.description,
            url=project.url,
            start_date=project.start_date,
            end_date=project.end_date,
            current=project.current,
            order=project.order,
        )

    for certification in original_resume.certifications.all():
        Certification.objects.create(
            resume=new_resume,
            name=certification.name,
            issuing_organization=certification.issuing_organization,
            issue_date=certification.issue_date,
            expiration_date=certification.expiration_date,
            credential_id=certification.credential_id,
            credential_url=certification.credential_url,
            order=certification.order,
        )

    for language in original_resume.languages.all():
        Language.objects.create(
            resume=new_resume,
            name=language.name,
            proficiency=language.proficiency,
            order=language.order,
        )

    for reference in original_resume.references.all():
        Reference.objects.create(
            resume=new_resume,
            name=reference.name,
            company=reference.company,
            title=reference.title,
            email=reference.email,
            phone=reference.phone,
            reference_text=reference.reference_text,
            order=reference.order,
        )

    for custom_section in original_resume.custom_sections.all():
        CustomSection.objects.create(
            resume=new_resume,
            title=custom_section.title,
            content=custom_section.content,
            order=custom_section.order,
        )

    messages.success(request, 'Resume duplicated successfully!')
    return redirect('resume:edit', slug=new_resume.slug)


@login_required
def export_resume(request, slug, format='pdf'):
    """Export a resume to PDF or DOCX."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)

    # Check if user has permission to export (based on subscription)
    if hasattr(request.user, 'subscription'):
        subscription = request.user.subscription
        if not subscription.is_active:
            messages.error(request, 'Your subscription has expired. Please renew to export resumes.')
            return redirect('resume:detail', slug=resume.slug)

    # Increment download count
    resume.increment_download_count()

    if format == 'pdf':
        # Generate PDF
        html_string = render_to_string('resume/export/pdf_template.html', {'resume': resume})

        # Create a PDF file
        pdf_file = HTML(string=html_string).write_pdf(
            stylesheets=[CSS(settings.STATIC_ROOT + '/css/pdf_export.css')]
        )

        # Create a response with the PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.slug}.pdf"'

        # Save export record
        ResumeExport.objects.create(
            resume=resume,
            user=request.user,
            format='pdf',
        )

        return response

    elif format == 'docx':
        # Generate DOCX
        document = Document()

        # Add resume content to the document
        document.add_heading(resume.full_name, 0)

        if resume.headline:
            document.add_paragraph(resume.headline)

        # Contact info
        contact_info = document.add_paragraph()
        if resume.email:
            contact_info.add_run(resume.email)
            contact_info.add_run(' | ')
        if resume.phone:
            contact_info.add_run(resume.phone)
            contact_info.add_run(' | ')
        if resume.location:
            contact_info.add_run(resume.location)

        # Summary
        if resume.summary:
            document.add_heading('Summary', level=1)
            document.add_paragraph(resume.summary)

        # Experience
        if resume.experiences.exists():
            document.add_heading('Experience', level=1)
            for exp in resume.experiences.all():
                p = document.add_paragraph()
                p.add_run(f"{exp.title} at {exp.company}").bold = True
                p.add_run(f"\n{exp.start_date.strftime('%b %Y')} - ")
                if exp.current:
                    p.add_run("Present")
                else:
                    p.add_run
                    p.add_run("Present")
            else:
                p.add_run(f"{exp.end_date.strftime('%b %Y')}")

        if exp.location:
            p.add_run(f"\n{exp.location}")

        if exp.description:
            document.add_paragraph(exp.description)

    # Education
    if resume.education.exists():
        document.add_heading('Education', level=1)
        for edu in resume.education.all():
            p = document.add_paragraph()
            p.add_run(f"{edu.degree} in {edu.field_of_study}").bold = True
            p.add_run(f"\n{edu.institution}")
            p.add_run(f"\n{edu.start_date.strftime('%b %Y')} - ")
            if edu.current:
                p.add_run("Present")
            else:
                p.add_run(f"{edu.end_date.strftime('%b %Y')}")

            if edu.description:
                document.add_paragraph(edu.description)

    # Skills
    if resume.skills.exists():
        document.add_heading('Skills', level=1)
        skills_para = document.add_paragraph()
        skills_list = [skill.name for skill in resume.skills.all()]
        skills_para.add_run(', '.join(skills_list))

        # Add other sections as needed

        # Save to a BytesIO object
        from io import BytesIO
        docx_file = BytesIO()
        document.save(docx_file)
        docx_file.seek(0)

        # Create a response with the DOCX
        response = HttpResponse(docx_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{resume.slug}.docx"'

        # Save export record
        ResumeExport.objects.create(
            resume=resume,
            user=request.user,
            format='docx',
        )

        return response

    else:
        messages.error(request, f'Unsupported export format: {format}')
    return redirect('resume:detail', slug=resume.slug)


@login_required
def share_resume(request, slug):
    """Share a resume via a public link."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)

    if request.method == 'POST':
        # Toggle public status
        resume.is_public = not resume.is_public

        # Generate or clear public URL
        if resume.is_public and not resume.public_url:
            resume.public_url = uuid.uuid4().hex[:10]
        elif not resume.is_public:
            resume.public_url = ''

        resume.save()

        if resume.is_public:
            messages.success(request, 'Your resume is now public and can be shared!')
        else:
            messages.success(request, 'Your resume is now private.')

        return redirect('resume:detail', slug=resume.slug)

    context = {
        'resume': resume,
    }
    return render(request, 'resume/share_resume.html', context)


def public_resume(request, public_url):
    """View a publicly shared resume."""
    resume = get_object_or_404(Resume, public_url=public_url, is_public=True)
    resume.increment_view_count()

    context = {
        'resume': resume,
        'is_public_view': True,
    }
    return render(request, 'resume/public_resume.html', context)


# AJAX views for resume sections

@login_required
@require_POST
def add_education(request, slug):
    """Add education to a resume."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)
    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save(commit=False)
        education.resume = resume
        education.order = resume.education.count()
        education.save()

        return JsonResponse({
            'success': True,
            'id': education.id,
            'html': render_to_string('resume/partials/education_item.html', {'education': education})
        })

    return JsonResponse({'success': False, 'errors': form.errors})


@login_required
@require_POST
def update_education(request, id):
    """Update an education entry."""
    education = get_object_or_404(Education, id=id, resume__user=request.user)
    form = EducationForm(request.POST, instance=education)

    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'html': render_to_string('resume/partials/education_item.html', {'education': education})
        })

    return JsonResponse({'success': False, 'errors': form.errors})


@login_required
@require_POST
def delete_education(request, id):
    """Delete an education entry."""
    education = get_object_or_404(Education, id=id, resume__user=request.user)
    education.delete()
    return JsonResponse({'success': True})


# Similar AJAX views for other resume sections (Experience, Skills, etc.)
# These would follow the same pattern as the education views above

@login_required
@require_POST
def reorder_sections(request, slug):
    """Reorder resume sections."""
    resume = get_object_or_404(Resume, slug=slug, user=request.user)

    try:
        data = json.loads(request.body)
        section_type = data.get('section_type')
        ordered_ids = data.get('ordered_ids', [])

        if section_type == 'education':
            for i, id in enumerate(ordered_ids):
                Education.objects.filter(id=id, resume=resume).update(order=i)
        elif section_type == 'experience':
            for i, id in enumerate(ordered_ids):
                Experience.objects.filter(id=id, resume=resume).update(order=i)
        elif section_type == 'skill':
            for i, id in enumerate(ordered_ids):
                Skill.objects.filter(id=id, resume=resume).update(order=i)
        # Add similar blocks for other section types

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def search_resumes(request):
    """Search user's resumes."""
    query = request.GET.get('q', '')

    if query:
        resumes = Resume.objects.filter(
            user=request.user
        ).filter(
            Q(title__icontains=query) |
            Q(full_name__icontains=query) |
            Q(headline__icontains=query) |
            Q(summary__icontains=query)
        )
    else:
        resumes = Resume.objects.filter(user=request.user)

    context = {
        'resumes': resumes,
        'query': query,
    }
    return render(request, 'resume/resume_search.html', context)


@login_required
def upload_resume(request):
    """Upload an existing resume."""
    if request.method == 'POST':
        # Handle file upload
        if 'resume_file' in request.FILES:
            # Process the uploaded file
            messages.success(request, 'Resume uploaded successfully!')
            return redirect('resume:my_resumes')

    return render(request, 'resume/upload.html')


@login_required
def my_resumes(request):
    """View all user resumes."""
    # Get user's resumes
    resumes = []  # This would typically come from the database

    context = {
        'resumes': resumes,
    }
    return render(request, 'resume/my_resumes.html', context)


class ResumeTemplateListView(ListView):
    """View for browsing resume templates"""
    model = ResumeTemplate
    template_name = 'dashboard/resume_templates.html'
    context_object_name = 'templates'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(ResumeTemplate.CATEGORY_CHOICES)
        context['selected_category'] = self.request.GET.get('category', '')
        return context


@login_required
def resume_edit(request, uuid):
    """Edit a resume"""
    resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
    sections = resume.sections.all().order_by('order')

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated successfully!")
            return redirect('dashboard:resume_edit', uuid=resume.uuid)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'dashboard/resume_edit.html', {
        'resume': resume,
        'sections': sections,
        'form': form,
    })


@login_required
def resume_preview(request, uuid):
    """Preview a resume"""
    resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
    sections = resume.sections.all().order_by('order')

    return render(request, 'dashboard/resume_preview.html', {
        'resume': resume,
        'sections': sections,
    })


@login_required
def upload_resume(request):
    """Upload an existing resume for parsing"""
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Here you would implement resume parsing logic
            # For now, we'll just create a blank resume
            template = ResumeTemplate.objects.filter(category='simple').first()

            resume = Resume.objects.create(
                user=request.user,
                template=template,
                title="Uploaded Resume",
                content={"personal_info": {"email": request.user.email}}
            )

            # Create default sections
            default_sections = [
                {"type": "summary", "title": "Professional Summary", "order": 1},
                {"type": "experience", "title": "Work Experience", "order": 2},
                {"type": "education", "title": "Education", "order": 3},
                {"type": "skills", "title": "Skills", "order": 4},
            ]

            for section in default_sections:
                ResumeSection.objects.create(
                    resume=resume,
                    section_type=section["type"],
                    title=section["title"],
                    order=section["order"],
                    content={}
                )

            messages.success(request, "Resume uploaded successfully! Please review and edit the extracted information.")
            return redirect('dashboard:resume_edit', uuid=resume.uuid)
    else:
        form = ResumeUploadForm()

    return render(request, 'dashboard/resume_upload.html', {'form': form})


@login_required
def add_section(request, resume_uuid):
    """AJAX endpoint to add a new section to a resume"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resume = get_object_or_404(Resume, uuid=resume_uuid, user=request.user)

            # Get the highest order value and add 1
            highest_order = ResumeSection.objects.filter(resume=resume).order_by('-order').first()
            new_order = 1 if not highest_order else highest_order.order + 1

            section = ResumeSection.objects.create(
                resume=resume,
                section_type=data.get('section_type', 'custom'),
                title=data.get('title', 'New Section'),
                order=new_order,
                content={}
            )

            return JsonResponse({
                'success': True,
                'section_id': section.id,
                'section_type': section.section_type,
                'title': section.title
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def save_resume(request, uuid):
    """AJAX endpoint to save resume data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

            # Update personal info
            if 'personal_info' in data:
                resume.content['personal_info'] = data['personal_info']

            # Update sections
            if 'sections' in data:
                for section_data in data['sections']:
                    section_id = section_data.get('id')
                    section = get_object_or_404(ResumeSection, id=section_id, resume=resume)

                    # Update section content
                    section.content = section_data.get('content', {})
                    section.save()

            resume.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def delete_resume(request, resume_id):
    """Delete a resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        resume_title = resume.title
        resume.delete()
        messages.success(request, f"Resume '{resume_title}' has been deleted.")
        return redirect('dashboard:my_resumes')

    return redirect('dashboard:my_resumes')


@login_required
def download_resume(request, uuid, format):
    """Download resume in various formats"""
    resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
    sections = resume.sections.all().order_by('order')

    if format == 'pdf':
        # For PDF generation, you would typically use a library like WeasyPrint or xhtml2pdf
        # This is a simplified example
        from django.template.loader import render_to_string
        from django.http import HttpResponse
        from weasyprint import HTML, CSS
        from django.conf import settings
        import tempfile

        # Render the resume to HTML
        html_string = render_to_string('dashboard/resume_pdf.html', {
            'resume': resume,
            'sections': sections,
            'base_url': request.build_absolute_uri('/'),
        })

        # Create HTTP response with PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'

        # Generate PDF from HTML
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(
            response,
            stylesheets=[CSS(string=resume.template.css_styles)]
        )

        return response

    elif format == 'docx':
        # For DOCX generation, you would typically use a library like python-docx
        # This is a simplified example
        from django.http import HttpResponse
        import docx
        from docx.shared import Pt

        # Create a new document
        doc = docx.Document()

        # Add title
        doc.add_heading(
            f"{resume.content.get('personal_info', {}).get('first_name', '')} {resume.content.get('personal_info', {}).get('last_name', '')}",
            0)

        # Add contact info
        contact_info = resume.content.get('personal_info', {})
        p = doc.add_paragraph()
        p.add_run(f"Email: {contact_info.get('email', '')}\n")
        p.add_run(f"Phone: {contact_info.get('phone', '')}\n")
        p.add_run(
            f"Address: {contact_info.get('address', '')}, {contact_info.get('city', '')}, {contact_info.get('state', '')} {contact_info.get('zip_code', '')}")

        # Add sections
        for section in sections:
            doc.add_heading(section.title, 1)

            if section.section_type == 'summary':
                doc.add_paragraph(section.content.get('summary', ''))

            elif section.section_type == 'experience':
                for item in section.content.get('items', []):
                    p = doc.add_paragraph()
                    p.add_run(f"{item.get('job_title', '')} at {item.get('employer', '')}").bold = True
                    p.add_run(
                        f"\n{item.get('start_date', '')} - {item.get('end_date', 'Present') if not item.get('current_job', False) else 'Present'}")
                    doc.add_paragraph(item.get('description', ''))

            elif section.section_type == 'education':
                for item in section.content.get('items', []):
                    p = doc.add_paragraph()
                    p.add_run(f"{item.get('degree', '')} - {item.get('institution', '')}").bold = True
                    p.add_run(
                        f"\n{item.get('start_date', '')} - {item.get('end_date', 'Present') if not item.get('current_education', False) else 'Present'}")
                    doc.add_paragraph(item.get('description', ''))

            elif section.section_type == 'skills':
                skills = section.content.get('skills', [])
                if skills:
                    p = doc.add_paragraph(style='List Bullet')
                    p.add_run(', '.join(skills))

            else:
                doc.add_paragraph(section.content.get('text', ''))

        # Create response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.docx"'

        # Save document to response
        doc.save(response)

        return response

    elif format == 'txt':
        # For TXT generation
        from django.http import HttpResponse

        # Create response
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.txt"'

        # Write personal info
        personal_info = resume.content.get('personal_info', {})
        response.write(f"{personal_info.get('first_name', '')} {personal_info.get('last_name', '')}\n")
        response.write(f"Email: {personal_info.get('email', '')}\n")
        response.write(f"Phone: {personal_info.get('phone', '')}\n")
        response.write(
            f"Address: {personal_info.get('address', '')}, {personal_info.get('city', '')}, {personal_info.get('state', '')} {personal_info.get('zip_code', '')}\n\n")

        # Write sections
        for section in sections:
            response.write(f"{section.title.upper()}\n")
            response.write("=" * len(section.title) + "\n\n")

            if section.section_type == 'summary':
                response.write(f"{section.content.get('summary', '')}\n\n")

            elif section.section_type == 'experience':
                for item in section.content.get('items', []):
                    response.write(f"{item.get('job_title', '')} at {item.get('employer', '')}\n")
                    response.write(
                        f"{item.get('start_date', '')} - {item.get('end_date', 'Present') if not item.get('current_job', False) else 'Present'}\n")
                    response.write(f"{item.get('description', '')}\n\n")

            elif section.section_type == 'education':
                for item in section.content.get('items', []):
                    response.write(f"{item.get('degree', '')} - {item.get('institution', '')}\n")
                    response.write(
                        f"{item.get('start_date', '')} - {item.get('end_date', 'Present') if not item.get('current_education', False) else 'Present'}\n")
                    response.write(f"{item.get('description', '')}\n\n")

            elif section.section_type == 'skills':
                skills = section.content.get('skills', [])
                if skills:
                    response.write(', '.join(skills) + "\n\n")

            else:
                response.write(f"{section.content.get('text', '')}\n\n")

        return response

    else:
        # Invalid format
        messages.error(request, f"Invalid download format: {format}")
        return redirect('dashboard:resume_preview', uuid=uuid)