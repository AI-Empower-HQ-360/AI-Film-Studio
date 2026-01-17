import Navigation from "@/app/components/Navigation";
import Link from "next/link";

export default function Careers() {
  const openings = [
    {
      title: "Senior AI/ML Engineer",
      department: "Engineering",
      location: "Remote / San Francisco",
      type: "Full-time",
      description: "Build and optimize AI models for video generation and processing."
    },
    {
      title: "Full Stack Engineer",
      department: "Engineering",
      location: "Remote",
      type: "Full-time",
      description: "Develop scalable web applications using Next.js, React, and FastAPI."
    },
    {
      title: "DevOps Engineer",
      department: "Infrastructure",
      location: "Remote",
      type: "Full-time",
      description: "Manage AWS infrastructure, Kubernetes clusters, and CI/CD pipelines."
    },
    {
      title: "Product Designer",
      department: "Design",
      location: "Remote / New York",
      type: "Full-time",
      description: "Create intuitive user experiences for our AI-powered platform."
    },
    {
      title: "Content Marketing Manager",
      department: "Marketing",
      location: "Remote",
      type: "Full-time",
      description: "Develop content strategy and create engaging materials for our community."
    },
    {
      title: "Customer Success Manager",
      department: "Customer Success",
      location: "Remote",
      type: "Full-time",
      description: "Help our users succeed and drive product adoption."
    }
  ];

  const benefits = [
    {
      icon: "💰",
      title: "Competitive Salary",
      description: "Industry-leading compensation with equity options"
    },
    {
      icon: "🏥",
      title: "Health & Wellness",
      description: "Comprehensive health, dental, and vision coverage"
    },
    {
      icon: "🌴",
      title: "Unlimited PTO",
      description: "Take time off when you need it, no questions asked"
    },
    {
      icon: "🏠",
      title: "Remote-First",
      description: "Work from anywhere with flexible hours"
    },
    {
      icon: "📚",
      title: "Learning Budget",
      description: "$2,000 annual budget for courses and conferences"
    },
    {
      icon: "💻",
      title: "Latest Equipment",
      description: "Top-of-the-line laptop and equipment of your choice"
    },
    {
      icon: "🚀",
      title: "Stock Options",
      description: "Early employee equity in a fast-growing startup"
    },
    {
      icon: "👥",
      title: "Great Team",
      description: "Work with talented, passionate, and friendly people"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            Join Our{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Mission
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-8">
            Help us democratize film production and empower creators worldwide with AI technology.
          </p>
          <div className="flex items-center justify-center gap-4 text-slate-400">
            <span>🌍 Remote-first</span>
            <span>•</span>
            <span>⚡ Fast-growing</span>
            <span>•</span>
            <span>🚀 Impact-driven</span>
          </div>
        </div>
      </section>

      {/* Why Join Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-16">Why Join AI Film Studio?</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-sky-500/20 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
                🎯
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Meaningful Work</h3>
              <p className="text-slate-400">
                Build products that empower millions of creators to bring their stories to life.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
                🧠
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Cutting-Edge Tech</h3>
              <p className="text-slate-400">
                Work with the latest AI models, cloud infrastructure, and development tools.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500/20 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
                📈
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Rapid Growth</h3>
              <p className="text-slate-400">
                Join a fast-growing startup with massive market opportunity and venture backing.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-4">Benefits & Perks</h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            We take care of our team so they can focus on building amazing products.
          </p>

          <div className="grid md:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => (
              <div key={index} className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="text-3xl mb-3">{benefit.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{benefit.title}</h3>
                <p className="text-sm text-slate-400">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Open Positions Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-4">Open Positions</h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            We're hiring talented individuals across all departments.
          </p>

          <div className="space-y-4">
            {openings.map((job, index) => (
              <div key={index} className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-sky-500/50 transition-all">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-white mb-2">{job.title}</h3>
                    <p className="text-slate-400 mb-3">{job.description}</p>
                    <div className="flex flex-wrap gap-3 text-sm">
                      <span className="px-3 py-1 bg-slate-700 rounded-full text-slate-300">
                        {job.department}
                      </span>
                      <span className="px-3 py-1 bg-slate-700 rounded-full text-slate-300">
                        📍 {job.location}
                      </span>
                      <span className="px-3 py-1 bg-slate-700 rounded-full text-slate-300">
                        ⏰ {job.type}
                      </span>
                    </div>
                  </div>
                  <Link 
                    href="#"
                    className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all whitespace-nowrap"
                  >
                    Apply Now
                  </Link>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <p className="text-slate-400 mb-4">Don't see a position that fits?</p>
            <Link 
              href="/contact"
              className="inline-block text-sky-400 hover:text-sky-300 font-semibold"
            >
              Send us your resume anyway →
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-br from-sky-900/30 to-purple-900/30 rounded-2xl p-12 border border-slate-700">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Join Us?</h2>
          <p className="text-slate-300 mb-8">
            Be part of a team that's revolutionizing content creation with AI.
          </p>
          <Link 
            href="#open-positions" 
            className="inline-block bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all shadow-lg"
          >
            View Open Positions
          </Link>
        </div>
      </section>
    </div>
  );
}
