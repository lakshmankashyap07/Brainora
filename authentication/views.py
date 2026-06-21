from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from datetime import timedelta

from .models import LoginHistory
from .forms import SignUpForm, LoginForm, OTPVerificationForm, ForgotPasswordForm, ResetPasswordForm, ProfileEditForm

User = get_user_model()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            
            # Generate OTP & Send email
            otp = user.generate_otp()
            send_mail(
                'Verify your Brainora Account',
                f'Hello {user.full_name or user.username},\n\nYour OTP for registration verification is: {otp}\nIt expires in 10 minutes.\n\nWarm regards,\nBrainora Team',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True
            )
            
            request.session['otp_user_id'] = user.id
            messages.success(request, "Account created successfully! Please verify your email using the OTP sent to you.")
            return redirect('authentication:verify_otp')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})

def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Session expired or invalid access. Please sign up or login again.")
        return redirect('authentication:signup')
        
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('authentication:signup')
        
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            if user.is_otp_valid(otp_code):
                user.is_verified = True
                user.clear_otp()
                user.save()
                
                # Autologin after verification
                auth_login(request, user, backend='authentication.backends.EmailOrUsernameBackend')
                
                # Record login history
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
                
                del request.session['otp_user_id']
                messages.success(request, "Your email has been verified. Welcome to Brainora!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Invalid or expired OTP code.")
    else:
        form = OTPVerificationForm()
    return render(request, 'authentication/otp_verification.html', {'form': form, 'user_email': user.email})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            # Find user for lockout check
            try:
                user = User.objects.get(Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email))
                if user.is_locked_out():
                    messages.error(request, f"Your account is locked due to too many failed login attempts. Please try again after {user.lockout_until.strftime('%H:%M:%S')}.")
                    return render(request, 'authentication/login.html', {'form': form})
            except User.DoesNotExist:
                user = None
                
            authenticated_user = authenticate(request, username=username_or_email, password=password)
            
            if authenticated_user is not None:
                # Security checks
                if not authenticated_user.is_active:
                    messages.error(request, "Your account is disabled.")
                    return render(request, 'authentication/login.html', {'form': form})
                    
                authenticated_user.reset_failed_attempts()
                
                # Check for 2FA requirement
                if authenticated_user.two_factor_enabled:
                    otp = authenticated_user.generate_otp()
                    send_mail(
                        'Brainora Two-Factor Authentication OTP',
                        f'Your 2FA verification OTP is: {otp}\nIt is valid for 10 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [authenticated_user.email],
                        fail_silently=True
                    )
                    request.session['pre_2fa_user_id'] = authenticated_user.id
                    request.session['remember_me'] = remember_me
                    messages.info(request, "A 2FA verification code has been sent to your email.")
                    return redirect('authentication:verify_2fa')
                
                # Standard login
                auth_login(request, authenticated_user, backend='authentication.backends.EmailOrUsernameBackend')
                
                # Remember me logic
                if remember_me:
                    request.session.set_expiry(1209600) # 2 weeks
                else:
                    request.session.set_expiry(0) # End of session
                    
                # Create login log
                LoginHistory.objects.create(
                    user=authenticated_user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
                
                # Redirect if not verified yet
                if not authenticated_user.is_verified:
                    request.session['otp_user_id'] = authenticated_user.id
                    messages.warning(request, "Please verify your email address to access all features.")
                    return redirect('authentication:verify_otp')
                    
                messages.success(request, f"Welcome back, {authenticated_user.full_name or authenticated_user.username}!")
                return redirect('dashboard:home')
            else:
                # Increment failed attempts on target user if user exists
                if user:
                    user.increment_failed_attempts()
                    if user.is_locked_out():
                        messages.error(request, "Account locked! You have exceeded maximum failed attempts. Try again in 15 minutes.")
                    else:
                        remaining = 5 - user.failed_login_attempts
                        messages.error(request, f"Invalid password. {remaining} attempt(s) remaining before lockout.")
                else:
                    messages.error(request, "Invalid username/email or password.")
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def verify_2fa_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        messages.error(request, "Invalid session. Please login again.")
        return redirect('authentication:login')
        
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('authentication:login')
        
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            if user.is_otp_valid(otp_code):
                user.clear_otp()
                auth_login(request, user, backend='authentication.backends.EmailOrUsernameBackend')
                
                # Set Session Expiry
                remember_me = request.session.get('remember_me', False)
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                    
                # Create history log
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
                
                # Cleanup session variables
                del request.session['pre_2fa_user_id']
                if 'remember_me' in request.session:
                    del request.session['remember_me']
                    
                messages.success(request, f"2FA verification successful. Welcome back, {user.full_name or user.username}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        form = OTPVerificationForm()
    return render(request, 'authentication/verify_2fa.html', {'form': form, 'user_email': user.email})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('authentication:login')

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['username_or_email']
            try:
                user = User.objects.get(Q(username__iexact=term) | Q(email__iexact=term))
                otp = user.generate_otp()
                send_mail(
                    'Brainora Password Reset OTP',
                    f'Your password reset OTP code is: {otp}\nIt is valid for 10 minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True
                )
                request.session['reset_user_id'] = user.id
                messages.success(request, "A password reset code has been sent to your email address.")
                return redirect('authentication:reset_password')
            except User.DoesNotExist:
                messages.error(request, "No account matches that username or email.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'authentication/forgot_password.html', {'form': form})

def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please initiate the request again.")
        return redirect('authentication:forgot_password')
        
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('authentication:forgot_password')
        
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            
            if user.is_otp_valid(otp_code):
                user.set_password(new_password)
                user.clear_otp()
                user.is_verified = True  # Verified since they verified their email link
                user.save()
                
                # Cleanup session
                del request.session['reset_user_id']
                messages.success(request, "Your password has been reset successfully. Please login with your new credentials.")
                return redirect('authentication:login')
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        form = ResetPasswordForm()
    return render(request, 'authentication/reset_password.html', {'form': form})

@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
        
    uploaded_resources = profile_user.uploaded_resources.all()[:6]
    bookmarked = profile_user.bookmarked_resources.all()[:6]
    
    context = {
        'profile_user': profile_user,
        'uploaded_resources': uploaded_resources,
        'bookmarked_resources': bookmarked,
    }
    return render(request, 'authentication/profile.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('authentication:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'authentication/edit_profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, "Your Brainora account has been permanently deleted.")
        return redirect('authentication:signup')
    return redirect('authentication:settings')

@login_required
def settings_view(request):
    login_logs = request.user.login_histories.all()[:10]
    return render(request, 'authentication/settings.html', {'login_logs': login_logs})
