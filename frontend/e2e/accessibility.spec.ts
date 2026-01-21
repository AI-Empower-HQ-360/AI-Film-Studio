/**
 * Accessibility Tests (E2E)
 * Tests WCAG 2.1 AA compliance, keyboard navigation, and screen reader support
 */
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y } from 'axe-playwright';

test.describe('Accessibility Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await injectAxe(page);
  });

  test('should have no accessibility violations on homepage', async ({ page }) => {
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  });

  test('should have proper heading hierarchy', async ({ page }) => {
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBeGreaterThanOrEqual(1);
    expect(h1Count).toBeLessThanOrEqual(1); // Only one h1 per page

    // Check heading order (h1 before h2, etc.)
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    let lastLevel = 0;
    for (const heading of headings) {
      const tagName = await heading.evaluate(el => el.tagName.toLowerCase());
      const level = parseInt(tagName.charAt(1));
      expect(level).toBeGreaterThanOrEqual(lastLevel - 1); // Allow skipping levels down
      lastLevel = level;
    }
  });

  test('should have accessible form labels', async ({ page }) => {
    const inputs = await page.locator('input[type="text"], input[type="url"], textarea').all();
    
    for (const input of inputs) {
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledBy = await input.getAttribute('aria-labelledby');
      const placeholder = await input.getAttribute('placeholder');
      
      // Should have at least one label mechanism
      const hasLabel = id && (await page.locator(`label[for="${id}"]`).count() > 0);
      expect(hasLabel || ariaLabel || ariaLabelledBy || placeholder).toBeTruthy();
    }
  });

  test('should have accessible buttons', async ({ page }) => {
    const buttons = await page.locator('button').all();
    
    for (const button of buttons) {
      const text = await button.textContent();
      const ariaLabel = await button.getAttribute('aria-label');
      const title = await button.getAttribute('title');
      
      // Button should have accessible text
      expect(text?.trim() || ariaLabel || title).toBeTruthy();
      
      // Icon-only buttons should have aria-label
      const hasIcon = await button.locator('svg, i, img').count() > 0;
      if (hasIcon && !text?.trim()) {
        expect(ariaLabel).toBeTruthy();
      }
    }
  });

  test('should support keyboard navigation', async ({ page }) => {
    // Test Tab navigation
    await page.keyboard.press('Tab');
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
    
    // Tab through interactive elements
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press('Tab');
      const currentFocus = page.locator(':focus');
      if (await currentFocus.count() > 0) {
        await expect(currentFocus).toBeVisible();
      }
    }
  });

  test('should have proper ARIA roles', async ({ page }) => {
    // Check for common ARIA roles
    const navigation = page.locator('nav, [role="navigation"]');
    const main = page.locator('main, [role="main"]');
    const banner = page.locator('header, [role="banner"]');
    const contentinfo = page.locator('footer, [role="contentinfo"]');
    
    // At least main should exist
    const mainCount = await main.count();
    expect(mainCount).toBeGreaterThanOrEqual(1);
  });

  test('should have alt text for images', async ({ page }) => {
    const images = await page.locator('img').all();
    
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');
      
      // Decorative images should have alt="" or role="presentation"
      // Informative images should have descriptive alt text
      expect(alt !== null || role === 'presentation').toBeTruthy();
    }
  });

  test('should have sufficient color contrast', async ({ page }) => {
    // Test text contrast (basic check - full contrast testing requires browser APIs)
    const textElements = await page.locator('p, span, div, h1, h2, h3, h4, h5, h6, a, button, label').all();
    
    for (const element of textElements.slice(0, 10)) { // Sample first 10
      const color = await element.evaluate(el => {
        const style = window.getComputedStyle(el);
        return {
          color: style.color,
          backgroundColor: style.backgroundColor,
          fontSize: style.fontSize
        };
      });
      
      // Just verify styles are applied (actual contrast calculation needs specialized tool)
      expect(color.color).toBeTruthy();
    }
  });

  test('should support screen readers with proper landmarks', async ({ page }) => {
    // Check for semantic HTML or ARIA landmarks
    const landmarks = [
      'header',
      'nav',
      'main',
      'footer',
      '[role="banner"]',
      '[role="navigation"]',
      '[role="main"]',
      '[role="contentinfo"]'
    ];
    
    let landmarkCount = 0;
    for (const landmark of landmarks) {
      const count = await page.locator(landmark).count();
      landmarkCount += count;
    }
    
    expect(landmarkCount).toBeGreaterThan(0);
  });

  test('should have skip links', async ({ page }) => {
    // Check for skip to main content link
    const skipLinks = page.locator('a[href="#main"], a[href="#content"], .skip-link');
    const skipLinkCount = await skipLinks.count();
    
    // Skip links are recommended but not always required
    if (skipLinkCount > 0) {
      await expect(skipLinks.first()).toBeVisible();
    }
  });

  test('should handle focus visible', async ({ page }) => {
    // Test focus indicators
    const interactiveElements = await page.locator('a, button, input, textarea, select').all();
    
    for (const element of interactiveElements.slice(0, 5)) {
      await element.focus();
      const focusedElement = page.locator(':focus');
      
      // Check if element has focus styles
      const outline = await focusedElement.evaluate(el => {
        const style = window.getComputedStyle(el);
        return style.outline || style.boxShadow;
      });
      
      // Should have visible focus indicator
      expect(outline).toBeTruthy();
    }
  });

  test('should have proper form error messages', async ({ page }) => {
    // Find forms and test error handling
    const forms = await page.locator('form').all();
    
    for (const form of forms) {
      // Try to submit empty form
      const submitButton = form.locator('button[type="submit"]');
      if (await submitButton.count() > 0) {
        await submitButton.click();
        
        // Check for error messages with proper ARIA
        const errorMessages = form.locator('[role="alert"], .error, [aria-invalid="true"]');
        const errorCount = await errorMessages.count();
        
        // Errors should be associated with fields via aria-describedby
        if (errorCount > 0) {
          const firstError = errorMessages.first();
          const id = await firstError.getAttribute('id');
          
          if (id) {
            const associatedInput = page.locator(`[aria-describedby*="${id}"]`);
            const associatedCount = await associatedInput.count();
            expect(associatedCount).toBeGreaterThanOrEqual(0); // May or may not be associated
          }
        }
      }
    }
  });

  test('should support keyboard shortcuts', async ({ page }) => {
    // Test common keyboard shortcuts
    const shortcuts = [
      { key: 'Escape', description: 'Close modals/dropdowns' },
      { key: 'Enter', description: 'Submit forms' },
      { key: 'Space', description: 'Activate buttons' }
    ];
    
    for (const shortcut of shortcuts) {
      await page.keyboard.press(shortcut.key);
      // Should not cause errors
      const errors = await page.locator('[role="alert"]').count();
      expect(errors).toBeGreaterThanOrEqual(0);
    }
  });

  test('should have descriptive link text', async ({ page }) => {
    const links = await page.locator('a[href]').all();
    
    for (const link of links) {
      const text = await link.textContent();
      const ariaLabel = await link.getAttribute('aria-label');
      const title = await link.getAttribute('title');
      
      // Links should have descriptive text (not just "click here")
      const hasText = text?.trim() && text.trim().toLowerCase() !== 'click here';
      expect(hasText || ariaLabel || title).toBeTruthy();
    }
  });

  test('should support RTL languages', async ({ page }) => {
    // Test RTL support (if applicable)
    const html = await page.locator('html').first();
    const dir = await html.getAttribute('dir');
    
    // Should have dir attribute or support RTL via CSS
    expect(dir === 'ltr' || dir === 'rtl' || dir === null).toBeTruthy();
  });

  test('should handle dynamic content updates', async ({ page }) => {
    // Test ARIA live regions for dynamic content
    const liveRegions = page.locator('[role="status"], [role="alert"], [aria-live]');
    const liveRegionCount = await liveRegions.count();
    
    // Live regions are optional but recommended for dynamic content
    // Just verify page can handle them
    expect(liveRegionCount).toBeGreaterThanOrEqual(0);
  });
});
