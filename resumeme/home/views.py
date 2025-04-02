from .models import *
from django.views.generic import TemplateView, FormView
from .models import Pricing, Feature, FAQ, Testimonial
from .forms import ContactForm
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from dashboard.forms import ResumeForm
from .utils import WordExporter, PDFExporter, AIHelper
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, FileResponse
from .utils import PDFExporter
import os
import textwrap
from .models import BlogPost, ResumeExample, CareerAdvice
from .models import CVTemplate, Resume
from .forms import CVTemplateSelectForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CoverLetter, CoverLetterTemplate
from .forms import CoverLetterForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import ResumeTemplate, Resume, ResumeSection
from .forms import ResumeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CareerArticle, CareerCategory, NewsletterSubscription
from .forms import NewsletterSubscriptionForm, CareerAdviceSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib import messages
import json
from .models import ResumeTemplate, Resume, ResumeSection
from .forms import ResumeForm


def home(request):
    """Landing page view"""
    # Count resumes created today
    from django.utils import timezone
    from django.db.models import Count
    import random

    today = timezone.now().date()
    # For demo purposes, generate a random number or use actual count
    resumes_today = Resume.objects.filter(created_at__date=today).count()
    if resumes_today < 100:  # If it's a new site or few users
        resumes_today = random.randint(1000, 50000)  # Show an impressive number

    featured_templates = ResumeTemplate.objects.filter(is_featured=True)[:3]

    return render(request, 'home/index.html', {
        'resumes_today': resumes_today,
        'featured_templates': featured_templates,
    })


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
            return redirect('resume_edit', uuid=resume.uuid)
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
            return redirect('resume_edit', uuid=resume.uuid)
    else:
        form = ResumeUploadForm()

    return render(request, 'dashboard/resume_upload.html', {'form': form})


def landing_page(request):
    """Render the landing page."""
    # Get featured templates
    featured_templates = ResumeTemplate.objects.filter(
        is_premium=True
    ).order_by('-created_at')[:6]

    # Get resume count (this would typically come from a cache or database counter)
    resume_count = 43711  # Placeholder value

    context = {
        'featured_templates': featured_templates,
        'resume_count': resume_count,
    }
    return render(request, 'home/landing_page.html', context)


def choose_template(request):
    """
    View to display available resume templates for users to choose from.
    """
    # Define available templates
    templates = [
        {'id': 1, 'name': 'Classic', 'image': 'images/classic.png'},
        {'id': 2, 'name': 'Modern', 'image': 'images/modern.png'},
        {'id': 3, 'name': 'Creative', 'image': 'images/creative.png'},
        # Add more templates as needed
    ]

    # Context to pass to the template
    context = {'templates': templates}

    return render(request, 'resume_builder/choose_template.html', context)


def career_development(request):
    """
    Comprehensive guide on career development strategies, including goal setting,
    skill enhancement, networking, and advancement opportunities.
    """
    # Career development categories
    categories = [
        {
            'id': 'goal_setting',
            'name': 'Goal Setting',
            'icon': 'target',
            'description': 'Define and track your career objectives'
        },
        {
            'id': 'skill_enhancement',
            'name': 'Skill Enhancement',
            'icon': 'school',
            'description': 'Identify and develop key skills for career growth'
        },
        {
            'id': 'networking',
            'name': 'Networking',
            'icon': 'people',
            'description': 'Build and leverage professional relationships'
        },
        {
            'id': 'advancement',
            'name': 'Advancement',
            'icon': 'trending_up',
            'description': 'Strategies for moving forward in your career'
        }
    ]

    # Goal setting strategies
    goal_strategies = [
        {
            'title': 'SMART Goals',
            'description': 'Set Specific, Measurable, Achievable, Relevant, and Time-bound goals to ensure clarity and trackability.',
            'example': 'Instead of "Improve my skills," set a SMART goal like "Complete an online course in data analysis by the end of Q2 to enhance my analytical skills."'
        },
        {
            'title': 'Vision Board',
            'description': 'Create a visual representation of your career aspirations to keep you motivated and focused.',
            'example': 'Include images and words that represent your career goals, such as a picture of a company you aspire to work for or a word that embodies your desired role.'
        },
        {
            'title': 'Regular Check-ins',
            'description': 'Schedule regular reviews of your goals to assess progress and make necessary adjustments.',
            'example': 'Set a monthly reminder to review your goals, celebrate achievements, and adjust timelines or strategies as needed.'
        }
    ]

    # Skill enhancement resources
    skill_resources = [
        {
            'name': 'Online Courses',
            'description': 'Platforms offering courses in various fields to enhance your skills.',
            'examples': [
                {'name': 'Coursera', 'url': 'https://www.coursera.org'},
                {'name': 'Udemy', 'url': 'https://www.udemy.com'},
                {'name': 'edX', 'url': 'https://www.edx.org'},
                {'name': 'LinkedIn Learning', 'url': 'https://www.linkedin.com/learning/'}
            ]
        },
        {
            'name': 'Workshops & Seminars',
            'description': 'Attend industry-specific workshops and seminars to gain practical knowledge and network with peers.',
            'examples': [
                {'name': 'Industry Conferences', 'url': '#'},
                {'name': 'Local Meetups', 'url': '#'},
                {'name': 'Webinars', 'url': '#'}
            ]
        },
        {
            'name': 'Mentorship Programs',
            'description': 'Connect with experienced professionals for guidance and advice.',
            'examples': [
                {'name': 'MentorMatch', 'url': '#'},
                {'name': 'Professional Associations', 'url': '#'},
                {'name': 'Company Mentorship Programs', 'url': '#'}
            ]
        }
    ]

    # Networking tips
    networking_tips = [
        {
            'title': 'Leverage LinkedIn',
            'description': 'Use LinkedIn to connect with industry professionals, join groups, and share your expertise.',
            'tips': [
                'Optimize your profile with a professional photo and detailed work history.',
                'Engage with content by liking, commenting, and sharing posts.',
                'Join industry-specific groups to participate in discussions and expand your network.'
            ]
        },
        {
            'title': 'Attend Networking Events',
            'description': 'Participate in events to meet new contacts and strengthen existing relationships.',
            'tips': [
                'Prepare an elevator pitch to introduce yourself effectively.',
                'Follow up with new contacts after the event to maintain the connection.',
                'Volunteer at events to increase visibility and meet more people.'
            ]
        },
        {
            'title': 'Informational Interviews',
            'description': 'Conduct informational interviews to learn about different roles and industries.',
            'tips': [
                'Research the person and their company before the interview.',
                'Prepare thoughtful questions to gain insights into their career path.',
                'Express gratitude and ask for referrals to other professionals.'
            ]
        }
    ]

    # Advancement strategies
    advancement_strategies = [
        {
            'title': 'Seek Feedback',
            'description': 'Regularly seek feedback from peers and supervisors to identify areas for improvement.',
            'example': 'Schedule quarterly feedback sessions with your manager to discuss performance and career aspirations.'
        },
        {
            'title': 'Take on New Challenges',
            'description': 'Volunteer for projects outside your comfort zone to develop new skills and demonstrate initiative.',
            'example': 'Offer to lead a cross-departmental project to gain experience in project management and collaboration.'
        },
        {
            'title': 'Build a Personal Brand',
            'description': 'Establish a strong personal brand to differentiate yourself and attract opportunities.',
            'example': 'Create a professional blog or portfolio showcasing your expertise and achievements.'
        }
    ]

    context = {
        'categories': categories,
        'goal_strategies': goal_strategies,
        'skill_resources': skill_resources,
        'networking_tips': networking_tips,
        'advancement_strategies': advancement_strategies,
        'page_title': 'Career Development Guide',
        'page_description': 'Strategies and resources to help you advance your career'
    }

    return render(request, 'home/career_development.html', context)


def salary_negotiation(request):
    """
    Comprehensive guide on salary negotiation tactics, including research methods,
    negotiation scripts, and timing strategies for maximizing compensation.
    """
    # Negotiation phases
    phases = [
        {
            'id': 'research',
            'name': 'Research',
            'icon': 'search',
            'description': 'Gather data to determine your market value'
        },
        {
            'id': 'preparation',
            'name': 'Preparation',
            'icon': 'assignment',
            'description': 'Plan your negotiation strategy and talking points'
        },
        {
            'id': 'timing',
            'name': 'Timing',
            'icon': 'schedule',
            'description': 'Choose the optimal moment to discuss compensation'
        },
        {
            'id': 'conversation',
            'name': 'Conversation',
            'icon': 'forum',
            'description': 'Navigate the negotiation discussion effectively'
        },
        {
            'id': 'response',
            'name': 'Response',
            'icon': 'psychology',
            'description': 'Handle counteroffers and objections'
        },
        {
            'id': 'benefits',
            'name': 'Benefits',
            'icon': 'card_giftcard',
            'description': 'Negotiate the complete compensation package'
        }
    ]

    # Research resources
    research_resources = [
        {
            'name': 'Salary Comparison Tools',
            'description': 'Online resources that provide salary data based on role, experience, and location',
            'examples': [
                {'name': 'Glassdoor', 'url': 'https://www.glassdoor.com'},
                {'name': 'PayScale', 'url': 'https://www.payscale.com'},
                {'name': 'Salary.com', 'url': 'https://www.salary.com'},
                {'name': 'LinkedIn Salary', 'url': 'https://www.linkedin.com/salary/'}
            ]
        },
        {
            'name': 'Industry Reports',
            'description': 'Comprehensive reports on industry-specific compensation trends',
            'examples': [
                {'name': 'Robert Half Salary Guide', 'url': '#'},
                {'name': 'Dice Tech Salary Report', 'url': '#'},
                {'name': 'BLS Occupational Outlook Handbook', 'url': '#'}
            ]
        },
        {
            'name': 'Professional Networks',
            'description': 'Connect with professionals in your field to gather insights on compensation',
            'examples': [
                {'name': 'LinkedIn Groups', 'url': '#'},
                {'name': 'Professional Associations', 'url': '#'},
                {'name': 'Alumni Networks', 'url': '#'}
            ]
        }
    ]

    # Negotiation scripts
    negotiation_scripts = [
        {
            'scenario': 'Discussing salary requirements during an interview',
            'script': 'Based on my research of similar roles in this industry and location, and considering my experience and skills, Im looking for a salary in the range of $X to $Y.However, Im also considering the entire compensation package and am somewhat flexible for the right opportunity. May I ask what range you have budgeted for this position?', 'rationale': 'This response shows youve done your homework while maintaining flexibility.Asking about their budget turns the question back to them and helps ensure youre in the same ballpark.' }, { 'scenario': 'Responding to a job offer',
    'script': 'Thank you for the offer. Im excited about the opportunity to join your team.Based on my research and the value I can bring to this role with my[ specific skills / experience], I was expecting a salary closer to $X.Is there room to discuss this further?',
    'rationale': 'This response expresses gratitude and enthusiasm while clearly stating your expectation. Mentioning specific skills or experience justifies your request for a higher salary.'

    },
    {
    'scenario': 'Negotiating after receiving a lower-than-expected offer',
    'script': 'I appreciate the offer and am very interested in the position. However, given my [specific qualifications/achievements] and the market rate for professionals with my background, I was hoping for a salary closer to $X. Is there flexibility in the budget to reach this number?',
    'rationale': 'This approach is direct but polite, focusing on your qualifications and market data rather than personal needs.'
    },
    {
    'scenario': 'Handling a firm "no" on salary',
    'script': 'I understand there are budget constraints. In that case, could we discuss other aspects of the compensation package, such as additional PTO, flexible working arrangements, professional development opportunities, or a performance review in six months with the potential for a salary adjustment?',
    'rationale': 'If salary is fixed, this pivots to other valuable benefits that might have more flexibility and could improve your overall compensation package.'
    },
    {
    'scenario': 'Negotiating a raise with your current employer',
    'script': 'Over the past year, Ive taken on additional responsibilities including[specific examples] and have delivered measurable results such as [specific achievements with metrics].Based on these contributions and my research on market rates for my role, Id like to discuss adjusting my compensation to $X, which better reflects my current value to the team.', 'rationale': 'This focuses on your increased value to the company with specific examples and metrics, making a data-based case for higher compensation.' } ]

    # Common mistakes
    negotiation_mistakes = [
        {
    'mistake': 'Giving the first number too early',
    'consequence': 'You might undervalue yourself or anchor the negotiation too low',
    'solution': 'When asked about salary expectations early in the interview process, politely deflect with: "Id like to learn more about the role and responsibilities first so we can determine a fair compensation package."'
    },
    {
    'mistake': 'Basing your ask solely on your current or previous salary',
    'consequence': 'This can perpetuate salary inequities and undervaluation, especially if you were underpaid previously',
    'solution': 'Research market rates for the specific role, company size, industry, and location. Base your expectations on this data rather than your salary history.'
    },
    {
    'mistake': 'Focusing only on base salary',
    'consequence': 'You might miss valuable benefits and perks that contribute to total compensation',
    'solution': 'Consider the entire package: health benefits, retirement contributions, bonuses, equity, paid time off, professional development, flexible work arrangements, and other perks.'
    },
    {
    'mistake': 'Justifying your salary request with personal reasons',
    'consequence': 'Employers care about your value to them, not your personal financial needs',
    'solution': 'Frame your request in terms of your market value, skills, experience, and the specific value youll bring to the company. '
    },
    {
    'mistake': 'Accepting an offer too quickly',
    'consequence': 'You might leave money on the table or miss negotiation opportunities',
    'solution': 'Thank the employer for the offer, express enthusiasm, but ask for time to consider it. Use this time to evaluate the entire package and prepare your negotiation strategy.'
    },
    {
    'mistake': 'Using aggressive or confrontational tactics',
    'consequence': 'This can damage relationships and potentially lead to rescinded offers',
    'solution': 'Maintain a collaborative, problem-solving approach. Frame the negotiation as finding a mutually beneficial arrangement.'
    }
    ]

    # Benefits beyond salary
    beyond_salary = [
        {
    'category': 'Health & Wellness',
    'benefits': [
        'Premium health, dental, and vision insurance',
        'Health Savings Account (HSA) or Flexible Spending Account (FSA) contributions',
        'Mental health benefits and resources',
        'Gym memberships or wellness stipends',
        'Disability and life insurance'
    ]
    },
    {
    'category': 'Financial Benefits',
    'benefits': [
        'Retirement plan matching or contributions',
        'Performance bonuses',
        'Profit sharing',
        'Stock options or equity grants',
        'Student loan repayment assistance',
        'Relocation assistance'
    ]
    },
    {
    'category': 'Work-Life Balance',
    'benefits': [
        'Additional paid time off',
        'Flexible working hours',
        'Remote or hybrid work options',
        'Compressed workweek (e.g., four 10-hour days)',
        'Sabbaticals or extended leave options',
        'Parental leave beyond legal requirements'
    ]
    },
    {
    'category': 'Professional Growth',
    'benefits': [
        'Professional development budget',
        'Conference attendance',
        'Certification or education reimbursement',
        'Mentorship programs',
        'Career advancement opportunities',
        'Training and upskilling programs'
    ]
    },
    {
    'category': 'Workplace Perks',
    'benefits': [
        'Commuter benefits',
        'Meal stipends or free meals',
        'Technology allowances',
        'Home office stipend',
        'Child or elder care assistance',
        'Company events and retreats'
    ]
    }
    ]

    # Industry-specific negotiation tips
    industry_tips = [
        {
    'industry': 'Technology',
    'tips': [
        'Equity can be as important as salary, especially at startups',
        'Negotiate for specific technologies or projects youll work with',
        'Remote work flexibility is often highly negotiable',
    'Consider negotiating for conference attendance and training',
    'Ask about performance bonus structures and criteria'
    ]
    },
    {
    'industry': 'Finance',
    'tips': [
        'Bonus structures can significantly impact total compensation',
        'Title negotiation can affect future earning potential',
        'Advanced certifications often command salary premiums',
        'Work-life balance provisions may be more valuable than small salary increases',
        'Client portfolio assignments can impact career trajectory'
    ]
    },
    {
    'industry': 'Healthcare',
    'tips': [
        'Continuing education and licensing costs coverage can be valuable',
        'Schedule flexibility may be negotiable',
        'Malpractice insurance coverage and terms are important',
        'Consider negotiating for specific departments or specialties',
        'Relocation packages for high-demand locations'
    ]
    },
    {
    'industry': 'Creative Fields',
    'tips': [
        'Negotiate for creative control and project selection',
        'Copyright and intellectual property terms may be negotiable',
        'Portfolio usage rights for your work',
        'Flexible work arrangements to accommodate creative processes',
        'Budget for tools, software, and equipment'
    ]
    }
    ]

    # Salary calculators and tools
    salary_tools = [
        {
    'name': 'Compensation Calculator',
    'description': 'Calculate target salary based on role, location, experience, and skills',
    'link': '#compensation-calculator'
    },
    {
    'name': 'Offer Comparison Tool',
    'description': 'Compare multiple job offers considering all aspects of compensation',
    'link': '#offer-comparison'
    },
    {
    'name': 'Negotiation Script Builder',
    'description': 'Create customized negotiation scripts based on your situation',
    'link': '#script-builder'
    },
    {
    'name': 'Salary History Tracker',
    'description': 'Document your compensation growth over time',
    'link': '#salary-tracker'
    }
    ]

    context = {
        'phases': phases,
        'research_resources': research_resources,
        'negotiation_scripts': negotiation_scripts,
        'negotiation_mistakes': negotiation_mistakes,
        'beyond_salary': beyond_salary,
        'industry_tips': industry_tips,
        'salary_tools': salary_tools,
        'page_title': 'Salary Negotiation Guide',
        'page_description': 'Expert strategies to maximize your compensation package'
    }

    return render(request, 'home/salary_negotiation.html', context)


def interview_tips(request):
    """
    Comprehensive interview preparation tips and resources,
    including common questions, answer strategies, and mock interview tools.
    """
    # Interview tip categories
    categories = [
        {
            'id': 'preparation',
            'name': 'Interview Preparation',
            'icon': 'calendar',
            'description': 'Steps to take before your interview'
        },
        {
            'id': 'questions',
            'name': 'Common Questions',
            'icon': 'help',
            'description': 'Frequently asked interview questions and how to answer them'
        },
        {
            'id': 'behavioral',
            'name': 'Behavioral Questions',
            'icon': 'psychology',
            'description': 'Strategies for answering questions about past experiences'
        },
        {
            'id': 'technical',
            'name': 'Technical Interviews',
            'icon': 'code',
            'description': 'Tips for coding interviews and technical assessments'
        },
        {
            'id': 'remote',
            'name': 'Virtual Interviews',
            'icon': 'videocam',
            'description': 'Best practices for video and phone interviews'
        },
        {
            'id': 'followup',
            'name': 'Follow-Up Strategies',
            'icon': 'mail',
            'description': 'What to do after your interview'
        }
    ]

    # Common interview question categories
    question_categories = [
        {
            'id': 'general',
            'name': 'General Questions',
            'questions': [
                {
                    'question': 'Tell me about yourself.',
                    'tips': 'Focus on professional background and relevant experience. Keep it concise (60-90 seconds) and end with why youre interested in this role.',
                                               'example': 'Im amarketing professional with 5 years of experience in digital advertising.I started my career at XYZ Agency where I managed social media campaigns for retail clients, increasing their engagement by 45 %.For the past 3 years at ABC Company, Ive led a team of 4 marketing specialists, focusing on integrated campaigns across multiple channels. Im particularly proud of a recent product launch that generated $1.2M in revenue within the first quarter.Im excited about this Senior Marketing Manager role because it would allow me to combine my creative and analytical skills to develop strategies for an industry leader like your company.'
    },{'question': 'What is your greatest strength?','tips': 'Choose a strength thats relevant to the position and provide a specific example that demonstrates it',
    'example': 'My greatest strength is my ability to translate complex technical concepts into clear, accessible language for non-technical stakeholders. As a project manager at my current company, I regularly bridge communication between our development team and clients. For example, when implementing a new CRM system, I created visual documentation that helped our sales team understand the technical changes and how they would improve their workflow. This resulted in 95% adoption of the new system within two weeks of launch.'
    },
    {
        'question': 'What is your greatest weakness?',
        'tips': 'Be honest about a real weakness, but focus on steps youre taking to address it.Avoid clichéslike "Im a perfectionist" or weaknesses that are critical to the job.', 'example': 'Ive sometimes struggled with public speaking and presenting to large groups.To address this, I joined Toastmasters last year and have been volunteering to lead team presentations.Ive also taken an online course on presentation skills. While I still get nervous, Ive developed strategies to manage my anxiety, and feedback on my recent presentations has been quite positive.Im continuing to seek opportunities to improve in this area.'
    },
    {'question': 'Why do you want to work here?','tips': 'Show that youve researched the company and connect your goals to their mission and values.',
    'example': 'Im drawn to your company for several reasons.First, your commitment to sustainability aligns with my personal values—I was particularly impressed by your recent initiative to reduce packaging waste by 50 %.Second, the innovative work youre doing in the renewable energy sector presents exciting challenges that match my engineering background. Finally, after speaking with Jane Smith from your engineering team at a recent conference, I was impressed by the collaborative culture youve built.I believe my skills in energy systems design would allow me to contribute to your mission while growing professionally in an environment that values innovation and sustainability.' } ] }, { 'id': 'behavioral', 'name': 'Behavioral Questions', 'questions': [
            {
    'question': 'Tell me about a time when you faced a challenge at work and how you overcame it.',
    'tips': 'Use the STAR method (Situation, Task, Action, Result) to structure your answer. Choose a significant challenge that demonstrates important skills.',
    'example': 'Situation: At my previous company, we unexpectedly lost our largest client, which represented 30% of our annual revenue, due to a merger on their end.\n\nTask: As the account manager, I needed to both mitigate the immediate financial impact and develop a strategy to replace the lost revenue.\n\nAction: First, I negotiated a 3-month transition period rather than an immediate contract termination. Then, I analyzed our client portfolio and identified 5 existing clients with growth potential. I developed customized expansion proposals for each, highlighting additional services they werent utilizing.Simultaneously, I created a targeted outreach campaign to prospects in the same industry as our lost client, leveraging our relevant experience.\n\nResult: Within 6 months, we had recovered 85 % of the lost revenue through expanding 3 existing client relationships and signing 2 new clients.By the end of the year, we had actually grown our overall revenue by 10 % compared to before losing the large client, with a more diversified client base that reduced our risk exposure.'

    },
    {
    'question': 'Describe a situation where you had to work with a difficult colleague or team member.',
    'tips': 'Focus on how you handled the situation professionally rather than criticizing the other person. Highlight communication and conflict resolution skills.',
    'example': 'Situation: In my role as project manager, I was leading a cross-functional team that included a senior developer who was highly skilled but frequently missed deadlines and was dismissive during team meetings.\n\nTask: I needed to address this behavior without creating tension, as this developers technical expertise was crucial to the projects success.\n\nAction: Instead of confronting the developer in front of the team, I scheduled a private meeting. I began by acknowledging their technical contributions and then explained how missed deadlines were affecting other team members and project timelines. I asked about any challenges they were facing and discovered they were overwhelmed with responsibilities from multiple projects. Together, we worked out a more realistic timeline and agreed on clear communication protocols for status updates.\n\nResult: After our conversation, the developer became more engaged in team meetings and started meeting deadlines consistently. They appreciated being heard rather than criticized, and we eventually developed a strong working relationship. The project was completed successfully, and this experience taught me the importance of addressing issues privately and seeking to understand the root causes of behavior before making judgments.' } ] }, {
        'id': 'technical',
        'name': 'Technical Questions',
        'questions': [
            {
    'question': 'How do you approach troubleshooting a complex technical problem?',
    'tips': 'Outline your systematic approach to problem-solving. Mention specific tools or methodologies you use.',
    'example': 'When faced with a complex technical problem, I follow a systematic approach. First, I gather information to understand the full scope of the issue, including when it started and under what conditions it occurs. I then reproduce the problem if possible to observe it firsthand. Next, I break the problem down into smaller components to isolate potential causes, often using logging tools or debugging software to track system behavior.\n\nFor example, when our e-commerce platform was experiencing intermittent payment processing failures, I first analyzed error logs and identified patterns in the timing of failures. I created a test environment where I could safely reproduce the issue, then used monitoring tools to track network traffic, database queries, and API responses. This methodical approach revealed that the issue occurred when concurrent user sessions exceeded a certain threshold. I implemented a queuing system for payment processing requests, which resolved the issue while we worked on a more permanent scaling solution.\n\nThroughout my troubleshooting process, I document my findings and communicate with stakeholders to manage expectations and provide regular updates. This approach has consistently helped me resolve complex technical issues efficiently while minimizing disruption to users.'
    },
    {
    'question': 'Explain a complex technical concept to someone without technical background.','tips': 'Demonstrate your communication skills by using analogies, simple language, and visual explanations without being condescending.','example': 'Let me explain how cloud computing works. Imagine you used to store all your family photos on your home computer. This is like traditional computing—everything is stored and processed on your own physical device. If your computer breaks, you might lose those photos, and if you buy a new computer, you need to figure out how to transfer everything.\n\nCloud computing is like storing those photos in a digital safety deposit box that you can access from any device. Instead of keeping everything on your personal computer, your data is stored in large, specialized facilities run by companies like Amazon or Microsoft.\n\nThese facilities are like digital libraries with thousands of powerful computers that store and process data. When you need to access your information or run a program, your device sends a request to this digital library, which does the work and sends back the results. This means you can use less powerful devices—like smartphones or tablets—to do complex tasks because the heavy lifting happens in the cloud.\n\nThe benefits are similar to using a bank instead of storing money under your mattress: better security, access from anywhere, and you only pay for the space you use. Plus, if you suddenly need more storage or computing power, you can get it immediately without buying new hardware—like instantly expanding your safety deposit box during the holidays when you take more photos.'
    }
    ]
    }
    ]

    # Interview by industry tips
    industries = [
        {
            'id': 'tech',
            'name': 'Technology',
            'specific_tips': [
                'Be prepared for technical assessments and coding challenges',
                'Research the company\'s tech stack and products in detail',
                'Prepare examples of projects you\'ve worked on, with specific contributions and technologies used',
                'Be ready to discuss how you stay current with evolving technologies',
                'Practice system design questions for senior roles'
            ]
        },
        {
            'id': 'finance',
            'name': 'Finance & Banking',
            'specific_tips': [
                'Review financial concepts, regulations, and current market trends',
                'Be prepared for case studies and financial modeling exercises',
                'Demonstrate knowledge of relevant financial software and tools',
                'Research recent mergers, acquisitions, or major events in the industry',
                'Practice explaining complex financial concepts in simple terms'
            ]
        },
        {
            'id': 'healthcare',
            'name': 'Healthcare',
            'specific_tips': [
                'Review relevant healthcare regulations and standards (HIPAA, etc.)',
                'Prepare examples of how you\'ve handled patient care or sensitive situations',
                'Emphasize empathy and communication skills',
                'Research the organization\'s specific approach to healthcare delivery',
                'Be prepared to discuss teamwork in multidisciplinary environments'
            ]
        },
        {
            'id': 'creative',
            'name': 'Creative Fields',
            'specific_tips': [
                'Prepare a polished portfolio and be ready to discuss your creative process',
                'Practice explaining the reasoning behind your design choices',
                'Research current trends and innovations in your creative field',
                'Prepare examples of how you\'ve handled client feedback and revisions',
                'Demonstrate your ability to balance creativity with business objectives'
            ]
        }
    ]

    # Interview preparation checklist
    preparation_checklist = [
        {
            'category': 'Research',
            'items': [
                'Research the company\'s products, services, and recent news',
                'Review the company\'s mission, values, and culture',
                'Study the job description and identify key requirements',
                'Research your interviewers on LinkedIn if their names are provided',
                'Understand the industry trends and challenges'
            ]
        },
        {
            'category': 'Personal Preparation',
            'items': [
                'Prepare your "tell me about yourself" response',
                'Identify relevant accomplishments and prepare STAR examples',
                'Practice answers to common interview questions',
                'Prepare thoughtful questions to ask the interviewer',
                'Review your resume and be ready to discuss all aspects of it'
            ]
        },
        {
            'category': 'Logistics',
            'items': [
                'Confirm the interview time, location, or virtual meeting details',
                'Plan your route or test your video conferencing setup',
                'Prepare appropriate interview attire',
                'Bring copies of your resume, portfolio, and other relevant documents',
                'Get a good night\'s sleep before the interview'
            ]
        }
    ]

    # Virtual interview tips
    virtual_interview_tips = [
        {
            'title': 'Technical Setup',
            'tips': [
                'Test your camera, microphone, and internet connection beforehand',
                'Download any required software and test it a day before',
                'Position your camera at eye level and check your background',
                'Ensure your space is well-lit with light facing you, not behind you',
                'Close unnecessary applications to prevent notifications or slowdowns'
            ]
        },
        {
            'title': 'Environment',
            'tips': [
                'Find a quiet, private location without distractions',
                'Choose a clean, professional background or use a simple virtual background',
                'Inform household members about your interview to prevent interruptions',
                'Keep a glass of water nearby but out of camera view',
                'Have a notepad and pen ready for notes'
            ]
        },
        {
            'title': 'During the Interview',
            'tips': [
                'Look at the camera (not the screen) to make "eye contact"',
                'Speak clearly and slightly slower than in person',
                'Use professional body language and avoid excessive movement',
                'Pause briefly before answering to prevent talking over the interviewer',
                'If technical issues occur, stay calm and have a backup plan (phone number, etc.)'
            ]
        }
    ]

    # Mock interview resources
    mock_interview_resources = [
        {
            'name': 'Interview Simulator',
            'description': 'Practice with AI-powered interview simulations that provide instant feedback',
            'features': [
                'Industry-specific question banks',
                'Video recording for self-assessment',
                'Feedback on verbal and non-verbal communication',
                'Customizable interview scenarios'
            ],
            'link': '#interview-simulator'
        },
        {
            'name': 'Peer Interview Exchange',
            'description': 'Connect with other job seekers for mutual interview practice',
            'features': [
                'Match with peers in similar industries',
                'Structured feedback templates',
                'Schedule practice sessions on your calendar',
                'Access to interview question libraries'
            ],
            'link': '#peer-exchange'
        },
        {
            'name': 'Expert Coaching Sessions',
            'description': 'Book one-on-one sessions with professional interview coaches',
            'features': [
                'Personalized feedback from industry experts',
                'Role-specific interview preparation',
                'Guidance on addressing challenging questions',
                'Follow-up resources and action plans'
            ],
            'link': '#expert-coaching'
        }
    ]

    context = {
        'categories': categories,
        'question_categories': question_categories,
        'industries': industries,
        'preparation_checklist': preparation_checklist,
        'virtual_interview_tips': virtual_interview_tips,
        'mock_interview_resources': mock_interview_resources,
        'page_title': 'Interview Tips',
        'page_description': 'Comprehensive resources to help you prepare for and excel in job interviews'
    }
    return render(request, 'home/interview_tips.html', context)


def job_search(request):
    """
    Job search page allowing users to search and filter job listings from various sources.
    """
    # Get search and filter parameters
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    experience_level = request.GET.get('experience', '')
    salary_range = request.GET.get('salary', '')

    # Job types for filter dropdown
    job_types = [
        {'id': 'full_time', 'name': 'Full Time'},
        {'id': 'part_time', 'name': 'Part Time'},
        {'id': 'contract', 'name': 'Contract'},
        {'id': 'temporary', 'name': 'Temporary'},
        {'id': 'internship', 'name': 'Internship'},
        {'id': 'remote', 'name': 'Remote'}
    ]

    # Experience levels for filter dropdown
    experience_levels = [
        {'id': 'entry', 'name': 'Entry Level'},
        {'id': 'mid', 'name': 'Mid Level'},
        {'id': 'senior', 'name': 'Senior Level'},
        {'id': 'executive', 'name': 'Executive'}
    ]

    # Salary ranges for filter dropdown
    salary_ranges = [
        {'id': 'under_50k', 'name': 'Under $50K'},
        {'id': '50k_75k', 'name': '$50K - $75K'},
        {'id': '75k_100k', 'name': '$75K - $100K'},
        {'id': '100k_150k', 'name': '$100K - $150K'},
        {'id': 'over_150k', 'name': 'Over $150K'}
    ]

    # Popular job categories
    job_categories = [
        {'id': 'technology', 'name': 'Technology & IT', 'icon': 'computer', 'count': 1245},
        {'id': 'healthcare', 'name': 'Healthcare & Medical', 'icon': 'medical_services', 'count': 876},
        {'id': 'finance', 'name': 'Finance & Banking', 'icon': 'attach_money', 'count': 643},
        {'id': 'sales', 'name': 'Sales & Marketing', 'icon': 'trending_up', 'count': 589},
        {'id': 'engineering', 'name': 'Engineering', 'icon': 'build', 'count': 421},
        {'id': 'education', 'name': 'Education & Teaching', 'icon': 'school', 'count': 387}
    ]

    # Sample job listings (in a real app, these would be fetched from a database/API)
    job_listings = [
        {
            'id': 'job-1',
            'title': 'Senior Software Engineer',
            'company': 'Tech Innovations Inc.',
            'company_logo': 'images/companies/tech-innovations.png',
            'location': 'San Francisco, CA',
            'remote': True,
            'job_type': 'full_time',
            'experience': 'senior',
            'salary_range': '100k_150k',
            'salary': '$120,000 - $150,000',
            'description': 'We are seeking an experienced software engineer to join our team and lead development of our flagship product.',
            'requirements': [
                'Bachelor\'s degree in Computer Science or related field',
                '5+ years of experience in software development',
                'Proficiency in Python, JavaScript, and React',
                'Experience with cloud services (AWS, Azure, or GCP)',
                'Strong problem-solving skills and ability to mentor junior developers'
            ],
            'posted_date': '2023-05-12',
            'days_ago': 3,
            'category': 'technology'
        },
        {
            'id': 'job-2',
            'title': 'Financial Analyst',
            'company': 'Global Finance Group',
            'company_logo': 'images/companies/global-finance.png',
            'location': 'New York, NY',
            'remote': False,
            'job_type': 'full_time',
            'experience': 'mid',
            'salary_range': '75k_100k',
            'salary': '$85,000 - $95,000',
            'description': 'Join our financial planning team to analyze market trends and provide strategic recommendations to clients.',
            'requirements': [
                'Bachelor\'s degree in Finance, Economics, or related field',
                '3+ years of experience in financial analysis',
                'Proficiency in Excel and financial modeling',
                'Series 7 and 63 licenses preferred',
                'Strong analytical and communication skills'
            ],
            'posted_date': '2023-05-10',
            'days_ago': 5,
            'category': 'finance'
        },
        {
            'id': 'job-3',
            'title': 'Marketing Coordinator',
            'company': 'Brand Builders Co.',
            'company_logo': 'images/companies/brand-builders.png',
            'location': 'Chicago, IL',
            'remote': True,
            'job_type': 'full_time',
            'experience': 'entry',
            'salary_range': '50k_75k',
            'salary': '$55,000 - $65,000',
            'description': 'Help coordinate marketing campaigns across digital platforms and assist with content creation and analytics.',
            'requirements': [
                'Bachelor\'s degree in Marketing, Communications, or related field',
                '1-2 years of experience in marketing',
                'Experience with social media management and analytics tools',
                'Excellent writing and communication skills',
                'Basic design skills (Canva, Photoshop)'
            ],
            'posted_date': '2023-05-14',
            'days_ago': 1,
            'category': 'sales'
        },
        {
            'id': 'job-4',
            'title': 'Registered Nurse - ICU',
            'company': 'City General Hospital',
            'company_logo': 'images/companies/city-general.png',
            'location': 'Boston, MA',
            'remote': False,
            'job_type': 'full_time',
            'experience': 'mid',
            'salary_range': '75k_100k',
            'salary': '$80,000 - $95,000',
            'description': 'Seeking experienced ICU nurses to provide direct patient care in our state-of-the-art intensive care unit.',
            'requirements': [
                'BSN and active RN license',
                '3+ years of ICU experience',
                'BLS and ACLS certifications (PALS preferred)',
                'Strong clinical assessment and critical thinking skills',
                'Excellent communication and teamwork abilities'
            ],
            'posted_date': '2023-05-09',
            'days_ago': 6,
            'category': 'healthcare'
        },
        {
            'id': 'job-5',
            'title': 'Data Scientist',
            'company': 'Data Insights Partners',
            'company_logo': 'images/companies/data-insights.png',
            'location': 'Austin, TX',
            'remote': True,
            'job_type': 'full_time',
            'experience': 'mid',
            'salary_range': '100k_150k',
            'salary': '$110,000 - $130,000',
            'description': 'Join our team to develop machine learning models and extract insights from complex datasets for our Fortune 500 clients.',
            'requirements': [
                'MS or PhD in Computer Science, Statistics, or related field',
                '3+ years of experience in data science',
                'Proficiency in Python, R, and SQL',
                'Experience with machine learning frameworks (TensorFlow, PyTorch)',
                'Strong statistical analysis and problem-solving skills'
            ],
            'posted_date': '2023-05-11',
            'days_ago': 4,
            'category': 'technology'
        },
        {
            'id': 'job-6',
            'title': 'Elementary School Teacher',
            'company': 'Oakwood Elementary School',
            'company_logo': 'images/companies/oakwood-elementary.png',
            'location': 'Portland, OR',
            'remote': False,
            'job_type': 'full_time',
            'experience': 'entry',
            'salary_range': '50k_75k',
            'salary': '$52,000 - $60,000',
            'description': 'Seeking passionate educators to teach diverse elementary students in a supportive and collaborative environment.',
            'requirements': [
                'Bachelor\'s degree in Elementary Education',
                'Valid teaching certification/license',
                'Student teaching experience',
                'Knowledge of current curriculum standards',
                'Strong classroom management and communication skills'
            ],
            'posted_date': '2023-05-13',
            'days_ago': 2,
            'category': 'education'
        },
        {
            'id': 'job-7',
            'title': 'Mechanical Engineer',
            'company': 'Precision Engineering Solutions',
            'company_logo': 'images/companies/precision-engineering.png',
            'location': 'Detroit, MI',
            'remote': False,
            'job_type': 'full_time',
            'experience': 'mid',
            'salary_range': '75k_100k',
            'salary': '$85,000 - $100,000',
            'description': 'Design and develop mechanical components and systems for automotive applications using CAD tools and simulation software.',
            'requirements': [
                'Bachelor\'s degree in Mechanical Engineering',
                '3-5 years of experience in mechanical design',
                'Proficiency in CAD software (SolidWorks, AutoCAD)',
                'Knowledge of GD&T and manufacturing processes',
                'Problem-solving skills and attention to detail'
            ],
            'posted_date': '2023-05-08',
            'days_ago': 7,
            'category': 'engineering'
        },
        {
            'id': 'job-8',
            'title': 'UX/UI Designer',
            'company': 'Creative Digital Agency',
            'company_logo': 'images/companies/creative-digital.png',
            'location': 'Seattle, WA',
            'remote': True,
            'job_type': 'contract',
            'experience': 'mid',
            'salary_range': '75k_100k',
            'salary': '$90,000 - $100,000',
            'description': 'Create intuitive and visually appealing user interfaces for web and mobile applications, focusing on user experience and accessibility.',
            'requirements': [
                'Bachelor\'s degree in Design, HCI, or related field',
                '3+ years of experience in UX/UI design',
                'Proficiency in design tools (Figma, Sketch, Adobe XD)',
                'Portfolio demonstrating strong design skills',
                'Understanding of user-centered design principles'
            ],
            'posted_date': '2023-05-10',
            'days_ago': 5,
            'category': 'technology'
        }
    ]

    # Filter jobs based on search parameters
    filtered_jobs = job_listings

    if query:
        filtered_jobs = [job for job in filtered_jobs if
                         query.lower() in job['title'].lower() or
                         query.lower() in job['company'].lower() or
                         query.lower() in job['description'].lower()]

    if location:
        filtered_jobs = [job for job in filtered_jobs if location.lower() in job['location'].lower()]

    if job_type:
        filtered_jobs = [job for job in filtered_jobs if job['job_type'] == job_type]

    if experience_level:
        filtered_jobs = [job for job in filtered_jobs if job['experience'] == experience_level]

    if salary_range:
        filtered_jobs = [job for job in filtered_jobs if job['salary_range'] == salary_range]

    # Get featured jobs (could be based on employer partnerships, premium listings, etc.)
    featured_jobs = [job for job in job_listings if job.get('featured', False)]

    # Recent jobs (most recently posted)
    recent_jobs = sorted(job_listings, key=lambda x: x['posted_date'], reverse=True)[:5]

    context = {
        'job_listings': filtered_jobs,
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'job_types': job_types,
        'experience_levels': experience_levels,
        'salary_ranges': salary_ranges,
        'job_categories': job_categories,
        'query': query,
        'location': location,
        'job_type': job_type,
        'experience_level': experience_level,
        'salary_range': salary_range,
        'count': len(filtered_jobs)
    }

    return render(request, 'home/job_search.html', context)


def resume_formats(request):

    formats = [
        {
            'id': 'chronological',
            'name': 'Chronological',
            'best_for': 'Candidates with consistent work history',
            'description': 'Lists work experience in reverse chronological order, starting with the most recent position.',
            'structure': [
                'Contact information',
                'Professional summary or objective',
                'Work experience (most recent first)',
                'Education',
                'Skills',
                'Additional sections (certifications, awards, etc.)'
            ],
            'advantages': [
                'Shows career progression clearly',
                'Familiar to recruiters',
                'Preferred by most employers',
                'Highlights consistency and growth',
                'Works well with ATS systems'
            ],
            'disadvantages': [
                'Highlights employment gaps',
                'Less effective for career changers',
                'May not emphasize skills as much as experience',
                'Not ideal for those with limited work history'
            ],
            'example_cases': [
                'Professionals with steady career progression',
                'Job seekers staying within the same industry',
                'Candidates with no significant employment gaps',
                'Recent graduates with relevant internships or part-time work'
            ]
        },
        {
            'id': 'functional',
            'name': 'Functional',
            'best_for': 'Career changers or those with employment gaps',
            'description': 'Emphasizes skills and abilities rather than work history chronology.',
            'structure': [
                'Contact information',
                'Professional summary or objective',
                'Skills and qualifications (grouped by type)',
                'Achievements and accomplishments',
                'Work experience (minimal details)',
                'Education',
                'Additional sections'
            ],
            'advantages': [
                'Highlights transferable skills',
                'De-emphasizes employment gaps',
                'Good for career transitions',
                'Focuses on abilities rather than timeline',
                'Useful for those with diverse experience'
            ],
            'disadvantages': [
                'May raise red flags with recruiters',
                'Less common and sometimes less preferred',
                'Can appear to hide work history details',
                'May not perform well with ATS systems',
                'Requires strong skills categorization'
            ],
            'example_cases': [
                'Career changers entering a new field',
                'Candidates with significant employment gaps',
                'Those with varied work experience in different fields',
                'Professionals returning to the workforce after a break'
            ]
        },
        {
            'id': 'combination',
            'name': 'Combination (Hybrid)',
            'best_for': 'Experienced professionals with diverse skills',
            'description': 'Blends elements of chronological and functional formats, showcasing both skills and work history.',
            'structure': [
                'Contact information',
                'Professional summary',
                'Key skills and qualifications',
                'Work experience with accomplishments (chronological)',
                'Education',
                'Additional sections'
            ],
            'advantages': [
                'Highlights relevant skills and work history',
                'Flexible format for various situations',
                'Comprehensive presentation',
                'Can emphasize transferable skills while showing work timeline',
                'Good for senior positions requiring diverse expertise'
            ],
            'disadvantages': [
                'Can be longer than other formats',
                'May be complex to organize effectively',
                'Requires careful balance between skills and experience',
                'Can be redundant if not well-crafted',
                'Not always suitable for entry-level positions'
            ],
            'example_cases': [
                'Senior professionals with specialized skills',
                'Candidates with extensive experience in multiple relevant areas',
                'Those seeking positions requiring diverse qualifications',
                'Executives and managers with varied leadership experience'
            ]
        },
        {
            'id': 'targeted',
            'name': 'Targeted',
            'best_for': 'Specialists applying for specific positions',
            'description': 'Highly customized resume focused on specific job requirements, highlighting directly relevant experience and skills.',
            'structure': [
                'Contact information',
                'Position-specific professional summary',
                'Relevant skills and qualifications',
                'Targeted work experience and achievements',
                'Relevant education and training',
                'Specific certifications and qualifications'
            ],
            'advantages': [
                'Directly addresses job requirements',
                'Shows clear fit for the specific position',
                'Typically performs well in ATS systems',
                'Demonstrates research and commitment',
                'Highlights most relevant qualifications'
            ],
            'disadvantages': [
                'Requires significant customization for each application',
                'Time-consuming to create',
                'May not show full breadth of experience',
                'Less versatile for multiple applications',
                'Can feel repetitive of job description'
            ],
            'example_cases': [
                'Specialists applying for roles in their expertise area',
                'Candidates responding to detailed job descriptions',
                'Professionals targeting positions at specific companies',
                'Applicants for highly competitive positions'
            ]
        }
    ]

    context = {
        'formats': formats,
        'page_title': 'Resume Format Guide',
        'page_description': 'Find the perfect resume format for your career situation'
    }

    return render(request, 'home/resume_formats.html', context)


def resume_tips(request):

    # Resume tip categories
    categories = [
        {
            'id': 'general',
            'name': 'General Guidelines',
            'description': 'Essential principles for creating an effective resume'
        },
        {
            'id': 'content',
            'name': 'Content Optimization',
            'description': 'How to write compelling and impactful resume content'
        },
        {
            'id': 'ats',
            'name': 'ATS Optimization',
            'description': 'Techniques to ensure your resume passes through Applicant Tracking Systems'
        },
        {
            'id': 'format',
            'name': 'Resume Formats',
            'description': 'Different resume structures and when to use each one'
        },
        {
            'id': 'industry',
            'name': 'Industry-Specific Tips',
            'description': 'Tailored advice for different career fields'
        },
        {
            'id': 'checklist',
            'name': 'Final Checklist',
            'description': 'Essential items to review before submitting your resume'
        }
    ]

    # Industry-specific tips
    industries = [
        {
            'id': 'tech',
            'name': 'Technology',
            'keywords': ['Programming languages', 'Development methodologies', 'Technical certifications'],
            'advice': 'Highlight specific technologies, programming languages, and technical certifications. Include projects with measurable outcomes and contributions to technological advancements.'
        },
        {
            'id': 'business',
            'name': 'Business & Finance',
            'keywords': ['Revenue growth', 'Cost reduction', 'Process improvement'],
            'advice': 'Emphasize quantifiable achievements like revenue growth, cost savings, and process improvements. Include specific metrics that demonstrate business impact.'
        },
        {
            'id': 'healthcare',
            'name': 'Healthcare',
            'keywords': ['Patient care', 'Medical procedures', 'Regulatory compliance'],
            'advice': 'Focus on patient outcomes, compliance with regulations, and specialized medical knowledge. Include relevant certifications and experience with medical technologies.'
        },
        {
            'id': 'creative',
            'name': 'Creative Fields',
            'keywords': ['Portfolio highlights', 'Brand development', 'Creative process'],
            'advice': 'Showcase creative accomplishments, link to your portfolio, and describe creative processes. Highlight projects for notable clients or brands.'
        },
        {
            'id': 'education',
            'name': 'Education',
            'keywords': ['Student outcomes', 'Curriculum development', 'Teaching methodologies'],
            'advice': 'Emphasize teaching philosophy, student achievement metrics, and curriculum development. Include specialized training and educational technology proficiency.'
        }
    ]

    # Resume formats
    formats = [
        {
            'name': 'Chronological',
            'best_for': 'Candidates with consistent work history',
            'description': 'Lists work experience in reverse chronological order, starting with the most recent position.',
            'advantages': ['Shows career progression clearly', 'Familiar to recruiters', 'Preferred by most employers'],
            'disadvantages': ['Highlights employment gaps', 'Less effective for career changers']
        },
        {
            'name': 'Functional',
            'best_for': 'Career changers or those with employment gaps',
            'description': 'Emphasizes skills and abilities rather than work history chronology.',
            'advantages': ['Highlights transferable skills', 'De-emphasizes employment gaps',
                           'Good for career transitions'],
            'disadvantages': ['May raise red flags with recruiters', 'Less common and sometimes less preferred']
        },
        {
            'name': 'Combination',
            'best_for': 'Experienced professionals with diverse skills',
            'description': 'Blends elements of chronological and functional formats, showcasing both skills and work history.',
            'advantages': ['Highlights relevant skills and work history', 'Flexible format for various situations',
                           'Comprehensive presentation'],
            'disadvantages': ['Can be longer than other formats', 'May be complex to organize effectively']
        }
    ]

    # Action verbs by category
    action_verbs = {
        'leadership': ['Led', 'Managed', 'Directed', 'Supervised', 'Coordinated', 'Oversaw', 'Established',
                       'Pioneered'],
        'achievement': ['Achieved', 'Exceeded', 'Improved', 'Increased', 'Reduced', 'Enhanced', 'Accelerated',
                        'Maximized'],
        'communication': ['Presented', 'Negotiated', 'Authored', 'Corresponded', 'Persuaded', 'Publicized',
                          'Translated'],
        'analysis': ['Analyzed', 'Assessed', 'Evaluated', 'Researched', 'Investigated', 'Calculated', 'Formulated'],
        'creation': ['Created', 'Designed', 'Developed', 'Established', 'Founded', 'Initiated', 'Introduced',
                     'Launched'],
        'improvement': ['Streamlined', 'Restructured', 'Reorganized', 'Revamped', 'Transformed', 'Upgraded',
                        'Optimized']
    }

    context = {
        'categories': categories,
        'industries': industries,
        'formats': formats,
        'action_verbs': action_verbs,
        'page_title': 'Resume Writing Tips',
        'page_description': 'Expert advice to create a resume that gets you noticed and hired'
    }

    return render(request, 'home/resume_tips.html', context)


def job_matching(request):

    # You might eventually implement job matching algorithms here
    # For now, this is just a placeholder
    context = {
        'job_matches': [],  # This would eventually be populated with actual job matches
        'match_count': 0
    }
    return render(request, 'home/job_matching.html', context)


@login_required
def dashboard(request):
    # You can add actual models and queries later
    context = {
        'resumes_count': 0,  # Resume.objects.filter(user=request.user).count(),
        'applications_count': 0,  # JobApplication.objects.filter(user=request.user).count(),
        'downloads_count': 0,  # DownloadHistory.objects.filter(user=request.user).count(),
        'recent_resumes': [],  # Resume.objects.filter(user=request.user).order_by('-updated_at')[:5],
        'activity_logs': [],  # ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:5],
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def job_applications(request):

    return render(request, 'dashboard/job_applications.html', {'applications': []})

@login_required
def add_application(request):
    """View for adding a new job application."""
    # Form handling logic will go here
    return render(request, 'dashboard/add_application.html')

@login_required
def profile_settings(request):
    """View for user profile settings."""
    return render(request, 'dashboard/profile_settings.html')

@login_required
def subscription_details(request):
    """View for displaying and managing subscription details."""
    return render(request, 'dashboard/subscription.html')

@login_required
def resume_list(request):
    """View for listing all user resumes."""
    return render(request, 'dashboard/resume_list.html', {'resumes': []})



@login_required
def download_resume(request, resume_id):
    """View for downloading a resume as PDF."""
    # Logic for generating and serving PDF
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume_id}.pdf"'
    # PDF generation logic
    return response


from django.shortcuts import render


def features_cv(request):
    """
    View to display the features of the CV builder.
    """
    # Example data to pass to the template
    features = [
        {
            'title': 'Professional Templates',
            'description': 'Choose from dozens of ATS-friendly templates designed by HR professionals.',
            'icon': 'fas fa-file-alt'
        },
        {
            'title': 'AI Content Suggestions',
            'description': 'Get personalized content suggestions based on your industry and experience.',
            'icon': 'fas fa-magic'
        },
        {
            'title': 'Multiple Export Options',
            'description': 'Download your CV as PDF, DOCX, or TXT, ready to submit to employers.',
            'icon': 'fas fa-download'
        },
        {
            'title': 'ATS Optimization',
            'description': 'Our CV builder ensures your document passes Applicant Tracking Systems.',
            'icon': 'fas fa-check-circle'
        },
        {
            'title': 'Section Management',
            'description': 'Easily add, remove, and reorder sections to highlight your strengths.',
            'icon': 'fas fa-layer-group'
        },
        {
            'title': 'Multilingual Support',
            'description': 'Create CVs in multiple languages for international job applications.',
            'icon': 'fas fa-language'
        }
    ]

    return render(request, 'home/features_resume.html', {'features': features})


class CoverLetterListView(LoginRequiredMixin, ListView):
    model = CoverLetter
    template_name = 'home/cover_letter/list.html'
    context_object_name = 'cover_letters'
    paginate_by = 10

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

class CoverLetterDetailView(LoginRequiredMixin, DetailView):
    model = CoverLetter
    template_name = 'home/cover_letter/detail.html'
    context_object_name = 'cover_letter'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

class CoverLetterCreateView(LoginRequiredMixin, CreateView):
    model = CoverLetter
    form_class = CoverLetterForm
    template_name = 'home/cover_letter/form.html'
    success_url = reverse_lazy('home:cover_letter')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CoverLetterEditView(LoginRequiredMixin, UpdateView):
    model = CoverLetter
    form_class = CoverLetterForm
    template_name = 'home/cover_letter/form.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

class CoverLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = CoverLetter
    template_name = 'home/cover_letter/confirm_delete.html'
    success_url = reverse_lazy('home:cover_letter')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

class CoverLetterTemplateListView(ListView):
    model = CoverLetterTemplate
    template_name = 'home/cover_letter/list.html'
    context_object_name = 'templates'
    paginate_by = 12

    def get_queryset(self):
        return CoverLetterTemplate.objects.filter(is_active=True)

class CoverLetterTemplateDetailView(DetailView):
    model = CoverLetterTemplate
    template_name = 'home/cover_letter/templates/detail.html'
    context_object_name = 'template'


class CVTemplateListView(ListView):
    model = CVTemplate
    template_name = 'home/cv_templates/list.html'
    context_object_name = 'templates'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CVTemplate.objects.values_list(
            'category', flat=True).distinct()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(is_active=True)


class CVTemplateDetailView(DetailView):
    model = CVTemplate
    template_name = 'home/cv_templates/detail.html'
    context_object_name = 'template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CVTemplateSelectForm()
        context['related_templates'] = CVTemplate.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        ).filter(
            is_active=True
        )[:3]
        return context


class CVTemplateSelectView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = CVTemplateSelectForm
    template_name = 'home/cv_templates/select.html'
    success_url = reverse_lazy('home:resume_builder')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.template = get_object_or_404(
            CVTemplate,
            slug=self.kwargs['slug']
        )
        return super().form_valid(form)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'home/blog/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogPost.objects.values_list(
            'category', flat=True).distinct()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(status='published')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'home/blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related posts
        context['related_posts'] = BlogPost.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        ).filter(
            status='published'
        )[:3]
        return context


class ResumeExamplesView(ListView):
    model = ResumeExample
    template_name = 'resume_examples/list.html'
    context_object_name = 'examples'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResumeExample.objects.values_list(
            'category', flat=True).distinct()
        context['current_category'] = self.kwargs.get('category')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(is_published=True).order_by('-created_at')


class CareerAdviceListView(ListView):
    model = CareerAdvice
    template_name = 'home/career_advice/list.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CareerAdvice.objects.values_list(
            'category', flat=True).distinct()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(status='published')


class CareerAdviceDetailView(DetailView):
    model = CareerAdvice
    template_name = 'home/career_advice/detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related articles
        context['related_articles'] = CareerAdvice.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        ).filter(
            status='published'
        )[:3]
        return context


class ExportPDFView(LoginRequiredMixin, View):
    """
    Export resume as a PDF document with customizable styling and layout
    """

    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            # Get template preference
            template_name = request.GET.get('template', 'default')

            # Get styling preferences
            styling = {
                'font_size': request.GET.get('font_size', '11'),
                'margin': request.GET.get('margin', '1'),
                'line_spacing': request.GET.get('line_spacing', '1.15'),
                'include_photo': request.GET.get('include_photo', 'false') == 'true',
                'color_scheme': request.GET.get('color_scheme', 'professional')
            }

            # Initialize PDF exporter with options
            exporter = PDFExporter(
                resume=resume,
                template_name=template_name,
                styling=styling
            )

            # Generate PDF
            pdf_path = exporter.generate()

            # Check if user wants to preview or download
            if request.GET.get('preview', 'false') == 'true':
                response = FileResponse(
                    open(pdf_path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = 'inline; filename="resume_preview.pdf"'
            else:
                # Generate filename based on resume title
                filename = f"{resume.title.lower().replace(' ', '_')}.pdf"
                response = FileResponse(
                    open(pdf_path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Clean up temporary file after sending
            os.unlink(pdf_path)
            return response

        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'message': 'Failed to generate PDF'
            }, status=500)

    def post(self, request, uuid):
        """Handle custom PDF generation settings"""
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            # Get custom settings from POST data
            custom_settings = {
                'page_size': request.POST.get('page_size', 'A4'),
                'font_family': request.POST.get('font_family', 'Helvetica'),
                'primary_color': request.POST.get('primary_color', '#000000'),
                'secondary_color': request.POST.get('secondary_color', '#666666'),
                'section_spacing': request.POST.get('section_spacing', '20'),
                'header_style': request.POST.get('header_style', 'standard'),
                'include_page_numbers': request.POST.get('include_page_numbers', 'true') == 'true',
                'custom_css': request.POST.get('custom_css', '')
            }

            # Initialize PDF exporter with custom settings
            exporter = PDFExporter(
                resume=resume,
                custom_settings=custom_settings
            )

            # Generate PDF with custom settings
            pdf_path = exporter.generate()

            # Return the PDF file
            filename = f"{resume.title.lower().replace(' ', '_')}_custom.pdf"
            response = FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Clean up temporary file after sending
            os.unlink(pdf_path)
            return response

        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'message': 'Failed to generate custom PDF'
            }, status=500)


class ExportTextView(LoginRequiredMixin, View):
    """
    Export resume as a plain text document with formatting options
    """

    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            # Get formatting preferences
            width = int(request.GET.get('width', '80'))
            include_styling = request.GET.get('include_styling', 'false') == 'true'
            format_type = request.GET.get('format', 'plain')  # plain, markdown, or ascii

            # Generate text content
            content = self.generate_text_content(
                resume,
                width=width,
                include_styling=include_styling,
                format_type=format_type
            )

            # Determine file extension based on format
            extensions = {
                'plain': 'txt',
                'markdown': 'md',
                'ascii': 'txt'
            }
            ext = extensions.get(format_type, 'txt')

            # Generate filename
            filename = f"{resume.title.lower().replace(' ', '_')}.{ext}"

            # Create response
            response = HttpResponse(content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'message': 'Failed to generate text file'
            }, status=500)

    def generate_text_content(self, resume, width=80, include_styling=False, format_type='plain'):
        """Generate formatted text content from resume"""
        content = []

        # Header section
        if format_type == 'markdown':
            content.append(f"# {resume.title}\n")
        elif format_type == 'ascii':
            content.append("=" * width)
            content.append(resume.title.center(width))
            content.append("=" * width)
        else:
            content.append("=" * width)
            content.append(resume.title.upper())
            content.append("=" * width)

        # Personal Information
        personal_section = resume.sections.filter(type='personal').first()
        if personal_section:
            personal_info = personal_section.content
            if format_type == 'markdown':
                content.append("\n## Personal Information\n")
                for key, value in personal_info.items():
                    if value:
                        content.append(f"* **{key.title()}:** {value}")
            else:
                content.append("\nPERSONAL INFORMATION")
                content.append("-" * width)
                for key, value in personal_info.items():
                    if value:
                        content.append(f"{key.title()}: {value}")

        # Other Sections
        for section in resume.sections.all().order_by('order'):
            if section.type != 'personal':
                content.append("\n" + "=" * width)

                if format_type == 'markdown':
                    content.append(f"\n## {section.title}\n")
                else:
                    content.append(f"\n{section.title.upper()}\n")

                if section.type == 'experience':
                    content.extend(self.format_experience_section(
                        section, width, format_type))
                elif section.type == 'education':
                    content.extend(self.format_education_section(
                        section, width, format_type))
                elif section.type == 'skills':
                    content.extend(self.format_skills_section(
                        section, width, format_type))
                elif section.type == 'languages':
                    content.extend(self.format_languages_section(
                        section, width, format_type))

        # Join all content with proper line endings
        return "\n".join(content)

    def format_experience_section(self, section, width, format_type):
        """Format work experience section"""
        content = []
        for exp in section.experiences.all():
            if format_type == 'markdown':
                content.append(f"### {exp.company}")
                content.append(f"**{exp.position}**")
                content.append(f"_{exp.start_date.strftime('%B %Y')} - "
                               f"{'Present' if exp.is_current else exp.end_date.strftime('%B %Y')}_\n")
                if exp.description:
                    content.append(exp.description + "\n")
            else:
                content.append(exp.company)
                content.append(exp.position)
                content.append(f"{exp.start_date.strftime('%B %Y')} - "
                               f"{'Present' if exp.is_current else exp.end_date.strftime('%B %Y')}")
                if exp.description:
                    content.extend(textwrap.wrap(exp.description, width))
                content.append("")
        return content

    def format_education_section(self, section, width, format_type):
        """Format education section"""
        content = []
        for edu in section.education.all():
            if format_type == 'markdown':
                content.append(f"### {edu.institution}")
                content.append(f"**{edu.degree}**\n")
            else:
                content.append(edu.institution)
                content.append(edu.degree)
                content.append("")
        return content

    def format_skills_section(self, section, width, format_type):
        """Format skills section"""
        content = []
        skills = section.skills.all()
        if format_type == 'markdown':
            for skill in skills:
                content.append(f"* **{skill.name}** - {skill.level}")
        else:
            skill_groups = {}
            for skill in skills:
                if skill.level not in skill_groups:
                    skill_groups[skill.level] = []
                skill_groups[skill.level].append(skill.name)

            for level, skill_list in skill_groups.items():
                content.append(f"{level}:")
                content.append("  " + ", ".join(skill_list))
                content.append("")
        return content

    def format_languages_section(self, section, width, format_type):
        """Format languages section"""
        content = []
        languages = section.languages.all()
        if format_type == 'markdown':
            for lang in languages:
                content.append(f"* **{lang.name}** - {lang.level}")
        else:
            for lang in languages:
                content.append(f"{lang.name} - {lang.level}")
        return content


class ResumePreviewView(LoginRequiredMixin, DetailView):
    """
    Display a preview of the resume with live updates
    """
    model = Resume
    template_name = 'resume_builder/preview.html'
    context_object_name = 'resume'

    def get_object(self):
        return get_object_or_404(Resume, uuid=self.kwargs['uuid'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()

        # Get all sections ordered by their position
        context['sections'] = resume.sections.all().order_by('order')

        # Get template-specific data
        if resume.template:
            context['template_css'] = resume.template.get_css()
            context['template_js'] = resume.template.get_js()

        # Add custom styling
        context['custom_styles'] = {
            'colors': resume.custom_colors,
            'fonts': resume.custom_fonts,
            'spacing': resume.custom_spacing
        }

        return context

    def post(self, request, *args, **kwargs):
        """Handle AJAX requests for live preview updates"""
        resume = self.get_object()
        section_id = request.POST.get('section_id')
        content = request.POST.get('content')

        if section_id and content:
            section = get_object_or_404(ResumeSection, id=section_id, resume=resume)
            section.content = json.loads(content)
            section.save()

            # Render the updated section
            html = render_to_string(
                f'resume_builder/sections/{section.type}.html',
                {'section': section}
            )
            return JsonResponse({'html': html})
        return JsonResponse({'error': 'Invalid request'}, status=400)


class SaveContentView(LoginRequiredMixin, View):
    """
    Save resume content via AJAX
    """

    def post(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
        try:
            data = json.loads(request.body)
            section_id = data.get('section_id')
            content = data.get('content')

            if section_id and content:
                section = get_object_or_404(ResumeSection, id=section_id, resume=resume)
                section.content = content
                section.save()
                return JsonResponse({'status': 'success'})

            return JsonResponse({'error': 'Missing data'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ExportWordView(LoginRequiredMixin, View):
    """
    Export resume as a Word document
    """

    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            # Generate Word document
            exporter = WordExporter(resume)
            doc_path = exporter.generate()

            # Prepare response
            filename = os.path.basename(doc_path)
            response = FileResponse(
                open(doc_path, 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ExportPDFView(LoginRequiredMixin, View):
    """
    Export resume as a PDF document
    """

    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            # Generate PDF
            exporter = PDFExporter(resume)
            pdf_path = exporter.generate()

            # Prepare response
            filename = os.path.basename(pdf_path)
            response = FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AISuggestView(LoginRequiredMixin, View):
    """
    Get AI suggestions for resume content
    """

    def post(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
        ai = AIHelper()

        try:
            data = json.loads(request.body)
            section_type = data.get('section_type')
            content = data.get('content')

            if not section_type or not content:
                return JsonResponse({'error': 'Missing data'}, status=400)

            suggestions = {}

            if section_type == 'experience':
                # Generate improved bullet points
                suggestions['bullets'] = ai.generate_bullet_points(content)
                # Suggest achievements
                suggestions['achievements'] = ai.get_achievement_suggestions(
                    content.get('position', ''),
                    content.get('description', '')
                )

            elif section_type == 'skills':
                # Suggest relevant skills
                suggestions['skills'] = ai.suggest_skills(content)

            elif section_type == 'summary':
                # Improve summary text
                suggestions['improved_text'] = ai.improve_text(content)

            return JsonResponse({'suggestions': suggestions})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AIAnalyzeView(LoginRequiredMixin, View):
    """
    Get AI analysis of the entire resume
    """

    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
        ai = AIHelper()

        try:
            # Prepare resume data for analysis
            resume_data = {
                'sections': [
                    {
                        'type': section.type,
                        'title': section.title,
                        'content': section.content
                    }
                    for section in resume.sections.all()
                ]
            }

            # Get AI analysis
            analysis = ai.analyze_resume(resume_data)

            return JsonResponse({'analysis': analysis})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CustomizeLayoutView(LoginRequiredMixin, View):
    """
    Save custom layout settings for the resume
    """

    def post(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)

        try:
            data = json.loads(request.body)

            # Update custom styling
            if 'colors' in data:
                resume.custom_colors = data['colors']
            if 'fonts' in data:
                resume.custom_fonts = data['fonts']
            if 'spacing' in data:
                resume.custom_spacing = data['spacing']

            resume.save()

            # Return updated preview HTML
            html = render_to_string(
                'home/preview.html',
                {
                    'resume': resume,
                    'sections': resume.sections.all().order_by('order'),
                    'custom_styles': {
                        'colors': resume.custom_colors,
                        'fonts': resume.custom_fonts,
                        'spacing': resume.custom_spacing
                    }
                }
            )

            return JsonResponse({
                'status': 'success',
                'html': html
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class TemplateListView(ListView):
    model = ResumeTemplate
    template_name = 'resume_builder/template_list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            return queryset.filter(category=category)
        return queryset


class TemplateDetailView(DetailView):
    model = ResumeTemplate
    template_name = 'resume_builder/template_detail.html'
    context_object_name = 'template'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.template = get_object_or_404(
            ResumeTemplate,
            slug=self.kwargs['template_slug']
        )
        return super().form_valid(form)


class ResumeEditView(LoginRequiredMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume_form.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AddSectionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        resume = get_object_or_404(Resume, uuid=data['resume_uuid'], user=request.user)

        section = ResumeSection.objects.create(
            resume=resume,
            title=data['title'],
            type=data['type'],
            order=data.get('order', 0)
        )

        return JsonResponse({
            'id': section.id,
            'title': section.title,
            'html': section.get_html()
        })


class UpdateSectionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        section = get_object_or_404(ResumeSection,
                                    pk=pk,
                                    resume__user=request.user)
        data = json.loads(request.body)

        section.content = data.get('content', section.content)
        section.title = data.get('title', section.title)
        section.save()

        return JsonResponse({'status': 'success'})


class DeleteSectionView(LoginRequiredMixin, DeleteView):
    model = ResumeSection

    def get_queryset(self):
        return super().get_queryset().filter(resume__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'success'})


class ReorderSectionsView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        for item in data['sections']:
            section = get_object_or_404(
                ResumeSection,
                id=item['id'],
                resume__user=request.user
            )
            section.order = item['order']
            section.save()
        return JsonResponse({'status': 'success'})


class AutoSaveView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        resume = get_object_or_404(
            Resume,
            uuid=data['resume_uuid'],
            user=request.user
        )
        resume.content = data['content']
        resume.save()
        return JsonResponse({'status': 'success'})


class ExportPDFView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        resume = get_object_or_404(Resume, uuid=uuid, user=request.user)
        pdf = PDFExporter(resume).generate()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
        return response


class AIImproveView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        content = data['content']
        improved_content = AIHelper.improve_content(content)
        return JsonResponse({'improved_content': improved_content})


class CustomizeColorsView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        resume = get_object_or_404(
            Resume,
            uuid=data['resume_uuid'],
            user=request.user
        )
        resume.custom_colors = data['colors']
        resume.save()
        return JsonResponse({'status': 'success'})


class CustomizeFontsView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        resume = get_object_or_404(
            Resume,
            uuid=data['resume_uuid'],
            user=request.user
        )
        resume.custom_fonts = data['fonts']
        resume.save()
        return JsonResponse({'status': 'success'})


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        context['features'] = Feature.objects.filter(show_on_homepage=True)
        return context

class PricingView(TemplateView):
    template_name = 'home/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pricing_plans'] = Pricing.objects.filter(is_active=True)
        context['faqs'] = FAQ.objects.filter(category='pricing')
        return context

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        context['company_stats'] = CompanyStats.objects.first()
        return context

class ContactView(FormView):
    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()  # Save the contact message to database
        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission. Please try again.')
        return super().form_invalid(form)

class TermsView(TemplateView):
    template_name = 'home/terms.html'

class PrivacyView(TemplateView):
    template_name = 'home/privacy.html'


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_builder/dashboard.html', {
        'resumes': resumes
    })


@login_required
def create_resume(request, template_slug=None):
    """Create a new resume, optionally based on a template"""
    # First, try to find the template
    if template_slug:
        template = get_object_or_404(ResumeTemplate, slug=template_slug)
    else:
        # If no template specified, use the first simple template
        template = ResumeTemplate.objects.filter(category='simple').first()
        if not template:
            # Fallback to any template if no simple ones exist
            template = ResumeTemplate.objects.first()

    # Create a new resume without the template for now
    resume = Resume(
        user=request.user,
        title="My Resume",
    )

    # Save the resume first without the template
    resume.save()

    # Now try to handle the template assignment
    if template:
        try:
            # Try to find the corresponding Template object
            from django.apps import apps
            Template = apps.get_model('dashboard', 'Template')  # Adjust app name if needed

            # Try to find a Template with the same ID or slug as the ResumeTemplate
            template_obj = None
            try:
                template_obj = Template.objects.get(id=template.id)
            except Template.DoesNotExist:
                # If that fails, try to find by slug if Template has a slug field
                if hasattr(Template, 'slug'):
                    try:
                        template_obj = Template.objects.get(slug=template.slug)
                    except (Template.DoesNotExist, AttributeError):
                        pass

            # If we found a Template object, assign it
            if template_obj:
                resume.template = template_obj
                resume.save()
        except Exception as e:
            # Log the error but continue
            print(f"Error setting template: {e}")

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
            title=section["title"],
            order=section["order"],
        )

    # Redirect to the resume editor using the resume ID
    return redirect('home:edit_resume', resume_id=resume.id)


class ResumeBuilderView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/builder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = get_object_or_404(
            ResumeTemplate,
            slug=self.kwargs['template_slug']
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.template = get_object_or_404(
            ResumeTemplate,
            slug=self.kwargs['template_slug']
        )
        return super().form_valid(form)


class SaveResumeView(LoginRequiredMixin, UpdateView):
    model = Resume
    fields = ['content', 'name']
    http_method_names = ['post']

    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({'status': 'success'})


class DownloadResumeView(LoginRequiredMixin, DetailView):
    model = Resume

    def get(self, request, *args, **kwargs):
        resume = self.get_object()
        pdf = resume.generate_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.name}.pdf"'
        return response


class PreviewResumeView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume_builder/preview.html'
    context_object_name = 'resume'



class ResumeFeatureView(TemplateView):
    template_name = 'home/features_resume.html'


class CoverLetterFeatureView(TemplateView):
    template_name = 'home/features_cover_letter.html'



class HelpCenterView(TemplateView):
    template_name = 'home/help.html'


def features_resume(request):
    """
    View to display the features of the resume builder.
    """
    # Example data to pass to the template
    features = [
        {
            'title': 'Easy to Use',
            'description': 'Our resume builder is user-friendly and intuitive, making it easy for anyone to create a professional resume.',
            'icon': 'fas fa-user-check'
        },
        {
            'title': 'Customizable Templates',
            'description': 'Choose from a variety of templates and customize them to fit your personal style and career needs.',
            'icon': 'fas fa-paint-brush'
        },
        {
            'title': 'Real-time Preview',
            'description': 'See how your resume looks as you build it with our real-time preview feature.',
            'icon': 'fas fa-eye'
        },
        {
            'title': 'Download and Share',
            'description': 'Easily download your resume in multiple formats or share it directly with potential employers.',
            'icon': 'fas fa-download'
        }
    ]

    return render(request, 'home/features_resume.html', {'features': features})






@login_required
def my_resumes(request):
    """View for displaying user's resumes"""
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')

    return render(request, 'dashboard/my_resumes.html', {
        'resumes': resumes
    })


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


# Career Advice Views
def career_advice_list(request):
    """Display a list of career advice articles."""
    articles = CareerArticle.objects.filter(is_published=True)
    featured_article = CareerArticle.objects.filter(is_published=True, is_featured=True).first()

    # Pagination
    paginator = Paginator(articles, 9)  # Show 9 articles per page
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'featured_article': featured_article,
        'is_paginated': True,
        'paginator': paginator,
        'page_obj': articles,
    }

    return render(request, 'home/career_advice/list.html', context)


def career_advice_detail(request, slug):
    """Display a single career advice article."""
    article = get_object_or_404(CareerArticle, slug=slug, is_published=True)
    article.increment_view_count()

    # Get related articles
    related_articles = CareerArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }

    return render(request, 'home/career_advice/detail.html', context)


def career_advice_category(request, category_slug):
    """Display articles filtered by category."""
    category = get_object_or_404(CareerCategory, slug=category_slug)
    articles = CareerArticle.objects.filter(category=category, is_published=True)

    # Pagination
    paginator = Paginator(articles, 9)  # Show 9 articles per page
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'articles': articles,
        'selected_category': category_slug,
        'is_paginated': True,
        'paginator': paginator,
        'page_obj': articles,
    }

    return render(request, 'home/career_advice/list.html', context)


def career_advice_search(request):
    """Search for career advice articles."""
    form = CareerAdviceSearchForm(request.GET)
    query = request.GET.get('q', '')

    if query:
        articles = CareerArticle.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query),
            is_published=True
        )
    else:
        articles = CareerArticle.objects.none()

    # Pagination
    paginator = Paginator(articles, 9)  # Show 9 articles per page
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'query': query,
        'articles': articles,
        'is_paginated': True,
        'paginator': paginator,
        'page_obj': articles,
    }

    return render(request, 'home/career_advice/search_results.html', context)


def newsletter_subscribe(request):
    """Handle newsletter subscription."""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if email already exists
            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.info(request, "You're already subscribed to our newsletter!")
            else:
                form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "Please enter a valid email address.")

    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'career_advice'))


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Resume, ResumeSection, Template, ResumeTemplate


@login_required
def resume_edit(request, resume_id):
    """
    View for editing an existing resume
    """
    # Get the resume object, ensuring it belongs to the current user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Get all sections for this resume
    sections = resume.sections.all().order_by('order')

    # If this is a POST request, update the resume
    if request.method == 'POST':
        # Update basic resume information
        resume.title = request.POST.get('title', resume.title)
        resume.full_name = request.POST.get('full_name', resume.full_name)
        resume.email = request.POST.get('email', resume.email)
        resume.phone = request.POST.get('phone', resume.phone)
        resume.location = request.POST.get('location', resume.location)
        resume.headline = request.POST.get('headline', resume.headline)
        resume.summary = request.POST.get('summary', resume.summary)

        # Save the updated resume
        resume.save()

        # Show success message
        messages.success(request, 'Resume updated successfully!')

        # Redirect back to the edit page
        return redirect('templates_app:resume_edit', resume_id=resume.id)

    # Get available templates for template switching
    templates = ResumeTemplate.objects.filter(is_active=True)

    # Render the edit template with the resume data
    context = {
        'resume': resume,
        'sections': sections,
        'templates': templates,
        'active_tab': 'edit',  # For highlighting the active tab in navigation
    }

    return render(request, 'templates_app/edit_resume.html', context)


@login_required
@require_http_methods(["POST"])
def update_resume_section(request, resume_id, section_id):
    """
    API endpoint for updating a resume section
    """
    # Get the resume and section, ensuring they belong to the current user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    section = get_object_or_404(ResumeSection, id=section_id, resume=resume)

    # Update section data
    section.title = request.POST.get('title', section.title)
    section.order = request.POST.get('order', section.order)

    # Save the updated section
    section.save()

    # Return success response
    return JsonResponse({
        'success': True,
        'message': 'Section updated successfully',
        'section': {
            'id': section.id,
            'title': section.title,
            'order': section.order,
        }
    })


@login_required
@require_http_methods(["POST"])
def create_resume_section(request, resume_id):
    """
    API endpoint for creating a new resume section
    """
    # Get the resume, ensuring it belongs to the current user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Get the highest order value to place the new section at the end
    highest_order = resume.sections.aggregate(models.Max('order'))['order__max'] or 0

    # Create new section
    section = ResumeSection.objects.create(
        resume=resume,
        title=request.POST.get('title', 'New Section'),
        order=highest_order + 1,
    )

    # Return success response
    return JsonResponse({
        'success': True,
        'message': 'Section created successfully',
        'section': {
            'id': section.id,
            'title': section.title,
            'order': section.order,
        }
    })


@login_required
@require_http_methods(["DELETE"])
def delete_resume_section(request, resume_id, section_id):
    """
    API endpoint for deleting a resume section
    """
    # Get the resume and section, ensuring they belong to the current user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    section = get_object_or_404(ResumeSection, id=section_id, resume=resume)

    # Delete the section
    section.delete()

    # Return success response
    return JsonResponse({
        'success': True,
        'message': 'Section deleted successfully',
    })


@login_required
@require_http_methods(["POST"])
def change_resume_template(request, resume_id):
    """
    API endpoint for changing a resume's template
    """
    # Get the resume, ensuring it belongs to the current user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Get the template
    template_id = request.POST.get('template_id')
    if not template_id:
        return JsonResponse({
            'success': False,
            'message': 'Template ID is required',
        }, status=400)

    # Get the ResumeTemplate
    resume_template = get_object_or_404(ResumeTemplate, id=template_id)

    # Update the resume's template
    resume.template = resume_template.template
    resume.save()

    # Return success response
    return JsonResponse({
        'success': True,
        'message': 'Template changed successfully',
    })


