/**
 * E2E tests for DEPLOYED AI Film Studio frontend
 * Run against: https://ai-empower-hq-360.github.io/AI-Film-Studio
 *
 * Usage:
 *   npm run test:e2e:production
 *   PLAYWRIGHT_TEST_BASE_URL="https://..." npx playwright test e2e/production.spec.ts --config=playwright.config.production.ts
 */
import { test, expect } from '@playwright/test';

const BASE = process.env.PLAYWRIGHT_TEST_BASE_URL || 'https://ai-empower-hq-360.github.io/AI-Film-Studio';

test.describe('Deployed AI Film Studio – Home & Navigation', () => {
  test('home page loads', async ({ page }) => {
    await page.goto(BASE + '/');
    await expect(page).toHaveTitle(/AI Film Studio|Transform|Film/i);
    // Hero or main heading
    await expect(
      page.getByRole('heading', { level: 1 }).or(page.locator('h1'))
    ).toBeVisible({ timeout: 10000 });
  });

  test('home has nav and main content', async ({ page }) => {
    await page.goto(BASE + '/');
    // Nav: logo or links
    const nav = page.locator('nav').first();
    await expect(nav).toBeVisible({ timeout: 10000 });
    // At least one link
    const links = page.locator('nav a[href]');
    await expect(links.first()).toBeVisible({ timeout: 5000 });
  });

  test('Features link works', async ({ page }) => {
    await page.goto(BASE + '/');
    const features = page.getByRole('link', { name: /features/i }).first();
    if ((await features.count()) > 0) {
      await features.click();
      await expect(page).toHaveURL(/\/(#features|features)/i);
    }
  });

  test('Pricing link works', async ({ page }) => {
    await page.goto(BASE + '/');
    const pricing = page.getByRole('link', { name: /pricing/i }).first();
    if ((await pricing.count()) > 0) {
      await pricing.click();
      await expect(page).toHaveURL(/pricing/i);
    }
  });

  test('Dashboard link works', async ({ page }) => {
    await page.goto(BASE + '/');
    const dashboard = page.getByRole('link', { name: /dashboard/i }).first();
    if ((await dashboard.count()) > 0) {
      await dashboard.click();
      await expect(page).toHaveURL(/dashboard/i);
    }
  });

  test('Sign In link works', async ({ page }) => {
    await page.goto(BASE + '/');
    const signIn = page.getByRole('link', { name: /sign in/i }).first();
    if ((await signIn.count()) > 0) {
      await signIn.click();
      await expect(page).toHaveURL(/signin/i);
    }
  });

  test('Sign Up link works', async ({ page }) => {
    await page.goto(BASE + '/');
    const signUp = page.getByRole('link', { name: /sign up/i }).first();
    if ((await signUp.count()) > 0) {
      await signUp.click();
      await expect(page).toHaveURL(/signup/i);
    }
  });
});

test.describe('Deployed AI Film Studio – Dashboard', () => {
  test('dashboard page loads', async ({ page }) => {
    await page.goto(BASE + '/dashboard/');
    // Dashboard may redirect (e.g. signin) or show content
    const url = page.url();
    const isDashboard = /dashboard/i.test(url);
    const isSignIn = /signin/i.test(url);
    expect(isDashboard || isSignIn).toBeTruthy();
    if (isDashboard) {
      await expect(
        page.locator('main').or(page.locator('[role="main"]')).or(page.getByText(/dashboard|overview|projects/i))
      ).toBeVisible({ timeout: 10000 });
    }
  });

  test('dashboard has nav', async ({ page }) => {
    await page.goto(BASE + '/dashboard/');
    const nav = page.locator('nav').first();
    await expect(nav).toBeVisible({ timeout: 10000 });
  });
});

test.describe('Deployed AI Film Studio – Other Pages', () => {
  const pages: { path: string; name: string }[] = [
    { path: '/pricing', name: 'Pricing' },
    { path: '/about', name: 'About' },
    { path: '/features', name: 'Features' },
    { path: '/docs', name: 'Docs' },
    { path: '/contact', name: 'Contact' },
    { path: '/signin', name: 'Sign In' },
    { path: '/signup', name: 'Sign Up' },
    { path: '/privacy', name: 'Privacy' },
    { path: '/terms', name: 'Terms' },
  ];

  for (const { path, name } of pages) {
    test(`${name} (${path}) loads`, async ({ page }) => {
      const res = await page.goto(BASE + path, { waitUntil: 'domcontentloaded' });
      expect(res?.status()).toBeLessThan(500);
      await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
    });
  }
});

test.describe('Deployed AI Film Studio – Static Website (GitHub Pages)', () => {
  test('index.html loads', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
    await expect(
      page.getByText(/AI Film Studio|Transform|Film/i).first()
    ).toBeVisible({ timeout: 5000 });
  });

  test('features.html loads', async ({ page }) => {
    await page.goto(BASE + '/features.html');
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });

  test('docs.html loads', async ({ page }) => {
    await page.goto(BASE + '/docs.html');
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });

  test('about.html loads', async ({ page }) => {
    await page.goto(BASE + '/about.html');
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });
});
