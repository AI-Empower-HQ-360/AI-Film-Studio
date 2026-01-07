import Link from 'next/link';

export default function PricingPage() {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      duration: '/month',
      description: 'Perfect for trying out AI Film Studio',
      features: [
        '3 film generations per month',
        '30-second films only',
        'Basic templates',
        'Standard resolution (720p)',
        'Community support',
        'Watermarked output'
      ],
      buttonText: 'Start Free',
      buttonStyle: 'bg-slate-700 hover:bg-slate-600 text-white',
      popular: false
    },
    {
      name: 'Pro',
      price: '$29',
      duration: '/month',
      description: 'For content creators and small businesses',
      features: [
        '50 film generations per month',
        'Up to 90-second films',
        'Premium templates & styles',
        'HD resolution (1080p)',
        'Advanced AI models',
        'No watermarks',
        'Priority support',
        'Custom branding'
      ],
      buttonText: 'Start Pro Trial',
      buttonStyle: 'bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white',
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      duration: '',
      description: 'For agencies and large organizations',
      features: [
        'Unlimited film generations',
        'Custom film durations',
        'White-label solution',
        '4K resolution support',
        'Custom AI model training',
        'API access',
        'Dedicated support manager',
        'SLA guarantee',
        'Team collaboration tools',
        'Advanced analytics'
      ],
      buttonText: 'Contact Sales',
      buttonStyle: 'bg-slate-700 hover:bg-slate-600 text-white border border-slate-500',
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-purple-500 bg-clip-text text-transparent">
                🎬 AI Film Studio
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/#features" className="text-slate-300 hover:text-white transition-colors">
                Features
              </Link>
              <Link href="/#how-it-works" className="text-slate-300 hover:text-white transition-colors">
                How It Works
              </Link>
              <Link href="/pricing" className="text-white font-medium">
                Pricing
              </Link>
              <button className="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
            Choose Your{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Creative Plan
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-16">
            From free experimentation to enterprise-scale production. 
            Start creating AI-powered films that match your ambition.
          </p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-8 lg:gap-12">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`relative bg-slate-800/50 rounded-2xl p-8 border transition-all hover:transform hover:scale-105 ${
                  plan.popular 
                    ? 'border-sky-500 shadow-2xl shadow-sky-500/25 bg-gradient-to-b from-slate-800/80 to-slate-800/50' 
                    : 'border-slate-700 hover:border-slate-600'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-sky-500 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}

                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="flex items-baseline justify-center mb-4">
                    <span className="text-4xl lg:text-5xl font-bold text-white">{plan.price}</span>
                    {plan.duration && <span className="text-slate-400 ml-2">{plan.duration}</span>}
                  </div>
                  <p className="text-slate-300">{plan.description}</p>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <span className="text-sky-400 mr-3 mt-0.5">✓</span>
                      <span className="text-slate-300">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all shadow-lg ${plan.buttonStyle}`}>
                  {plan.buttonText}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/30">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-slate-400 text-center mb-16">
            Everything you need to know about our pricing and plans
          </p>
          
          <div className="grid gap-8">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-3">Can I upgrade or downgrade my plan?</h3>
              <p className="text-slate-300">
                Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, 
                and we&apos;ll prorate the billing accordingly.
              </p>
            </div>
            
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-3">What happens if I exceed my monthly limit?</h3>
              <p className="text-slate-300">
                When you reach your monthly generation limit, you can either wait for the next billing cycle 
                or upgrade to a higher plan for immediate access to more generations.
              </p>
            </div>
            
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-3">Do you offer refunds?</h3>
              <p className="text-slate-300">
                We offer a 14-day money-back guarantee for all paid plans. If you&apos;re not satisfied, 
                we&apos;ll refund your payment, no questions asked.
              </p>
            </div>
            
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-3">Can I use the films commercially?</h3>
              <p className="text-slate-300">
                Yes! All Pro and Enterprise plans include full commercial usage rights. 
                Free plan films have a watermark and are for personal/educational use only.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Stories?
          </h2>
          <p className="text-xl text-slate-300 mb-10">
            Join thousands of creators who are already using AI Film Studio to bring their visions to life.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="w-full sm:w-auto bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all shadow-lg shadow-sky-500/25">
              Start Creating Today
            </button>
            <Link href="/" className="w-full sm:w-auto bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-colors border border-slate-600 text-center">
              Learn More
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}