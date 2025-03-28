from django import forms
from django.forms import ModelForm
from .models import (
    Resume, Education, Experience, Skill, Project,
    Certification, Language, Reference, CustomSection, CoverLetter
)

class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'full_name', 'email', 'phone', 'location',
            'headline', 'summary', 'profile_photo',
            'primary_color', 'secondary_color', 'font_family',
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'font_family': forms.Select(choices=[
                ('Arial, sans-serif', 'Arial'),
                ('Helvetica, sans-serif', 'Helvetica'),
                ('Georgia, serif', 'Georgia'),
                ('Times New Roman, serif', 'Times New Roman'),
                ('Courier New, monospace', 'Courier New'),
                ('Verdana, sans-serif', 'Verdana'),
                ('Roboto, sans-serif', 'Roboto'),
                ('Open Sans, sans-serif', 'Open Sans'),
                ('Lato, sans-serif', 'Lato'),
                ('Montserrat, sans-serif', 'Montserrat'),
            ]),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            'institution', 'degree', 'field_of_study', 'location',
            'start_date', 'end_date', 'current', 'description', 'gpa'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'company', 'title', 'location',
            'start_date', 'end_date', 'current', 'description'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'url',
            'start_date', 'end_date', 'current'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = [
            'name', 'issuing_organization', 'issue_date',
            'expiration_date', 'credential_id', 'credential_url'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency']


class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = [
            'name', 'company', 'title', 'email', 'phone', 'reference_text'
        ]
        widgets = {
            'reference_text': forms.Textarea(attrs={'rows': 3}),
        }


class CustomSectionForm(ModelForm):
    class Meta:
        model = CustomSection
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class CoverLetterForm(ModelForm):
    class Meta:
        model = CoverLetter
        fields = [
            'title', 'resume', 'recipient_name', 'recipient_company',
            'recipient_address', 'greeting', 'body', 'closing'
        ]
        widgets = {
            'recipient_address': forms.Textarea(attrs={'rows': 2}),
            'body': forms.Textarea(attrs={'rows': 10}),
        }


