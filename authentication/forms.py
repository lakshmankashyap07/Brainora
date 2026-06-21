from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'role', 'college', 'semester', 'branch']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'college': forms.TextInput(attrs={'placeholder': 'College Name'}),
            'branch': forms.TextInput(attrs={'placeholder': 'Branch / Major'}),
            'semester': forms.NumberInput(attrs={'placeholder': 'Semester (1-8)', 'min': 1, 'max': 8}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control text-center fs-2 letter-spacing-lg',
        'placeholder': '••••••',
        'autocomplete': 'off',
        'autofocus': 'on'
    }))


class ForgotPasswordForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username or Email'}))


class ResetPasswordForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'placeholder': '6-digit OTP'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'full_name', 'profile_picture', 'bio', 
            'college', 'university', 'branch', 'semester', 
            'college_id', 'phone_contact', 'gender', 
            'location', 'date_of_birth', 'two_factor_enabled'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
