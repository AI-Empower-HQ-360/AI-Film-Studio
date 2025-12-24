// AI Film Studio - Main JavaScript

// API Configuration
const API_BASE_URL = window.location.origin;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    checkApiHealth();
    addAnimations();
});

// Navigation
function initializeNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Check API Health
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('✅ API is healthy:', data);
            updateApiStatus('healthy');
        }
    } catch (error) {
        console.error('❌ API health check failed:', error);
        updateApiStatus('unhealthy');
    }
}

function updateApiStatus(status) {
    const statusIndicators = document.querySelectorAll('.api-status');
    statusIndicators.forEach(indicator => {
        indicator.textContent = status === 'healthy' ? '🟢 API Connected' : '🔴 API Disconnected';
        indicator.style.color = status === 'healthy' ? 'var(--success-color)' : 'var(--error-color)';
    });
}

// Animations
function addAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .stat-card, .project-item').forEach(el => {
        observer.observe(el);
    });
}

// Form Handlers
function handleScriptGeneration(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    showLoading('Generating script...');
    
    // Simulate API call
    setTimeout(() => {
        hideLoading();
        showNotification('Script generated successfully!', 'success');
        displayGeneratedScript(data);
    }, 2000);
}

function displayGeneratedScript(data) {
    const outputDiv = document.getElementById('script-output');
    if (outputDiv) {
        outputDiv.innerHTML = `
            <div class="card">
                <h3 class="card-title">Generated Script</h3>
                <p class="card-description">
                    Based on your prompt: "${data.prompt}"
                </p>
                <div class="mt-3">
                    <p><strong>Genre:</strong> ${data.genre}</p>
                    <p><strong>Duration:</strong> ${data.duration} minutes</p>
                </div>
            </div>
        `;
    }
}

// Scene Management
function createNewScene() {
    showNotification('Creating new scene...', 'info');
    
    setTimeout(() => {
        const scenesList = document.getElementById('scenes-list');
        if (scenesList) {
            const sceneCount = scenesList.children.length + 1;
            const newScene = createSceneElement(sceneCount);
            scenesList.appendChild(newScene);
            showNotification(`Scene ${sceneCount} created!`, 'success');
        }
    }, 500);
}

function createSceneElement(number) {
    const scene = document.createElement('div');
    scene.className = 'card fade-in';
    scene.innerHTML = `
        <div class="flex items-center justify-between mb-2">
            <h3 class="card-title">Scene ${number}</h3>
            <span class="badge badge-info">Draft</span>
        </div>
        <p class="card-description">Scene description goes here. Edit to customize.</p>
        <div class="mt-3 flex gap-2">
            <button class="btn btn-secondary" onclick="editScene(${number})">Edit</button>
            <button class="btn btn-secondary" onclick="deleteScene(${number})">Delete</button>
        </div>
    `;
    return scene;
}

function editScene(number) {
    showNotification(`Editing Scene ${number}`, 'info');
}

function deleteScene(number) {
    if (confirm(`Are you sure you want to delete Scene ${number}?`)) {
        showNotification(`Scene ${number} deleted`, 'warning');
    }
}

// Video Rendering
function startRender() {
    showLoading('Rendering video...');
    
    const progressBar = document.getElementById('render-progress');
    if (progressBar) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            progressBar.style.width = `${progress}%`;
            
            if (progress >= 100) {
                clearInterval(interval);
                hideLoading();
                showNotification('Video rendered successfully!', 'success');
            }
        }, 300);
    }
}

// Project Management
function createNewProject() {
    const projectName = prompt('Enter project name:');
    if (projectName) {
        showNotification(`Creating project "${projectName}"...`, 'info');
        
        setTimeout(() => {
            addProjectToList(projectName);
            showNotification(`Project "${projectName}" created!`, 'success');
        }, 1000);
    }
}

function addProjectToList(projectName) {
    const projectsList = document.getElementById('projects-list');
    if (projectsList) {
        const project = document.createElement('div');
        project.className = 'project-item fade-in';
        project.innerHTML = `
            <div class="project-info">
                <h3>${projectName}</h3>
                <div class="project-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>⏱️ Just now</span>
                </div>
            </div>
            <div class="flex gap-2">
                <span class="badge badge-info">In Progress</span>
                <button class="btn btn-primary" onclick="openProject('${projectName}')">Open</button>
            </div>
        `;
        projectsList.insertBefore(project, projectsList.firstChild);
    }
}

function openProject(projectName) {
    showNotification(`Opening project "${projectName}"...`, 'info');
    setTimeout(() => {
        window.location.href = '/dashboard.html';
    }, 500);
}

// Utility Functions
function showLoading(message = 'Loading...') {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-overlay';
    loadingDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.9);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    loadingDiv.innerHTML = `
        <div class="spinner"></div>
        <p style="margin-top: 1rem; color: var(--text-secondary);">${message}</p>
    `;
    document.body.appendChild(loadingDiv);
}

function hideLoading() {
    const loadingDiv = document.getElementById('loading-overlay');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: rgba(30, 41, 59, 0.95);
        border-radius: var(--radius-md);
        border-left: 4px solid ${getNotificationColor(type)};
        color: var(--text-primary);
        box-shadow: var(--shadow-xl);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationColor(type) {
    const colors = {
        success: 'var(--success-color)',
        error: 'var(--error-color)',
        warning: 'var(--warning-color)',
        info: 'var(--primary-color)'
    };
    return colors[type] || colors.info;
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
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
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export functions for inline use
window.handleScriptGeneration = handleScriptGeneration;
window.createNewScene = createNewScene;
window.editScene = editScene;
window.deleteScene = deleteScene;
window.startRender = startRender;
window.createNewProject = createNewProject;
window.openProject = openProject;
