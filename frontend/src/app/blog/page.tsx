import Navigation from "@/app/components/Navigation";

export default function Blog() {
  const posts = [
    {
      title: "Introducing AI Film Studio: Transform Scripts into Films",
      excerpt: "We're excited to announce the launch of AI Film Studio, a revolutionary platform that uses AI to convert text scripts into cinematic short films.",
      date: "January 15, 2026",
      category: "Product",
      readTime: "5 min read",
      image: "🎬"
    },
    {
      title: "How We Built a 7-Stage AI Pipeline for Video Generation",
      excerpt: "A deep dive into our AI architecture: from script analysis to final video output, exploring the technologies and challenges we overcame.",
      date: "January 10, 2026",
      category: "Engineering",
      readTime: "12 min read",
      image: "⚙️"
    },
    {
      title: "The Future of Content Creation: AI and Human Creativity",
      excerpt: "Exploring how AI tools like ours augment rather than replace human creativity, and what this means for the future of filmmaking.",
      date: "January 5, 2026",
      category: "Insights",
      readTime: "8 min read",
      image: "🤖"
    },
    {
      title: "Stable Diffusion XL: Why We Chose It for Image Generation",
      excerpt: "Technical breakdown of why Stable Diffusion XL is the backbone of our image generation pipeline and how we optimized it for production.",
      date: "December 28, 2025",
      category: "AI/ML",
      readTime: "10 min read",
      image: "🎨"
    },
    {
      title: "Scaling AI Video Generation on AWS",
      excerpt: "Our infrastructure journey: how we built a cloud-native platform capable of handling thousands of concurrent video generation requests.",
      date: "December 20, 2025",
      category: "Infrastructure",
      readTime: "15 min read",
      image: "☁️"
    },
    {
      title: "Creating Culturally Aware AI Content",
      excerpt: "How we implemented cultural context awareness in our image generation to create authentic, diverse visual content.",
      date: "December 15, 2025",
      category: "AI/ML",
      readTime: "7 min read",
      image: "🌍"
    }
  ];

  const categories = ["All", "Product", "Engineering", "AI/ML", "Infrastructure", "Insights"];

  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            The AI Film Studio{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Blog
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Insights on AI, filmmaking, engineering, and the future of content creation.
          </p>
        </div>
      </section>

      {/* Categories */}
      <section className="py-8 px-4 sm:px-6 lg:px-8 bg-slate-800/50 sticky top-16 z-40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 overflow-x-auto pb-2">
            {categories.map((category, index) => (
              <button
                key={index}
                className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-all ${
                  index === 0
                    ? 'bg-gradient-to-r from-sky-500 to-purple-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Posts Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post, index) => (
              <article 
                key={index} 
                className="bg-slate-800/50 rounded-xl border border-slate-700 hover:border-sky-500/50 transition-all overflow-hidden group cursor-pointer"
              >
                <div className="h-48 bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center text-6xl group-hover:scale-110 transition-transform">
                  {post.image}
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-3 mb-3 text-sm">
                    <span className="px-3 py-1 bg-sky-500/20 text-sky-400 rounded-full">
                      {post.category}
                    </span>
                    <span className="text-slate-400">{post.readTime}</span>
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-sky-400 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-slate-400 mb-4 line-clamp-3">{post.excerpt}</p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-500">{post.date}</span>
                    <span className="text-sky-400 group-hover:translate-x-1 transition-transform inline-block">
                      Read more →
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>

          {/* Load More */}
          <div className="mt-12 text-center">
            <button className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-semibold transition-colors">
              Load More Articles
            </button>
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Stay Updated</h2>
          <p className="text-slate-300 mb-8">
            Subscribe to our newsletter for the latest updates on AI, product features, and company news.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20"
            />
            <button className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-lg whitespace-nowrap">
              Subscribe
            </button>
          </div>
          <p className="text-xs text-slate-500 mt-4">
            We respect your privacy. Unsubscribe anytime.
          </p>
        </div>
      </section>
    </div>
  );
}
