import React, { useState, useEffect } from 'react'
import { Award, Star, ExternalLink, Sparkles } from 'lucide-react'
import { supabase, Tool } from '../lib/supabase'
import { openToolLink } from '../utils/affiliateLinks'

// High-rated tool recommendations (9.0+ rating) for daily rotation
const dailyRecommendations = [
  {
    name: "Synthesia",
    description: "Create professional AI videos with realistic avatars in minutes",
    link: "https://www.synthesia.io",
    logo_url: "https://logo.clearbit.com/synthesia.io",
    category: "Video",
    popularity_score: 4.8
  },
  {
    name: "Runway ML",
    description: "Advanced AI video generation and editing platform",
    link: "https://runwayml.com",
    logo_url: "https://logo.clearbit.com/runwayml.com",
    category: "Video",
    popularity_score: 4.7
  },
  {
    name: "Grammarly",
    description: "AI-powered writing assistant for flawless communication",
    link: "https://www.grammarly.com",
    logo_url: "https://logo.clearbit.com/grammarly.com",
    category: "Writing",
    popularity_score: 4.9
  },
  {
    name: "Midjourney",
    description: "Generate stunning artwork and images from text descriptions",
    link: "https://www.midjourney.com",
    logo_url: "https://logo.clearbit.com/midjourney.com",
    category: "Design",
    popularity_score: 4.8
  },
  {
    name: "Copy.ai",
    description: "AI copywriter that creates high-converting content instantly",
    link: "https://www.copy.ai",
    logo_url: "https://logo.clearbit.com/copy.ai",
    category: "Writing",
    popularity_score: 4.6
  },
  {
    name: "Jasper AI",
    description: "Enterprise AI platform for content creation and marketing",
    link: "https://www.jasper.ai",
    logo_url: "https://logo.clearbit.com/jasper.ai",
    category: "Marketing",
    popularity_score: 4.7
  },
  {
    name: "Claude",
    description: "Advanced AI assistant for complex reasoning and analysis",
    link: "https://claude.ai",
    logo_url: "https://logo.clearbit.com/anthropic.com",
    category: "AI Assistant",
    popularity_score: 4.8
  }
]

function getDailyRecommendation() {
  // Use current date to get consistent daily rotation
  const today = new Date()
  const dayOfYear = Math.floor((today.getTime() - new Date(today.getFullYear(), 0, 0).getTime()) / (1000 * 60 * 60 * 24))
  const index = dayOfYear % dailyRecommendations.length
  return dailyRecommendations[index]
}

function renderStars(rating: number) {
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)
  
  return '★'.repeat(fullStars) + (hasHalfStar ? '½' : '') + '☆'.repeat(emptyStars)
}

function TopRecommendationOfTheDay() {
  const [topRecommendation, setTopRecommendation] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get today's recommendation from daily rotation
    const dailyTool = getDailyRecommendation()
    setTopRecommendation(dailyTool)
    setLoading(false)
  }, [])

  const handleVisitTool = () => {
    if (topRecommendation) {
      openToolLink(topRecommendation.link)
    }
  }

  const handleLearnMore = () => {
    if (topRecommendation) {
      // Scroll to the tool in the main list or show more info
      const toolName = topRecommendation.name.toLowerCase().replace(/\s+/g, '-')
      window.location.href = `?search=${encodeURIComponent(topRecommendation.name)}`
    }
  }

  if (loading) {
    return (
      <div className="recommendation-section top-recommendation-gradient">
        <div className="animate-pulse">
          <div className="flex items-center mb-4">
            <div className="w-6 h-6 bg-white/20 rounded mr-2"></div>
            <div className="w-48 h-6 bg-white/20 rounded"></div>
          </div>
          <div className="flex items-center margin-top: 15px">
            <div className="w-15 h-15 bg-white/20 rounded-full mr-4"></div>
            <div className="flex-1">
              <div className="w-48 h-8 bg-white/20 rounded mb-4"></div>
              <div className="w-full h-4 bg-white/20 rounded mb-2"></div>
              <div className="w-3/4 h-4 bg-white/20 rounded mb-4"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!topRecommendation) {
    return null
  }

  return (
    <div className="top-recommendation-gradient">
      <div className="flex items-center mb-6">
        <span className="star-icon" style={{color: '#FFD700', marginRight: '12px', fontSize: '28px'}}>⭐</span>
        <h2 className="top-recommendation-title">
          Top Recommendation of the Day
        </h2>
      </div>
      
      <div className="featured-tool-large" style={{display: 'flex', alignItems: 'center', gap: '24px'}}>
        <div className="tool-logo" style={{flexShrink: 0}}>
          <img 
            src={topRecommendation.logo_url} 
            alt={`${topRecommendation.name} logo`} 
            style={{
              width: '80px', 
              height: '80px', 
              borderRadius: '50%', 
              border: '3px solid rgba(255,255,255,0.3)',
              background: 'rgba(255,255,255,0.1)'
            }}
            onError={(e) => {
              const target = e.target as HTMLImageElement
              target.outerHTML = `<div style="width: 80px; height: 80px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: bold;">${topRecommendation.name.charAt(0)}</div>`
            }}
          />
        </div>
        
        <div className="tool-info" style={{flex: 1}}>
          <h3 style={{margin: '0 0 8px 0', fontSize: '24px', fontWeight: '600'}}>
            {topRecommendation.name}
          </h3>
          <p style={{margin: '0 0 12px 0', opacity: 0.9, fontSize: '16px', lineHeight: 1.5}}>
            {topRecommendation.description}
          </p>
          <div className="stars" style={{color: '#FFD700', fontSize: '18px', fontWeight: 'bold', marginBottom: '16px'}}>
            {renderStars(topRecommendation.popularity_score)} {topRecommendation.popularity_score}/5
          </div>
          
          <div style={{display: 'flex', gap: '12px', alignItems: 'center'}}>
            <button 
              onClick={handleVisitTool}
              className="btn-blue"
              style={{
                background: 'white', 
                color: '#3B82F6', 
                padding: '12px 24px', 
                borderRadius: '25px', 
                border: 'none', 
                fontWeight: '600', 
                cursor: 'pointer',
                fontSize: '16px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.15)'
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)'
              }}
            >
              Explore Now
            </button>
            
            <button
              onClick={handleLearnMore}
              className="btn-teal-outline"
              style={{
                background: 'transparent', 
                color: 'white', 
                padding: '12px 16px', 
                border: '2px solid #14B8A6', 
                borderRadius: '25px', 
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = '#14B8A6'
                e.currentTarget.style.borderColor = '#14B8A6'
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = 'transparent'
                e.currentTarget.style.borderColor = '#14B8A6'
              }}
            >
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TopRecommendationOfTheDay