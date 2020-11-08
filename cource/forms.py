from django.contrib.auth.models import User
from django import forms
from .models import Organization, Cource, Topic, Schedule

form_style_class = 'form-control'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
       'class': form_style_class, 
    }))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={
       'class': form_style_class, 
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets =  {
            "username": forms.TextInput(attrs={
                'class': form_style_class,
            }),
            "first_name": forms.TextInput(attrs={
                'class': form_style_class,
            }),
            "email": forms.EmailInput(attrs={
                'class': form_style_class,
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
       'class': form_style_class, 
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       'class': form_style_class, 
    }))

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'web_site', 'document_series',
        'document_number', 'document_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': form_style_class,
            }),
            'email': forms.EmailInput(attrs={
                'class': form_style_class,
            }),
            'web_site': forms.TextInput(attrs={
                'class': form_style_class,
            }),
            'document_series': forms.TextInput(attrs={
                'class': form_style_class,
            }),
            'document_number': forms.NumberInput(attrs={
                'class': form_style_class,
            }),
            'document_type': forms.TextInput(attrs={
                'class': form_style_class,
            }),
        }

class CourceForm(forms.ModelForm):
    class Meta:
        model = Cource
        fields = ['title', 'description', 'type_of_cource', 'attendance',
        'start_date','end_date','study_hours','base_education','graduate_control',
        'graduate_document','price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': form_style_class,
            }),
            'description': forms.Textarea(attrs={
                'class': form_style_class,
            }),
            'type_of_cource': forms.Select(attrs={
                'class': form_style_class,
            }),
            'attendance': forms.Select(attrs={
                'class': form_style_class,
            }),
            'start_date': forms.DateInput(attrs={
                'class': form_style_class,
                'placeholder': 'dd.mm.yyyy',
            }),
            'end_date': forms.DateInput(attrs={
                'class': form_style_class,
                'placeholder': 'dd.mm.yyyy',
            }),
            'study_hours': forms.NumberInput(attrs={
                'class': form_style_class,
            }),
            'base_education': forms.Select(attrs={
                'class': form_style_class,
            }),
            'graduate_control': forms.Select(attrs={
                'class': form_style_class,
            }),
            'graduate_document': forms.Select(attrs={
                'class': form_style_class,
            }),
            'price': forms.NumberInput(attrs={
                'class': form_style_class,
            }),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'hours']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': form_style_class,
            }),
            'hours': forms.NumberInput(attrs={
                'class': form_style_class,
            }),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'from_time', 'to_time']
        widgets = {
            'day': forms.Select(attrs={
                'class': form_style_class,
            }),
            'from_time': forms.TimeInput(attrs={
                'class': form_style_class,
            }),
            'to_time': forms.TimeInput(attrs={
                'class': form_style_class,
            }),
        }






