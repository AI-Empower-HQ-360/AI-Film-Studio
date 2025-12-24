// API base URL
const API_BASE_URL = window.location.origin;

// Fetch and display system data
async function fetchSystemData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/data/home`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching system data:', error);
        showError('Unable to load system data. Using default values.');
        // Use default values if API fails
        updateDashboard({
            stats: {
                total_projects: 0,
                completed_projects: 0,
                processing_projects: 0,
                api_status: 'online'
            },
            recent_activity: []
        });
    }
}

// Update dashboard with fetched data
function updateDashboard(data) {
    // Update stats
    document.getElementById('totalProjects').textContent = data.stats.total_projects;
    document.getElementById('completedProjects').textContent = data.stats.completed_projects;
    document.getElementById('processingProjects').textContent = data.stats.processing_projects;
    document.getElementById('apiStatus').textContent = data.stats.api_status;
    
    // Update recent activity
    displayRecentActivity(data.recent_activity);
}

// Display recent activity
function displayRecentActivity(activities) {
    const activityList = document.getElementById('activityList');
    
    if (activities.length === 0) {
        activityList.innerHTML = '<p class="loading">No recent activity to display</p>';
        return;
    }
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-description">${activity.description}</div>
            </div>
            <div class="activity-time">${formatTime(activity.timestamp)}</div>
        </div>
    `).join('');
}

// Format timestamp to relative time
function formatTime(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMs = now - time;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
}

// Show error message
function showError(message) {
    console.warn(message);
    // You could display a toast or notification here
}

// Fetch API version and update footer
async function fetchAPIVersion() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/health`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('apiVersion').textContent = data.version;
        }
    } catch (error) {
        console.error('Error fetching API version:', error);
    }
}

// Initialize dashboard
async function initDashboard() {
    await fetchAPIVersion();
    await fetchSystemData();
    
    // Refresh data every 30 seconds
    setInterval(fetchSystemData, 30000);
}

// Run when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
