from .models import Industry, JobTitle

def navbar_context(request):
    """Context processor to add industries and job titles to all templates"""
    return {
        'industries': Industry.objects.filter(featured=True)[:5],
        'popular_job_titles': JobTitle.objects.filter(featured=True)[:5],
    }

