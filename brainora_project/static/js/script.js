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

    // =====================================================
    // Theme Toggle Functionality
    // =====================================================
    const themeToggle = document.getElementById('themeToggle');
    const themeText = document.getElementById('themeText');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const htmlElement = document.documentElement;
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update theme text
            if (themeText) {
                themeText.textContent = newTheme === 'dark' ? 'Theme (Dark)' : 'Theme (Light)';
            }
        });
    }
    
    // Set initial theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    if (themeText) {
        themeText.textContent = savedTheme === 'dark' ? 'Theme (Dark)' : 'Theme (Light)';
    }

    // =====================================================
    // Language Selection Functionality
    // =====================================================
    const languageItems = document.querySelectorAll('[data-language]');
    const currentLanguage = localStorage.getItem('language') || 'en';
    
    languageItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const selectedLanguage = this.getAttribute('data-language');
            localStorage.setItem('language', selectedLanguage);
            
            // Update checkmark position
            languageItems.forEach(li => {
                const icon = li.querySelector('i');
                if (icon && icon.classList.contains('fa-check')) {
                    icon.classList.remove('fa-check');
                    icon.classList.add('fa-check-circle');
                    icon.style.opacity = '0.3';
                }
            });
            
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-check-circle');
                icon.classList.add('fa-check');
                icon.style.opacity = '1';
            }
            
            // Display confirmation
            alert('Language changed to: ' + selectedLanguage.toUpperCase());
        });
    });
    
    // Initialize checkmark for current language
    languageItems.forEach(item => {
        const itemLang = item.getAttribute('data-language');
        const icon = item.querySelector('i');
        if (icon) {
            if (itemLang === currentLanguage) {
                icon.classList.add('fa-check');
            } else {
                icon.classList.add('fa-check-circle');
                icon.style.opacity = '0.3';
            }
        }
    });
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

// =====================================================
// Dark Mode Toggle
// =====================================================

const dayNightToggle = document.getElementById('dayNightToggle');
if (dayNightToggle) {
    // Check for saved dark mode preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        dayNightToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    dayNightToggle.addEventListener('click', function(e) {
        e.preventDefault();
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        
        // Update icon
        if (isDark) {
            dayNightToggle.innerHTML = '<i class="fas fa-sun"></i>';
            dayNightToggle.title = 'Toggle to Light Mode';
        } else {
            dayNightToggle.innerHTML = '<i class="fas fa-moon"></i>';
            dayNightToggle.title = 'Toggle to Dark Mode';
        }
    });
}

// =====================================================
// Focus Mode Toggle
// =====================================================

const focusModeToggle = document.getElementById('focusModeToggle');
if (focusModeToggle) {
    // Check for saved focus mode preference
    const isFocusMode = localStorage.getItem('focusMode') === 'true';
    if (isFocusMode) {
        document.body.classList.add('focus-mode');
    }

    focusModeToggle.addEventListener('click', function(e) {
        e.preventDefault();
        document.body.classList.toggle('focus-mode');
        const isFocus = document.body.classList.contains('focus-mode');
        localStorage.setItem('focusMode', isFocus);
        
        // Update icon
        if (isFocus) {
            focusModeToggle.innerHTML = '<i class="fas fa-eye"></i>';
            focusModeToggle.title = 'Exit Focus Mode';
        } else {
            focusModeToggle.innerHTML = '<i class="fas fa-eye-slash"></i>';
            focusModeToggle.title = 'Enter Focus Mode';
        }
    });
}

// =====================================================
// Focus Mode Exit Button
// =====================================================

// Create focus mode exit button
const focusExitBtn = document.createElement('button');
focusExitBtn.className = 'focus-mode-exit-btn';
focusExitBtn.innerHTML = '<i class="fas fa-times-circle me-2"></i>Exit Focus Mode';
focusExitBtn.title = 'Exit Focus Mode (Esc)';
document.body.appendChild(focusExitBtn);

focusExitBtn.addEventListener('click', function() {
    document.body.classList.remove('focus-mode');
    localStorage.setItem('focusMode', false);
    if (focusModeToggle) {
        focusModeToggle.innerHTML = '<i class="fas fa-eye-slash"></i>';
        focusModeToggle.title = 'Enter Focus Mode';
    }
});

// Keyboard shortcut to exit focus mode
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && document.body.classList.contains('focus-mode')) {
        document.body.classList.remove('focus-mode');
        localStorage.setItem('focusMode', false);
        if (focusModeToggle) {
            focusModeToggle.innerHTML = '<i class="fas fa-eye-slash"></i>';
            focusModeToggle.title = 'Enter Focus Mode';
        }
    }
});

// =====================================================
// Downloads Section Handler
// =====================================================

const downloadsBtn = document.getElementById('downloadsBtn');
if (downloadsBtn) {
    downloadsBtn.addEventListener('click', function(e) {
        // You can add functionality here to show a downloads modal or page
        // For now, it just scrolls to the downloads section if it exists
        const downloadsSection = document.getElementById('downloads-section');
        if (downloadsSection) {
            downloadsSection.scrollIntoView({ behavior: 'smooth' });
        }
    });
}


