from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Resource


class LoginForm(AuthenticationForm):
    """Custom login form with improved styling"""
    username = forms.CharField(
        label='Username or Email',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )


class SignUpForm(UserCreationForm):
    """Custom signup form"""
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
        })
    )
    password_2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })
    )
    college_id = forms.CharField(
        label='College ID',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your college ID (optional)',
        })
    )

    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'college_id')


class ResourceUploadForm(forms.ModelForm):
    """Form for uploading resources and links"""
    class Meta:
        model = Resource
        fields = ('title', 'category', 'description', 'file', 'link')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional URL'}),
        }


class EditProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'profile_picture', 
                  'phone_contact', 'gender', 'location', 'date_of_birth', 'college_id', 'semester')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 4,
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'phone_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'type': 'tel',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City/Location',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'college_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'College ID',
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
