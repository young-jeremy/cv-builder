from django import forms
from .models import UserDashboardSettings, JobApplication
from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import ResumeTemplate, JobApplication
from accounts.models import UserProfile


class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplate
        fields = '__all__'
        widgets = {
            'content': forms.HiddenInput(),  # Will be handled by React
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Resume'))


class JobApplicationForm(forms.ModelForm):
    applied_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = JobApplication
        fields = ['company', 'status', 'applied_date', 'notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['resume'].queryset = ResumeTemplate.objects.filter(user=user)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'phone', 'linkedin_url', 'github_url', 'website']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserDashboardSettings
        fields = ['theme', 'notification_enabled']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-select'}),
        }



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']