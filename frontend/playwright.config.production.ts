import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright config for testing DEPLOYED AI Film Studio frontend
 * Use: PLAYWRIGHT_TEST_BASE_URL="https://ai-empower-hq-360.github.io/AI-Film-Studio" npx playwright test --config=playwright.config.production.ts
 * Or: npm run test:e2e:production
 */
const BASE_URL =
  process.env.PLAYWRIGHT_TEST_BASE_URL ||
  'https://ai-empower-hq-360.github.io/AI-Film-Studio';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report-production' }],
    ['list'],
  ],
  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    // Firefox/WebKit: run `npx playwright install` then add:
    // { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    // { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  // No local webServer – we test the deployed site
  // webServer: undefined
});
