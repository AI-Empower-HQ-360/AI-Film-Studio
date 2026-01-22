'use client';
import { useState } from 'react';
import Navigation from "@/app/components/Navigation";

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement form submission
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 5000);
  };

  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            Get in{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Touch
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Have questions, feedback, or need support? We'd love to hear from you.
          </p>
        </div>
      </section>

      {/* Contact Content */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700">
              <h2 className="text-2xl font-bold text-white mb-6">Send Us a Message</h2>
              
              {submitted && (
                <div className="mb-6 bg-green-900/30 border border-green-700 rounded-lg p-4">
                  <p className="text-green-300">✓ Message sent successfully! We'll get back to you soon.</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20"
                    placeholder="Your name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20"
                    placeholder="your@email.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Subject
                  </label>
                  <select
                    required
                    value={formData.subject}
                    onChange={(e) => setFormData({...formData, subject: e.target.value})}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20"
                  >
                    <option value="">Select a subject</option>
                    <option value="support">Technical Support</option>
                    <option value="billing">Billing Question</option>
                    <option value="feature">Feature Request</option>
                    <option value="partnership">Partnership Inquiry</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Message
                  </label>
                  <textarea
                    required
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    rows={6}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 resize-none"
                    placeholder="Tell us how we can help..."
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-6 py-4 rounded-lg font-semibold transition-all shadow-lg"
                >
                  Send Message
                </button>
              </form>
            </div>

            {/* Contact Information */}
            <div className="space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Other Ways to Reach Us</h2>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-sky-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">📧</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Email Support</h3>
                    <p className="text-slate-400 mb-2">For general inquiries and support</p>
                    <a href="mailto:support@aifilmstudio.com" className="text-sky-400 hover:text-sky-300">
                      support@aifilmstudio.com
                    </a>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">💼</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Business Inquiries</h3>
                    <p className="text-slate-400 mb-2">For partnerships and enterprise plans</p>
                    <a href="mailto:business@aifilmstudio.com" className="text-sky-400 hover:text-sky-300">
                      business@aifilmstudio.com
                    </a>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">📱</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Social Media</h3>
                    <p className="text-slate-400 mb-3">Connect with us on social platforms</p>
                    <div className="flex gap-4">
                      <a href="#" className="text-slate-400 hover:text-sky-400 transition-colors">Twitter</a>
                      <a href="#" className="text-slate-400 hover:text-purple-400 transition-colors">LinkedIn</a>
                      <a href="#" className="text-slate-400 hover:text-pink-400 transition-colors">Instagram</a>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">📖</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Documentation</h3>
                    <p className="text-slate-400 mb-2">Find answers in our knowledge base</p>
                    <a href="#" className="text-sky-400 hover:text-sky-300">
                      View Documentation →
                    </a>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-sky-900/30 to-purple-900/30 rounded-xl p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-2">Response Time</h3>
                <p className="text-slate-300 text-sm">
                  We typically respond to all inquiries within 24 hours during business days. 
                  For urgent technical issues, please include "URGENT" in your subject line.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-12">Frequently Asked Questions</h2>
          
          <div className="space-y-4">
            <details className="bg-slate-800/50 rounded-lg border border-slate-700 p-6 group">
              <summary className="font-semibold text-white cursor-pointer flex items-center justify-between">
                How long does it take to generate a video?
                <span className="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <p className="text-slate-400 mt-4">
                Most videos are generated in 30-90 seconds, depending on the length and complexity of your script.
              </p>
            </details>

            <details className="bg-slate-800/50 rounded-lg border border-slate-700 p-6 group">
              <summary className="font-semibold text-white cursor-pointer flex items-center justify-between">
                What video formats do you support?
                <span className="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <p className="text-slate-400 mt-4">
                We export videos in MP4 format with resolutions up to 4K, compatible with all major platforms.
              </p>
            </details>

            <details className="bg-slate-800/50 rounded-lg border border-slate-700 p-6 group">
              <summary className="font-semibold text-white cursor-pointer flex items-center justify-between">
                Can I use the videos commercially?
                <span className="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <p className="text-slate-400 mt-4">
                Yes! All content created with AI Film Studio is yours to use for commercial purposes under our license terms.
              </p>
            </details>
          </div>
        </div>
      </section>
    </div>
  );
}
