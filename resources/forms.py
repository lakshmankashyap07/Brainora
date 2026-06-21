from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'category', 'description', 'file', 'external_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide details about the material, course references, etc.'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter resource title'}),
            'external_link': forms.URLInput(attrs={'placeholder': 'https://drive.google.com/...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        external_link = cleaned_data.get('external_link')

        if not file and not external_link:
            raise forms.ValidationError("You must supply either a resource file OR an external link.")
        return cleaned_data
