from django import forms
from django import forms
from django.core.exceptions import ValidationError

from django import forms
from django import forms
# from .models import NewsletterSubscription, CareerArticle

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
       # model = NewsletterSubscription
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name (optional)'})
        }

class CareerAdviceSearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for career advice...'
        })
    )




class CoverLetterForm(forms.ModelForm):
    class Meta:
#        model = CoverLetter
        fields = [
            'title',
            'company_name',
            'job_title',
            'recipient_name',
            'recipient_title',
            'company_address',
            'content',
            'template'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'template': forms.Select(attrs={'class': 'form-control'})
        }


class CVTemplateSelectForm(forms.ModelForm):
    class Meta:
        #model = Resume
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter resume title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter resume description',
                'rows': 3
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long")
        return title.strip()


class ResumeForm(forms.ModelForm):
    class Meta:
#        model = Resume
        fields = ['title', 'template', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter resume title'
            }),
        }


from django import forms
# from .models import ResumeSection


class ResumeSectionForm(forms.ModelForm):
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter achievements (one per line)',
            'rows': 4
        }),
        required=False,
        help_text="Enter each achievement on a new line"
    )

    class Meta:
#        model = ResumeSection
        fields = [
            'type',
            'title',
            'company',
            'position',
            'location',
            'employment_type',
            'company_website',
            'start_date',
            'end_date',
            'is_current',
            'description',
            'achievements',
            'order',
            'is_visible'
        ]
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'handleSectionTypeChange(this)'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Section title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country or Remote'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://company.com'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'toggleEndDate(this)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your responsibilities and achievements'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_visible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional by default
        for field in self.fields:
            self.fields[field].required = False

        # Make required fields mandatory
        self.fields['type'].required = True
        self.fields['title'].required = True

    def clean(self):
        cleaned_data = super().clean()
        section_type = cleaned_data.get('type')

        # Validate work experience fields
        if section_type == 'experience':
            required_fields = ['company', 'position', 'start_date']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for work experience sections.')

            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            is_current = cleaned_data.get('is_current')

            if start_date and end_date and not is_current:
                if end_date < start_date:
                    raise forms.ValidationError("End date cannot be earlier than start date")

            if is_current:
                cleaned_data['end_date'] = None

            # Convert achievements from text to list
            achievements_text = cleaned_data.get('achievements', '')
            if achievements_text:
                cleaned_data['achievements'] = [
                    achievement.strip()
                    for achievement in achievements_text.split('\n')
                    if achievement.strip()
                ]
            else:
                cleaned_data['achievements'] = []

        return cleaned_data

from django import forms
# from .models import WorkExperience

class WorkExperienceForm(forms.ModelForm):
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter achievements (one per line)',
            'rows': 4
        }),
        required=False,
        help_text="Enter each achievement on a new line"
    )

    class Meta:
#        model = WorkExperience
        fields = [
            'company',
            'position',
            'location',
            'employment_type',
            'start_date',
            'end_date',
            'is_current',
            'description',
            'achievements',
            'company_website',
            'order'
        ]
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country or Remote'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'toggleEndDate(this)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your responsibilities and achievements'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://company.com'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')

        if start_date and end_date and not is_current:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be earlier than start date")

        if is_current:
            cleaned_data['end_date'] = None

        # Convert achievements from text to list
        achievements_text = cleaned_data.get('achievements', '')
        if achievements_text:
            cleaned_data['achievements'] = [
                achievement.strip()
                for achievement in achievements_text.split('\n')
                if achievement.strip()
            ]
        else:
            cleaned_data['achievements'] = []

        return cleaned_data


from django import forms
#from .models import Education

class EducationForm(forms.ModelForm):
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter achievements and honors (one per line)',
            'rows': 4
        }),
        required=False,
        help_text="Enter each achievement on a new line"
    )

    class Meta:
#        model = Education
        fields = [
            'institution',
            'degree',
            'field_of_study',
            'location',
            'start_date',
            'end_date',
            'is_current',
            'gpa',
            'achievements',
            'activities',
            'description',
            'order'
        ]
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'School or University name'
            }),
            'degree': forms.Select(attrs={
                'class': 'form-select'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Major or field of study'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, State/Province, Country'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'toggleEducationEndDate(this)'
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3.50',
                'step': '0.01',
                'min': '0',
                'max': '4.0'
            }),
            'activities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Extracurricular activities, societies, etc.'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional details about your studies'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')
        gpa = cleaned_data.get('gpa')

        if start_date and end_date and not is_current:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be earlier than start date")

        if is_current:
            cleaned_data['end_date'] = None

        if gpa is not None and (gpa < 0 or gpa > 4.0):
            raise forms.ValidationError("GPA must be between 0.0 and 4.0")

        # Convert achievements from text to list
        achievements_text = cleaned_data.get('achievements', '')
        if achievements_text:
            cleaned_data['achievements'] = [
                achievement.strip()
                for achievement in achievements_text.split('\n')
                if achievement.strip()
            ]
        else:
            cleaned_data['achievements'] = []

        return cleaned_data


from django import forms
# from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
#        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter skill name'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError("Skill name must be at least 2 characters long")
        return name.strip()


from django import forms
#from .models import Language

class LanguageForm(forms.ModelForm):
    class Meta:
      #  model = Language
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter language name'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError("Language name must be at least 2 characters long")
        return name.strip()


class CertificationForm(forms.ModelForm):
    class Meta:
        #model = Certification
        fields = [
            'name', 'issuing_organization', 'issue_date',
            'expiry_date', 'credential_id', 'credential_url', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certification name'
            }),
            'issuing_organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Issuing organization'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'credential_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Credential ID (optional)'
            }),
            'credential_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Credential URL (optional)'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    technologies = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter technologies used (one per line)',
            'rows': 3
        }),
        required=False
    )

    class Meta:
       # model = Project
        fields = [
            'title', 'description', 'technologies', 'start_date',
            'end_date', 'is_current', 'url', 'order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Project description'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project URL (optional)'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Date validation
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')

        if start_date and end_date and not is_current:
            if end_date < start_date:
                raise ValidationError("End date cannot be earlier than start date")

        if is_current:
            cleaned_data['end_date'] = None

        # Convert technologies from text to list
        technologies_text = cleaned_data.get('technologies', '')
        if technologies_text:
            cleaned_data['technologies'] = [
                tech.strip()
                for tech in technologies_text.split('\n')
                if tech.strip()
            ]
        else:
            cleaned_data['technologies'] = []

        return cleaned_data

class SavedSectionForm(forms.ModelForm):
    class Meta:
#        model = SavedSection
        fields = ['title', 'content', 'section_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Section title'
            }),
            'section_type': forms.Select(attrs={'class': 'form-select'}),
        }



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'newsletter-input'
        })
    )