'use client';
import Link from 'next/link';
import Navigation from '../components/Navigation';

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8">
          <h1 className="text-3xl font-bold text-white mb-8">Privacy Policy</h1>
          
          <div className="prose prose-invert max-w-none">
            <div className="text-slate-300 space-y-6">
              <div>
                <p className="text-slate-400 text-sm mb-8">Last updated: January 7, 2026</p>
              </div>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">1. Information We Collect</h2>
                
                <div className="mt-4">
                  <h3 className="text-lg font-medium text-white mb-2">Account Information</h3>
                  <p>When you create an account, we collect:</p>
                  <ul className="list-disc ml-6 mt-2 space-y-1">
                    <li>Name and email address</li>
                    <li>Authentication details (encrypted passwords)</li>
                    <li>Profile information and preferences</li>
                  </ul>
                </div>

                <div className="mt-4">
                  <h3 className="text-lg font-medium text-white mb-2">Content and Usage Data</h3>
                  <p>We collect and process:</p>
                  <ul className="list-disc ml-6 mt-2 space-y-1">
                    <li>Scripts, prompts, and text inputs you provide</li>
                    <li>Reference images and media you upload</li>
                    <li>Generated content (videos, images, audio)</li>
                    <li>Usage statistics (generation count, processing time)</li>
                    <li>Technical performance data (GPU usage, job duration)</li>
                  </ul>
                </div>

                <div className="mt-4">
                  <h3 className="text-lg font-medium text-white mb-2">Payment Information</h3>
                  <p>
                    Payment processing is handled by third-party providers (Stripe, PayPal). We store only:
                  </p>
                  <ul className="list-disc ml-6 mt-2 space-y-1">
                    <li>Subscription status and plan information</li>
                    <li>Payment method metadata (last 4 digits, expiration)</li>
                    <li>Transaction history and invoices</li>
                  </ul>
                </div>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">2. How We Use Your Information</h2>
                <p>We use your information to:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li>Provide and maintain the AI Film Studio service</li>
                  <li>Process your content generation requests</li>
                  <li>Manage your account and subscription</li>
                  <li>Improve our AI models and service quality</li>
                  <li>Send service updates and important notifications</li>
                  <li>Provide customer support</li>
                  <li>Prevent fraud and ensure service security</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">3. Information Sharing</h2>
                <p>We do not sell your personal information. We may share information with:</p>
                
                <div className="mt-4">
                  <h3 className="text-lg font-medium text-white mb-2">Service Providers</h3>
                  <ul className="list-disc ml-6 space-y-1">
                    <li>Cloud infrastructure providers (AWS, Google Cloud)</li>
                    <li>Payment processors (Stripe, PayPal)</li>
                    <li>Analytics and monitoring services</li>
                    <li>Customer support platforms</li>
                  </ul>
                </div>

                <div className="mt-4">
                  <h3 className="text-lg font-medium text-white mb-2">Legal Requirements</h3>
                  <p>We may disclose information when required by law or to:</p>
                  <ul className="list-disc ml-6 mt-2 space-y-1">
                    <li>Comply with legal obligations</li>
                    <li>Protect our rights and property</li>
                    <li>Prevent fraud or abuse</li>
                    <li>Ensure user safety</li>
                  </ul>
                </div>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">4. Data Security</h2>
                <p>We implement industry-standard security measures:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li>Encryption in transit and at rest</li>
                  <li>Regular security audits and monitoring</li>
                  <li>Access controls and authentication</li>
                  <li>Secure data centers and infrastructure</li>
                  <li>Employee security training and protocols</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">5. Data Retention</h2>
                <p>We retain your data as follows:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li><strong>Account Information:</strong> Until account deletion + 30 days</li>
                  <li><strong>Generated Content:</strong> As long as your account is active</li>
                  <li><strong>Usage Data:</strong> Up to 2 years for analytics and improvements</li>
                  <li><strong>Payment Records:</strong> 7 years for tax and legal compliance</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">6. Your Rights</h2>
                <p>You have the right to:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li><strong>Access:</strong> Request a copy of your personal data</li>
                  <li><strong>Rectification:</strong> Correct inaccurate personal information</li>
                  <li><strong>Erasure:</strong> Request deletion of your personal data</li>
                  <li><strong>Portability:</strong> Export your data in a structured format</li>
                  <li><strong>Restriction:</strong> Limit processing of your data</li>
                  <li><strong>Objection:</strong> Opt-out of certain data processing</li>
                </ul>
                <p className="mt-2">
                  To exercise these rights, contact us at privacy@aifilmstudio.com
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">7. Cookies and Tracking</h2>
                <p>We use cookies and similar technologies for:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li>Authentication and session management</li>
                  <li>Preference storage and personalization</li>
                  <li>Analytics and performance monitoring</li>
                  <li>Security and fraud prevention</li>
                </ul>
                <p className="mt-2">
                  You can control cookies through your browser settings.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">8. Third-Party Services</h2>
                <p>Our service integrates with:</p>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  <li><strong>Google OAuth:</strong> For authentication (governed by Google's Privacy Policy)</li>
                  <li><strong>AI Model Providers:</strong> For content generation processing</li>
                  <li><strong>CDN Services:</strong> For content delivery and performance</li>
                </ul>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">9. International Data Transfers</h2>
                <p>
                  Your data may be processed in countries other than your country of residence. 
                  We ensure appropriate safeguards are in place for international data transfers, 
                  including standard contractual clauses and adequacy decisions.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">10. Children's Privacy</h2>
                <p>
                  AI Film Studio is not intended for children under 13 years of age. We do not knowingly collect 
                  personal information from children under 13. If you believe we have collected information from 
                  a child under 13, please contact us immediately.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">11. Changes to Privacy Policy</h2>
                <p>
                  We may update this Privacy Policy from time to time. We will notify you of any material changes 
                  by posting the new Privacy Policy on this page and updating the "Last updated" date. 
                  We encourage you to review this Privacy Policy periodically.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold text-white mb-4">12. Contact Us</h2>
                <p>
                  If you have questions about this Privacy Policy or our data practices, please contact us:
                </p>
                <div className="mt-2">
                  <p>Email: privacy@aifilmstudio.com</p>
                  <p>Data Protection Officer: dpo@aifilmstudio.com</p>
                  <p>Address: [Your Company Address]</p>
                </div>
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