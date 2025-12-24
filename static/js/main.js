// AI Film Studio - Main JavaScript

// API Base URL
const API_BASE_URL = window.location.origin;

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#6366f1'};
        color: white;
        border-radius: 0.5rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        
        if (!response.ok) {
            let errorMessage = 'Request failed';
            try {
                const error = await response.json();
                errorMessage = error.detail || errorMessage;
            } catch (e) {
                // Response is not JSON, use status text
                errorMessage = response.statusText || errorMessage;
            }
            throw new Error(errorMessage);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

// Authentication
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

function setAuthToken(token) {
    localStorage.setItem('auth_token', token);
}

function clearAuthToken() {
    localStorage.removeItem('auth_token');
}

function isAuthenticated() {
    return !!getAuthToken();
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Project Functions
async function createProject(projectData) {
    return await apiRequest('/api/v1/projects', {
        method: 'POST',
        body: JSON.stringify(projectData),
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

async function getProjects() {
    return await apiRequest('/api/v1/projects', {
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

async function getProject(projectId) {
    return await apiRequest(`/api/v1/projects/${projectId}`, {
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

async function getJob(jobId) {
    return await apiRequest(`/api/v1/jobs/${jobId}`, {
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

async function cancelJob(jobId) {
    return await apiRequest(`/api/v1/jobs/${jobId}/cancel`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

// User Functions
async function getUserCredits() {
    return await apiRequest('/api/v1/user/credits', {
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

async function getUserStats() {
    return await apiRequest('/api/v1/user/stats', {
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
        },
    });
}

// Format Helpers
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds}s`;
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
}

function formatCredits(credits) {
    return credits.toLocaleString();
}

// Status Helper
function getStatusBadgeClass(status) {
    const statusMap = {
        'queued': 'status-queued',
        'running': 'status-running',
        'completed': 'status-completed',
        'failed': 'status-failed',
    };
    return statusMap[status] || 'status-queued';
}

// Progress Polling
function pollJobProgress(jobId, callback, interval = 2000) {
    const poll = async () => {
        try {
            const job = await getJob(jobId);
            callback(job);
            
            if (job.status === 'completed' || job.status === 'failed') {
                return; // Stop polling
            }
            
            setTimeout(poll, interval);
        } catch (error) {
            console.error('Polling error:', error);
        }
    };
    
    poll();
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            input.style.borderColor = '#374151';
        }
    });
    
    return isValid;
}

// Navigation
function navigateTo(path) {
    window.location.href = path;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
