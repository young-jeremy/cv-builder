from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Resume, PersonalInfo, Experience, Education,
    Skill, Project, Language, Certification, TemplateColor
)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-select'}),
        }


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Experience
        exclude = ['resume', 'order']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EducationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Education
        exclude = ['resume', 'order']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
        }


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Project
        exclude = ['resume', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
        }


class CertificationForm(forms.ModelForm):
    issue_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    expiration_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Certification
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'credential_id': forms.TextInput(attrs={'class': 'form-control'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TemplateColorForm(forms.ModelForm):
    class Meta:
        model = TemplateColor
        exclude = ['resume']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color_code': forms.TextInput(attrs={'class': 'form-control color-picker'}),
        }


class ResumeExportForm(forms.Form):
    EXPORT_CHOICES = (
        ('pdf', 'PDF'),
        ('docx', 'Word Document (DOCX)'),
        ('txt', 'Plain Text (TXT)'),
    )

    export_format = forms.ChoiceField(
        choices=EXPORT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

