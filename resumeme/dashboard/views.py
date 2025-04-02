from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserDashboardSettings, JobApplication
from .forms import UserSettingsForm, JobApplicationForm, ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .models import ResumeTemplate
from home.models import Resume
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .models import ResumeTemplate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create_resume(request):
    """Create a new resume."""
    # This would typically redirect to the resume editor with a new resume
    return render(request, 'resume/editor.html')


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


@login_required
def dashboard_index(request):
    """Dashboard home page."""
    return render(request, 'dashboard/index.html')


@login_required
def template_gallery(request):
    """Display all available resume templates."""
    templates = ResumeTemplate.objects.filter(is_active=True)

    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        templates = templates.filter(category=category)

    context = {
        'templates': templates,
        'categories': dict(ResumeTemplate.CATEGORY_CHOICES),
        'selected_category': category,
    }
    return render(request, 'dashboard/template_gallery.html', context)


@login_required
def template_preview(request, template_slug):
    """Preview a specific template with user's data."""
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Check if this is a premium template and user has access
    if template.is_premium and not hasattr(request.user, 'profile') or not request.user.profile.has_premium_access:
        messages.warning(request, "This is a premium template. Upgrade to access it.")

    context = {
        'template': template,
    }
    return render(request, 'dashboard/template_preview.html', context)


@login_required
def select_template(request, template_slug):
    """Select a template for the user's resume."""
    if request.method != 'POST':
        return redirect('dashboard:template_gallery')

    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Check if this is a premium template and user has access
    if template.is_premium and not hasattr(request.user, 'profile') or not request.user.profile.has_premium_access:
        messages.error(request, "You need to upgrade to use premium templates.")
        return redirect('dashboard:template_gallery')

    # Save user's template selection
    selection, created = UserTemplateSelection.objects.update_or_create(
        user=request.user,
        template=template,
        defaults={
            'primary_color': request.POST.get('primary_color', template.primary_color),
            'secondary_color': request.POST.get('secondary_color', template.secondary_color),
            'text_color': request.POST.get('text_color', template.text_color),
            'font_family': request.POST.get('font_family'),
        }
    )

    # Update template usage count
    if created:
        template.usage_count += 1
        template.save()

    messages.success(request, f"Template '{template.name}' has been selected for your resume.")
    return redirect('resume:create')


@login_required
def customize_template(request, template_slug):
    """Customize a template's colors and fonts."""
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Get user's current selection if it exists
    selection = UserTemplateSelection.objects.filter(
        user=request.user,
        template=template
    ).first()

    context = {
        'template': template,
        'selection': selection,
    }
    return render(request, 'dashboard/customize_template.html', context)


@login_required
def render_resume_preview(request):
    """AJAX endpoint to render resume preview with selected template."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    template_slug = request.POST.get('template_slug')
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Get customization options
    primary_color = request.POST.get('primary_color', template.primary_color)
    secondary_color = request.POST.get('secondary_color', template.secondary_color)
    text_color = request.POST.get('text_color', template.text_color)
    font_family = request.POST.get('font_family', 'Arial, sans-serif')

    # Render the preview
    html = render_to_string('dashboard/partials/resume_preview.html', {
        'template': template,
        'primary_color': primary_color,
        'secondary_color': secondary_color,
        'text_color': text_color,
        'font_family': font_family,
    })

    return JsonResponse({'html': html})


@login_required
def template_gallery(request):
    """Display all available resume templates."""
    templates = ResumeTemplate.objects.filter(is_active=True)

    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        templates = templates.filter(category=category)

    # Get user's resume data for preview
    user_resume = Resume.objects.filter(user=request.user).first()

    context = {
        'templates': templates,
        'categories': dict(ResumeTemplate.CATEGORY_CHOICES),
        'selected_category': category,
        'user_resume': user_resume,
    }
    return render(request, 'dashboard/template_gallery.html', context)


@login_required
def template_preview(request, template_slug):
    """Preview a specific template with user's data."""
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Get user's resume data
    user_resume = Resume.objects.filter(user=request.user).first()

    # Check if this is a premium template and user has access
    if template.is_premium and not request.user.profile.has_premium_access:
        messages.warning(request, "This is a premium template. Upgrade to access it.")

    context = {
        'template': template,
        'user_resume': user_resume,
    }
    return render(request, 'dashboard/template_preview.html', context)


@login_required
def select_template(request, template_slug):
    """Select a template for the user's resume."""
    if request.method != 'POST':
        return redirect('dashboard:template_gallery')

    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Check if this is a premium template and user has access
    if template.is_premium and not request.user.profile.has_premium_access:
        messages.error(request, "You need to upgrade to use premium templates.")
        return redirect('dashboard:template_gallery')

    # Save user's template selection
    selection, created = UserTemplateSelection.objects.update_or_create(
        user=request.user,
        template=template,
        defaults={
            'primary_color': request.POST.get('primary_color', template.primary_color),
            'secondary_color': request.POST.get('secondary_color', template.secondary_color),
            'text_color': request.POST.get('text_color', template.text_color),
            'font_family': request.POST.get('font_family'),
        }
    )

    # Update template usage count
    if created:
        template.usage_count += 1
        template.save()

    messages.success(request, f"Template '{template.name}' has been selected for your resume.")
    return redirect('home:resume_editor')


@login_required
def customize_template(request, template_slug):
    """Customize a template's colors and fonts."""
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Get user's current selection if it exists
    selection = UserTemplateSelection.objects.filter(
        user=request.user,
        template=template
    ).first()

    context = {
        'template': template,
        'selection': selection,
    }
    return render(request, 'dashboard/customize_template.html', context)


@login_required
def render_resume_preview(request):
    """AJAX endpoint to render resume preview with selected template."""
    if request.method != 'POST' or not request.is_ajax():
        return JsonResponse({'error': 'Invalid request'}, status=400)

    template_slug = request.POST.get('template_slug')
    template = get_object_or_404(ResumeTemplate, slug=template_slug, is_active=True)

    # Get user's resume data
    user_resume = Resume.objects.filter(user=request.user).first()

    # Get customization options
    primary_color = request.POST.get('primary_color', template.primary_color)
    secondary_color = request.POST.get('secondary_color', template.secondary_color)
    text_color = request.POST.get('text_color', template.text_color)
    font_family = request.POST.get('font_family', 'Arial, sans-serif')

    # Render the preview
    html = render_to_string('dashboard/partials/resume_preview.html', {
        'template': template,
        'user_resume': user_resume,
        'primary_color': primary_color,
        'secondary_color': secondary_color,
        'text_color': text_color,
        'font_family': font_family,
    })

    return JsonResponse({'html': html})


@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')

# Resume Management Views
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard/resumes/list.html', {'resumes': resumes})

@login_required
def create_resume(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'dashboard/resumes/create.html')

@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'dashboard/resumes/edit.html', {'resume': resume})

@login_required
def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully')
        return redirect('resume_list')
    return render(request, 'dashboard/resumes/delete_confirm.html', {'resume': resume})

@login_required
def duplicate_resume(request, id):
    original_resume = get_object_or_404(Resume, id=id, user=request.user)
    # Logic to duplicate resume
    return redirect('resume_list')

@login_required
def download_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    # Logic to generate and download resume
    return HttpResponse('Resume file content', content_type='application/pdf')

# Profile Management Views
@login_required
def profile_settings(request):
    if request.method == 'POST':
        # Handle profile update
        pass
    return render(request, 'dashboard/profile/settings.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        # Handle password change
        pass
    return render(request, 'dashboard/profile/change_password.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        # Handle email change
        pass
    return render(request, 'dashboard/profile/change_email.html')

# Subscription Management Views
@login_required
def subscription_details(request):
    return render(request, 'dashboard/subscription/details.html')

@login_required
def upgrade_subscription(request):
    if request.method == 'POST':
        # Handle subscription upgrade
        pass
    return render(request, 'dashboard/subscription/upgrade.html')

@login_required
def cancel_subscription(request):
    if request.method == 'POST':
        # Handle subscription cancellation
        pass
    return render(request, 'dashboard/subscription/cancel.html')

@login_required
def billing_history(request):
    # Get billing history
    return render(request, 'dashboard/subscription/billing_history.html')

# Job Applications Views
@login_required
def job_applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    return render(request, 'dashboard/applications/list.html', {'applications': applications})

@login_required
def add_application(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'dashboard/applications/add.html')

@login_required
def edit_application(request, id):
    application = get_object_or_404(JobApplication, id=id, user=request.user)
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'dashboard/applications/edit.html', {'application': application})

# Analytics & Reports Views
@login_required
def resume_analytics(request):
    # Get analytics data
    return render(request, 'dashboard/analytics/resume_analytics.html')

@login_required
def generate_reports(request):
    # Generate reports
    return render(request, 'dashboard/analytics/reports.html')

# Settings Views
@login_required
def account_settings(request):
    if request.method == 'POST':
        # Handle settings update
        pass
    return render(request, 'dashboard/settings/account.html')

@login_required
def notification_settings(request):
    if request.method == 'POST':
        # Handle notification settings update
        pass
    return render(request, 'dashboard/settings/notifications.html')

@login_required
def privacy_settings(request):
    if request.method == 'POST':
        # Handle privacy settings update
        pass
    return render(request, 'dashboard/settings/privacy.html')

# Help & Support Views
@login_required
def help_center(request):
    return render(request, 'dashboard/help/center.html')

@login_required
def support_ticket(request):
    if request.method == 'POST':
        # Handle ticket submission
        pass
    return render(request, 'dashboard/help/support_ticket.html')

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        # Handle feedback submission
        pass
    return render(request, 'dashboard/help/feedback.html')

# API Access Views
@login_required
def api_keys(request):
    # Get user's API keys
    return render(request, 'dashboard/api/keys.html')

@login_required
def api_documentation(request):
    return render(request, 'dashboard/api/documentation.html')


@login_required
def job_applications(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Job application added successfully!')
            return redirect('dashboard:job_applications')
    else:
        form = JobApplicationForm()

    applications = JobApplication.objects.filter(user=request.user).order_by('-applied_date')
    return render(request, 'dashboard/job_applications.html', {
        'form': form,
        'applications': applications
    })


@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard:profile_settings')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'dashboard/profile_settings.html', {'form': form})