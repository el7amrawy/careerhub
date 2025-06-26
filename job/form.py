from django import forms
from .models import Apply, Job, Category, Skill
from django.utils.translation import gettext_lazy as _




class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['name', 'email', 'website', 'cv', 'cover_letter']



class JobForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'skills-input',
            'multiple': 'multiple',
            'data-placeholder': 'Search skills...'
        }),
        required=False,
        help_text="Search and select required skills"
    )
    
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'company_description', 'location',
            'job_type', 'job_level', 'category', 'description',
            'requirements', 'responsibilities', 'vacancy', 'salary',
            'experience_min', 'experience_max', 'image', 'is_featured',
            'is_active', 'skills'
        ]
        exclude = ('owner', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Company Description', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Location'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'job_level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Requirements', 'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Responsibilities', 'rows': 5}),
            'vacancy': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Vacancies'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary Amount'}),
            'experience_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Experience (years)'}),
            'experience_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Experience (years)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }