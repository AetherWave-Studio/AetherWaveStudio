import React from 'react'
import { Link } from 'react-router-dom'
import { Search, Globe, Users, Mail, ExternalLink, Target, Heart, Zap } from 'lucide-react'

function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-poppins font-bold text-gray-900 mb-6">
            About <span className="text-purple-600">AetherWave</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your comprehensive directory of 1000+ AI tools, curated to help you discover 
            the perfect AI solution for every task and industry.
          </p>
        </div>

        {/* Mission Section */}
        <div className="bg-white rounded-2xl shadow-sm p-8 mb-12">
          <div className="flex items-center mb-6">
            <div className="p-3 bg-purple-100 rounded-full mr-4">
              <Target className="h-6 w-6 text-purple-600" />
            </div>
            <h2 className="text-2xl font-poppins font-bold text-gray-900">Our Mission</h2>
          </div>
          <p className="text-gray-600 leading-relaxed mb-4">
            At AetherWave Studio, we believe artificial intelligence should be accessible to everyone. 
            Our mission is to bridge the gap between innovative AI solutions and the people 
            who need them most.
          </p>
          <p className="text-gray-600 leading-relaxed">
            We carefully curate and categorize the best AI tools available, making it easy 
            for artists, entrepreneurs, students, and curious minds to find the right 
            AI solution for their specific needs.
          </p>
        </div>

        {/* What is AIverse Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="bg-white rounded-2xl shadow-sm p-8">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-blue-100 rounded-full mr-4">
                <Globe className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-poppins font-bold text-gray-900">What is AetherWave Studio</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              AEtherWave provides the world's most comprehensive directory of AI tools and platforms. 
              We've cataloged over 1,000 AI solutions across 15+ categories, from content creation 
              and productivity to marketing and development tools.
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-sm p-8">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-green-100 rounded-full mr-4">
                <Search className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-poppins font-bold text-gray-900">Why We Curate AI Tools</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              The AI landscape is vast and constantly evolving. Instead of getting lost in endless 
              searches, we provide a trusted, organized platform where quality AI tools are 
              properly categorized, reviewed, and continuously updated.
            </p>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mb-12">
          <h2 className="text-2xl font-poppins font-bold text-gray-900 mb-8 text-center">
            What Makes AIverse Special
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <div className="p-4 bg-purple-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <Heart className="h-8 w-8 text-purple-600" />
              </div>
              <h4 className="font-poppins font-semibold text-gray-900 mb-2">Carefully Curated</h4>
              <p className="text-sm text-gray-600">Every tool is manually reviewed and tested for quality and reliability</p>
            </div>
            
            <div className="text-center p-6">
              <div className="p-4 bg-blue-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <Zap className="h-8 w-8 text-blue-600" />
              </div>
              <h4 className="font-poppins font-semibold text-gray-900 mb-2">Always Updated</h4>
              <p className="text-sm text-gray-600">New tools added weekly, with regular updates to existing listings</p>
            </div>
            
            <div className="text-center p-6">
              <div className="p-4 bg-green-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <Users className="h-8 w-8 text-green-600" />
              </div>
              <h4 className="font-poppins font-semibold text-gray-900 mb-2">Community Driven</h4>
              <p className="text-sm text-gray-600">Recommendations and submissions from our growing user community</p>
            </div>
          </div>
        </div>

        {/* Contact Section */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
          <div className="text-center mb-8">
            <div className="p-3 bg-white/20 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Mail className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-2xl font-poppins font-bold mb-4">Get in Touch</h2>
            <p className="text-purple-100 mb-6">
              Have a suggestion for a new AI tool? Found an issue? Want to partner with us? 
              We'd love to hear from you!
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://docs.google.com/forms/d/e/1FAIpQLSfJL7xP6G_V0GPNTPdcpxOqbP899MJa7L49-qQp72-CxJ7GfQ/viewform?usp=dialog"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center px-6 py-3 bg-white text-purple-600 rounded-full font-medium hover:bg-purple-50 transition-colors"
            >
              Submit an AI Tool
              <ExternalLink className="ml-2 h-4 w-4" />
            </a>
            
            <Link
              to="/"
              className="flex items-center justify-center px-6 py-3 bg-white/20 text-white rounded-full font-medium hover:bg-white/30 transition-colors border border-white/30"
            >
              Explore Tools
              <Search className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-12 grid grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-3xl font-poppins font-bold text-purple-600 mb-2">1000+</div>
            <div className="text-gray-600 text-sm">AI Tools Listed</div>
          </div>
          <div>
            <div className="text-3xl font-poppins font-bold text-blue-600 mb-2">15+</div>
            <div className="text-gray-600 text-sm">Categories</div>
          </div>
          <div>
            <div className="text-3xl font-poppins font-bold text-green-600 mb-2">Daily</div>
            <div className="text-gray-600 text-sm">Updates</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AboutPage