import Navigation from "@/app/components/Navigation";
import Link from "next/link";

export default function About() {
  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            About{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              AI Film Studio
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            We're on a mission to democratize film production by making professional-quality 
            video creation accessible to everyone through AI technology.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-white mb-6">Our Mission</h2>
              <p className="text-slate-300 mb-4">
                AI Film Studio was founded with a simple belief: everyone has a story to tell, 
                and technology should make storytelling easier, not harder.
              </p>
              <p className="text-slate-300 mb-4">
                We combine cutting-edge AI models with intuitive design to transform text scripts 
                into cinematic short films in minutes. What once required expensive equipment, 
                large teams, and weeks of production can now be done from your browser.
              </p>
              <p className="text-slate-300">
                Our platform serves content creators, businesses, educators, and filmmakers 
                worldwide, enabling them to bring their creative visions to life at a fraction 
                of traditional costs.
              </p>
            </div>
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700">
              <div className="grid grid-cols-2 gap-6 text-center">
                <div>
                  <div className="text-4xl font-bold text-sky-400 mb-2">2025</div>
                  <p className="text-slate-400">Founded</p>
                </div>
                <div>
                  <div className="text-4xl font-bold text-purple-400 mb-2">10K+</div>
                  <p className="text-slate-400">Users</p>
                </div>
                <div>
                  <div className="text-4xl font-bold text-pink-400 mb-2">50K+</div>
                  <p className="text-slate-400">Films Created</p>
                </div>
                <div>
                  <div className="text-4xl font-bold text-green-400 mb-2">150+</div>
                  <p className="text-slate-400">Countries</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-16">Our Values</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-xl font-semibold text-white mb-3">Innovation First</h3>
              <p className="text-slate-400">
                We push the boundaries of what's possible with AI, constantly exploring 
                new models and techniques to improve quality and speed.
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-white mb-3">User-Centric</h3>
              <p className="text-slate-400">
                Every feature we build starts with understanding our users' needs. 
                Your feedback directly shapes our product roadmap.
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">🌍</div>
              <h3 className="text-xl font-semibold text-white mb-3">Accessibility</h3>
              <p className="text-slate-400">
                We believe powerful creative tools should be accessible to everyone, 
                regardless of technical expertise or budget.
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold text-white mb-3">Privacy & Security</h3>
              <p className="text-slate-400">
                Your creative work is yours. We use enterprise-grade security and 
                never share your content without permission.
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold text-white mb-3">Performance</h3>
              <p className="text-slate-400">
                Speed matters. We optimize every aspect of our platform to deliver 
                results in minutes, not hours.
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-8 border border-slate-700">
              <div className="text-4xl mb-4">🤝</div>
              <h3 className="text-xl font-semibold text-white mb-3">Community</h3>
              <p className="text-slate-400">
                We're building more than a product—we're fostering a community of 
                creators who inspire and learn from each other.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-4">Built by AI-Empower-HQ-360</h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            A team of AI engineers, filmmakers, and product designers passionate about 
            the intersection of creativity and technology.
          </p>

          <div className="bg-gradient-to-br from-sky-900/30 to-purple-900/30 rounded-2xl p-12 border border-slate-700 text-center">
            <h3 className="text-2xl font-bold text-white mb-4">Join Our Team</h3>
            <p className="text-slate-300 mb-6 max-w-2xl mx-auto">
              We're always looking for talented individuals who are passionate about AI, 
              filmmaking, and building products that matter.
            </p>
            <Link 
              href="/careers" 
              className="inline-block bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all shadow-lg"
            >
              View Open Positions
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
          <p className="text-slate-300 mb-8">
            Join thousands of creators transforming their scripts into films.
          </p>
          <Link 
            href="/signup" 
            className="inline-block bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all shadow-lg"
          >
            Start Creating Free
          </Link>
        </div>
      </section>
    </div>
  );
}
