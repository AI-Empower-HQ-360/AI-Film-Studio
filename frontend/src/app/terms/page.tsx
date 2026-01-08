'use client';
import Link from 'next/link';
import Navigation from '../components/Navigation';

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8">
          <h1 className="text-3xl font-bold text-white mb-8">Terms of Service</h1>
          
          <div className="prose prose-invert max-w-none">
            <div className="text-slate-300 space-y-6">
              <div>
                <p className="text-slate-400 text-sm mb-8">Last updated: January 7, 2026</p>
              </div>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">1. Agreement to Terms</h2>
                <p>
                  By accessing and using AI Film Studio (&quot;the Service&quot;), you accept and agree to be bound by the terms and provision of this agreement. 
                  If you do not agree to abide by the above, please do not use this service.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">2. Description of Service</h2>
                <p>
                  AI Film Studio is an AI-powered platform that transforms text scripts into cinematic short films using cutting-edge AI image and video generation technology. 
                  The Service allows users to create, edit, and download AI-generated video content.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">3. User Accounts</h2>
                <p>
                  To access certain features of the Service, you must create an account. You are responsible for:
                </p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li>Providing accurate and complete information during registration</li>
                  <li>Maintaining the security of your password</li>
                  <li>All activities that occur under your account</li>
                  <li>Notifying us immediately of any unauthorized use of your account</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">4. Acceptable Use</h2>
                <p>You agree not to use the Service to:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li>Create content that is illegal, harmful, threatening, abusive, or offensive</li>
                  <li>Infringe upon intellectual property rights of others</li>
                  <li>Generate deepfakes or misleading content of real people without consent</li>
                  <li>Create content for spam, phishing, or fraudulent purposes</li>
                  <li>Attempt to reverse engineer, hack, or compromise the Service</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">5. Content Ownership and Rights</h2>
                <p>
                  <strong>Your Content:</strong> You retain ownership of the scripts, prompts, and reference materials you provide to the Service.
                </p>
                <p className="mt-2">
                  <strong>Generated Content:</strong> You own the AI-generated videos, images, and audio files created through the Service, 
                  subject to your compliance with these terms and applicable laws.
                </p>
                <p className="mt-2">
                  <strong>Commercial Use:</strong> Standard and Pro plan users may use generated content for commercial purposes. 
                  Free plan content includes watermarks and is limited to personal/educational use.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">6. Subscription and Payment</h2>
                <p>
                  <strong>Subscription Plans:</strong> We offer Free, Standard, and Pro subscription plans with different features and usage limits.
                </p>
                <p className="mt-2">
                  <strong>Billing:</strong> Paid subscriptions are billed monthly or annually in advance. All fees are non-refundable except as required by law.
                </p>
                <p className="mt-2">
                  <strong>Changes:</strong> We may change subscription prices with 30 days advance notice to existing subscribers.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">7. Privacy</h2>
                <p>
                  Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the Service, 
                  to understand our practices.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">8. Limitation of Liability</h2>
                <p>
                  AI Film Studio shall not be liable for any indirect, incidental, special, consequential, or punitive damages, 
                  including without limitation, loss of profits, data, use, goodwill, or other intangible losses.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">9. Service Availability</h2>
                <p>
                  We strive to maintain high service availability but do not guarantee uninterrupted access. 
                  The Service may be temporarily unavailable due to maintenance, updates, or unforeseen circumstances.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">10. Termination</h2>
                <p>
                  We may terminate or suspend your account and access to the Service immediately, without prior notice, 
                  for conduct that we believe violates these Terms of Service or is harmful to other users or the Service.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">11. Changes to Terms</h2>
                <p>
                  We reserve the right to modify these terms at any time. We will notify users of significant changes via email 
                  or through the Service. Continued use after changes constitutes acceptance of the new terms.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">12. Contact Information</h2>
                <p>
                  If you have questions about these Terms of Service, please contact us at:
                </p>
                <p className="mt-2">
                  Email: legal@aifilmstudio.com<br />
                  Address: [Your Company Address]
                </p>
              </section>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-slate-600 text-center">
            <Link href="/signup" className="text-sky-400 hover:text-sky-300 transition-colors">
              ← Back to Sign Up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}