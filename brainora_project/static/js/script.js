// =====================================================
// Brainora - Learning Platform JavaScript
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add form validation feedback
    const forms = document.querySelectorAll('.auth-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Password strength indicator for signup
    const password1 = document.getElementById('id_password1');
    if (password1) {
        password1.addEventListener('input', function() {
            const strength = calculatePasswordStrength(this.value);
            updatePasswordStrengthUI(strength);
        });
    }
});

/**
 * Calculate password strength
 * @param {string} password - Password to check
 * @returns {string} - 'weak', 'medium', or 'strong'
 */
function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    
    if (strength <= 2) return 'weak';
    if (strength <= 3) return 'medium';
    return 'strong';
}

/**
 * Update password strength indicator UI
 * @param {string} strength - Password strength level
 */
function updatePasswordStrengthUI(strength) {
    const password1 = document.getElementById('id_password1');
    const existingIndicator = password1.parentElement.querySelector('.password-strength');
    
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    const indicator = document.createElement('div');
    indicator.className = 'password-strength mt-2';
    
    let color, text;
    switch(strength) {
        case 'weak':
            color = 'danger';
            text = 'Weak password';
            break;
        case 'medium':
            color = 'warning';
            text = 'Medium strength';
            break;
        case 'strong':
            color = 'success';
            text = 'Strong password';
            break;
    }
    
    indicator.innerHTML = `<small class="text-${color}"><i class="fas fa-shield-alt"></i> ${text}</small>`;
    password1.parentElement.appendChild(indicator);
}

/**
 * Toggle password visibility
 * @param {string} inputId - ID of password input
 */
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

/**
 * Disable submit button temporarily to prevent double submission
 */
function preventDoubleSubmit(formSelector) {
    const form = document.querySelector(formSelector);
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    }
}

// Initialize form submission prevention
preventDoubleSubmit('.auth-form');

// Console message
console.log('%cBrainora Learning Platform', 'font-size: 20px; font-weight: bold; color: #4f46e5;');
console.log('%cWelcome to your college learning hub!', 'font-size: 14px; color: #6b7280;');
