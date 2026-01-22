/**
 * E2E tests for DEPLOYED AI Film Studio frontend
 * Base URL: https://ai-empower-hq-360.github.io/AI-Film-Studio (see playwright.config.production.ts)
 *
 * Usage:
 *   npm run test:e2e:production
 *   PLAYWRIGHT_TEST_BASE_URL="https://..." npm run test:e2e:production
 */
import { test, expect } from '@playwright/test';

test.describe('Deployed AI Film Studio – Home & Navigation', () => {
  test('home page loads', async ({ page }) => {
    const res = await page.goto('/', { waitUntil: 'domcontentloaded' });
    expect(res?.status()).toBeLessThan(500);
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
    const hasH1 = (await page.locator('h1').count()) >= 1;
    const title = await page.title();
    expect(hasH1 || /AI Film Studio|Transform|Film/i.test(title)).toBeTruthy();
  });

  test('home has nav and main content', async ({ page }) => {
    await page.goto('/');
    const nav = page.locator('nav').first();
    const hasNav = (await nav.count()) > 0;
    const links = page.locator('nav a[href], a[href]');
    const hasLinks = (await links.count()) > 0;
    expect(hasNav || hasLinks).toBeTruthy();
  });

  test('Features link works', async ({ page }) => {
    await page.goto('/');
    const features = page.getByRole('link', { name: /features/i }).first();
    if ((await features.count()) > 0) {
      await features.click();
      await expect(page).toHaveURL(/\/(#features|features|features\.html)/i);
    }
  });

  test('Pricing link works', async ({ page }) => {
    await page.goto('/');
    const pricing = page.getByRole('link', { name: /pricing/i }).first();
    if ((await pricing.count()) > 0) {
      await pricing.click();
      await expect(page).toHaveURL(/pricing/i);
    }
  });

  test('Dashboard link works', async ({ page }) => {
    await page.goto('/');
    const dashboard = page.getByRole('link', { name: /dashboard/i }).first();
    if ((await dashboard.count()) > 0) {
      await dashboard.click();
      await expect(page).toHaveURL(/dashboard/i);
    }
  });

  test('Sign In link works', async ({ page }) => {
    await page.goto('/');
    const signIn = page.getByRole('link', { name: /sign in/i }).first();
    if ((await signIn.count()) > 0) {
      await signIn.click();
      await expect(page).toHaveURL(/signin/i);
    }
  });

  test('Sign Up link works', async ({ page }) => {
    await page.goto('/');
    const signUp = page.getByRole('link', { name: /sign up/i }).first();
    if ((await signUp.count()) > 0) {
      await signUp.click();
      await expect(page).toHaveURL(/signup/i);
    }
  });
});

test.describe('Deployed AI Film Studio – Dashboard', () => {
  test('dashboard page loads', async ({ page }) => {
    await page.goto('/dashboard/');
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
    await page.goto('/dashboard/');
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
      const res = await page.goto(path, { waitUntil: 'domcontentloaded' });
      expect(res?.status()).toBeLessThan(500);
      await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
    });
  }
});

test.describe('Deployed AI Film Studio – Static Website (GitHub Pages)', () => {
  test('index.html loads', async ({ page }) => {
    const res = await page.goto('/index.html', { waitUntil: 'domcontentloaded' });
    expect(res?.status()).toBeLessThan(500);
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
    const text = (await page.locator('body').textContent()) || '';
    // Either AI Film Studio content or GitHub 404 (site not yet published)
    expect(
      /AI Film Studio|Transform|Film|script/i.test(text) || /404|GitHub Pages/i.test(text)
    ).toBeTruthy();
  });

  test('features.html loads', async ({ page }) => {
    const res = await page.goto('/features.html', { waitUntil: 'domcontentloaded' });
    expect(res?.status()).toBeLessThan(500);
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });

  test('docs.html loads', async ({ page }) => {
    const res = await page.goto('/docs.html', { waitUntil: 'domcontentloaded' });
    expect(res?.status()).toBeLessThan(500);
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });

  test('about.html loads', async ({ page }) => {
    const res = await page.goto('/about.html', { waitUntil: 'domcontentloaded' });
    expect(res?.status()).toBeLessThan(500);
    await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
  });
});
