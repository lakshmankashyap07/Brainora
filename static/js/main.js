// Brainora Core JavaScript Functionality

document.addEventListener('DOMContentLoaded', function () {
    // 1. Theme Configuration
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            let theme = document.documentElement.getAttribute('data-theme');
            let newTheme = theme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Re-render chart if it exists to adapt to new theme colors
            if (window.myDashboardChart) {
                renderDashboardChart(newTheme);
            }
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun text-warning';
        } else {
            icon.className = 'fas fa-moon text-primary';
        }
    }

    // 2. Mobile Sidebar Control
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
        if (sidebar && sidebar.classList.contains('show')) {
            if (!sidebar.contains(e.target) && !sidebarToggleBtn.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });

    // 3. Remove Loader
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(function () {
            loader.style.opacity = '0';
            setTimeout(function () {
                loader.style.display = 'none';
            }, 300);
        }, 400);
    }

    // 4. Auto-dismiss Django Messages
    const djangoAlerts = document.querySelectorAll('.django-alert');
    djangoAlerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

// Toast Notification Manager
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast custom-toast show mb-2 django-alert`;
    toast.setAttribute('role', 'alert');
    
    let iconClass = 'fa-info-circle text-info';
    if (type === 'success') iconClass = 'fa-check-circle text-success';
    if (type === 'warning') iconClass = 'fa-exclamation-triangle text-warning';
    if (type === 'danger') iconClass = 'fa-times-circle text-danger';

    toast.innerHTML = `
        <div class="toast-body d-flex align-items-center justify-content-between p-3">
            <div class="d-flex align-items-center gap-2">
                <i class="fas ${iconClass} fs-5"></i>
                <span class="fw-semibold">${message}</span>
            </div>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 4500);
}

// Chart.js Configuration
function initChart(canvasId, labels, dataValues) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    window.chartData = { labels, dataValues, canvasId };
    const currentTheme = localStorage.getItem('theme') || 'light';
    renderDashboardChart(currentTheme);
}

function renderDashboardChart(theme) {
    if (!window.chartData) return;
    const { canvasId, labels, dataValues } = window.chartData;
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (window.myDashboardChart) {
        window.myDashboardChart.destroy();
    }

    const gridColor = theme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)';
    const textColor = theme === 'dark' ? '#cbd5e1' : '#475569';

    window.myDashboardChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Uploads',
                data: dataValues,
                backgroundColor: 'rgba(99, 102, 241, 0.65)',
                borderColor: '#6366f1',
                borderWidth: 2,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: textColor }
                },
                y: {
                    grid: { color: gridColor },
                    ticks: { color: textColor, stepSize: 1 }
                }
            }
        }
    });
}
