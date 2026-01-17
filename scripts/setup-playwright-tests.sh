#!/bin/bash
# Setup script for AI-powered testing tools

echo "🤖 Setting up AI-powered testing tools for AI Film Studio..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Install Playwright for E2E testing
echo -e "${BLUE}📦 Installing Playwright...${NC}"
pip install playwright pytest-playwright

echo -e "${BLUE}🌐 Installing browsers...${NC}"
playwright install chromium

# 2. Create E2E test directory
echo -e "${BLUE}📁 Creating E2E test structure...${NC}"
mkdir -p tests/e2e

# 3. Create sample E2E test
cat > tests/e2e/test_landing_page.py << 'EOF'
"""E2E tests for AI Film Studio landing page"""
import pytest
from playwright.sync_api import Page, expect

def test_landing_page_loads(page: Page):
    """Test that landing page loads successfully"""
    page.goto("http://localhost:3000")
    
    # Check title
    expect(page).to_have_title("AI Film Studio")
    
    # Check hero section
    expect(page.get_by_text("Transform Scripts into")).to_be_visible()

def test_navigation_menu(page: Page):
    """Test navigation menu functionality"""
    page.goto("http://localhost:3000")
    
    # Check all nav links are present
    expect(page.get_by_role("link", name="Features")).to_be_visible()
    expect(page.get_by_role("link", name="Pricing")).to_be_visible()
    expect(page.get_by_role("link", name="About")).to_be_visible()

def test_cta_buttons(page: Page):
    """Test call-to-action buttons"""
    page.goto("http://localhost:3000")
    
    # Check primary CTA
    get_started = page.get_by_role("button", name="Get Started")
    expect(get_started).to_be_visible()
    
    # Click and verify navigation
    get_started.click()
    expect(page).to_have_url(/.*signup/)

@pytest.mark.slow
def test_video_generation_flow(page: Page):
    """Test complete video generation flow"""
    page.goto("http://localhost:3000/dashboard")
    
    # Click create film
    page.get_by_role("button", name="Create Film").click()
    
    # Fill script
    page.get_by_placeholder("Enter your script").fill(
        "A young explorer discovers a hidden world beneath the ocean."
    )
    
    # Select duration
    page.get_by_label("Duration").select_option("30")
    
    # Submit
    page.get_by_role("button", name="Generate").click()
    
    # Wait for processing
    expect(page.get_by_text("Processing")).to_be_visible(timeout=5000)
EOF

# 4. Create Playwright config
cat > playwright.config.py << 'EOF'
"""Playwright configuration for AI Film Studio tests"""
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "test-results/videos/",
    }

@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Run before each test
    page.set_default_timeout(30000)  # 30 seconds
    yield
    # Cleanup after test
EOF

# 5. Create visual testing setup (optional)
echo -e "${BLUE}🎨 Setting up visual regression testing...${NC}"
cat > tests/e2e/test_visual_regression.py << 'EOF'
"""Visual regression tests using Playwright"""
import pytest
from playwright.sync_api import Page

def test_landing_page_screenshot(page: Page):
    """Capture and compare landing page screenshot"""
    page.goto("http://localhost:3000")
    page.screenshot(path="test-results/landing-page.png", full_page=True)
    
    # Playwright will compare with baseline on subsequent runs
    expect(page).to_have_screenshot("landing-page.png")

def test_dashboard_screenshot(page: Page):
    """Capture dashboard screenshot"""
    page.goto("http://localhost:3000/dashboard")
    expect(page).to_have_screenshot("dashboard.png")
EOF

# 6. Create conftest for E2E tests
cat > tests/e2e/conftest.py << 'EOF'
"""Pytest configuration for E2E tests"""
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "test-results/videos/",
        "record_har_path": "test-results/network.har",
    }
EOF

# 7. Update pytest.ini
echo -e "${BLUE}⚙️  Updating pytest configuration...${NC}"
if ! grep -q "e2e" pytest.ini; then
    cat >> pytest.ini << 'EOF'

# E2E test markers
e2e: End-to-end tests with Playwright
visual: Visual regression tests
EOF
fi

# 8. Create test run script
cat > scripts/run-e2e-tests.sh << 'EOF'
#!/bin/bash
# Run E2E tests with Playwright

echo "🚀 Starting Next.js dev server..."
cd frontend
npm run dev &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server..."
sleep 5

cd ..

echo "🧪 Running E2E tests..."
pytest tests/e2e/ --browser chromium --headed --video on

TEST_EXIT_CODE=$?

# Stop server
kill $SERVER_PID

exit $TEST_EXIT_CODE
EOF

chmod +x scripts/run-e2e-tests.sh

# 9. Install additional testing tools
echo -e "${BLUE}📦 Installing additional testing dependencies...${NC}"
pip install pytest-xdist pytest-html pytest-json-report

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Start your Next.js server: cd frontend && npm run dev"
echo "2. Run E2E tests: pytest tests/e2e/ --browser chromium"
echo "3. Record new tests: playwright codegen http://localhost:3000"
echo "4. View test results: open test-results/report.html"
echo ""
echo "🎥 Optional: Install Applitools for visual AI testing"
echo "   pip install eyes-playwright"
echo ""
echo "📖 See docs/AI_TESTING_TOOLS.md for more information"
