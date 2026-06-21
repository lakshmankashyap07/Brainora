from django import forms
from .models import AcademicResource

class AcademicResourceForm(forms.ModelForm):
    class Meta:
        model = AcademicResource
        fields = [
            'title', 'description', 'resource_type', 'semester',
            'subject', 'department', 'course_code', 'file'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resource Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Resource Description'
            }),
            'resource_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject Name'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department (Optional)'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course Code (Optional)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.ppt,.pptx,.doc,.docx,.xls,.xlsx,.zip'
            }),
        }
