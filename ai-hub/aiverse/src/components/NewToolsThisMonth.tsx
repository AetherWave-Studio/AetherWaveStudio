import React, { useState, useEffect } from 'react'
import { Star, ChevronRight, Calendar } from 'lucide-react'
import { openToolLink } from '../utils/affiliateLinks'

// New tools data from Toolify.ai for August 2025
const newToolsData = [
  {"name": "ChatGPT", "description": "Language model for generating responses.", "link": "https://chat.openai.com", "logo_url": "https://logo.clearbit.com/openai.com", "stars": 5, "category": "Chatbots", "featured": true},
  {"name": "Midjourney", "description": "Platform for creating images from text.", "link": "https://www.midjourney.com", "logo_url": "https://logo.clearbit.com/midjourney.com", "stars": 4, "category": "Design", "featured": true},
  {"name": "Copy.ai", "description": "Templates for blog and social content.", "link": "https://www.copy.ai", "logo_url": "https://logo.clearbit.com/copy.ai", "stars": 4, "category": "Writing", "featured": true},
  {"name": "Grammarly", "description": "Checks grammar, spelling, and style.", "link": "https://www.grammarly.com", "logo_url": "https://logo.clearbit.com/grammarly.com", "stars": 5, "category": "Writing", "featured": true},
  {"name": "Adobe Photoshop Generative Fill", "description": "Adds or modifies image content.", "link": "https://www.adobe.com/products/photoshop.html", "logo_url": "https://logo.clearbit.com/adobe.com", "stars": 5, "category": "Design", "featured": true},
  {"name": "Taskade", "description": "Outlines and mindmaps for instructors.", "link": "https://www.taskade.com", "logo_url": "https://logo.clearbit.com/taskade.com", "stars": 4, "category": "Productivity", "featured": true},
  {"name": "QuillBot", "description": "Enhances writing fluency.", "link": "https://quillbot.com", "logo_url": "https://logo.clearbit.com/quillbot.com", "stars": 4, "category": "Writing", "featured": true},
  {"name": "AWS AI", "description": "Suite for NLP and vision.", "link": "https://aws.amazon.com/ai", "logo_url": "https://logo.clearbit.com/aws.amazon.com", "stars": 4, "category": "Developer Tools", "featured": true},
  {"name": "Lumen5", "description": "Video generator from text inputs.", "link": "https://www.lumen5.com", "logo_url": "https://logo.clearbit.com/lumen5.com", "stars": 4, "category": "Video"},
  {"name": "Surfer SEO", "description": "SEO tool for improving rankings.", "link": "https://surferseo.com", "logo_url": "https://logo.clearbit.com/surferseo.com", "stars": 4, "category": "SEO"},
  {"name": "Writesonic", "description": "Marketing and ad content creator.", "link": "https://writesonic.com", "logo_url": "https://logo.clearbit.com/writesonic.com", "stars": 4, "category": "Marketing"},
  {"name": "Filmora", "description": "Video editing with smart cutout and denoise.", "link": "https://filmora.wondershare.com", "logo_url": "https://logo.clearbit.com/wondershare.com", "stars": 4, "category": "Video"},
  {"name": "Summarize.tech", "description": "Digests YouTube videos into summaries.", "link": "https://www.summarize.tech", "logo_url": "https://logo.clearbit.com/summarize.tech", "stars": 4, "category": "Productivity"},
  {"name": "Udio", "description": "Music generator from prompts.", "link": "https://www.udio.com", "logo_url": "https://logo.clearbit.com/udio.com", "stars": 4, "category": "Content Creation"},
  {"name": "Quizizz", "description": "Assessments to enhance learning.", "link": "https://quizizz.com", "logo_url": "https://logo.clearbit.com/quizizz.com", "stars": 4, "category": "Education"},
  {"name": "Freepik AI", "description": "High-quality images and illustrations.", "link": "https://www.freepik.com/ai", "logo_url": "https://logo.clearbit.com/freepik.com", "stars": 4, "category": "Design"},
  {"name": "Runway", "description": "Generates images and videos from text.", "link": "https://runwayml.com", "logo_url": "https://logo.clearbit.com/runwayml.com", "stars": 4, "category": "Video"},
  {"name": "Recraft", "description": "Creates visuals and vector graphics.", "link": "https://www.recraft.ai", "logo_url": "https://logo.clearbit.com/recraft.ai", "stars": 4, "category": "Design"},
  {"name": "TubeBuddy", "description": "Channel management and SEO.", "link": "https://www.tubebuddy.com", "logo_url": "https://logo.clearbit.com/tubebuddy.com", "stars": 4, "category": "Social Media"},
  {"name": "VidIQ A.I.", "description": "Analytics for content optimization.", "link": "https://vidiq.com", "logo_url": "https://logo.clearbit.com/vidiq.com", "stars": 4, "category": "Social Media"}
]

function renderStars(rating: number) {
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 !== 0
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)
  
  return '★'.repeat(fullStars) + (hasHalfStar ? '½' : '') + '☆'.repeat(emptyStars)
}

function NewToolsThisMonth() {
  const [showAll, setShowAll] = useState(false)
  
  // Show first 20 tools: mix of popular and new
  const displayTools = showAll ? newToolsData : newToolsData.slice(0, 20)
  
  return (
    <div className="new-tools-section">
      {/* Header */}
      <div className="new-tools-header">
        <Calendar className="star-icon h-8 w-8" />
        <span>Top AI Tools</span>
      </div>
      
      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {displayTools.map((tool, index) => (
          <div
            key={index}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-4 hover:bg-white/20 transition-all duration-300 cursor-pointer"
            onClick={() => openToolLink(tool.link)}
          >
            <div className="flex items-center space-x-3 mb-3">
              {tool.logo_url ? (
                <img
                  src={tool.logo_url}
                  alt={`${tool.name} logo`}
                  className="w-10 h-10 object-cover rounded-lg bg-white/20"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                  }}
                />
              ) : (
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                  {tool.name.charAt(0).toUpperCase()}
                </div>
              )}
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-white text-sm truncate">
                  {tool.name}
                </h4>
                <div className="star-rating text-xs">
                  {renderStars(tool.stars)}
                </div>
              </div>
            </div>
            
            <p className="text-white/80 text-xs leading-relaxed mb-3 line-clamp-2">
              {tool.description}
            </p>
            
            <div className="flex items-center justify-between">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-white/20 text-white">
                {tool.category}
              </span>
              <ChevronRight className="h-4 w-4 text-white/60" />
            </div>
          </div>
        ))}
      </div>
      
      {/* Show More Button */}
      {!showAll && newToolsData.length > 20 && (
        <div className="text-center">
          <button
            onClick={() => setShowAll(true)}
            className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-full font-medium transition-all duration-300 inline-flex items-center"
          >
            Show All {newToolsData.length} New Tools
            <ChevronRight className="ml-2 h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  )
}

export default NewToolsThisMonth