import React, { useState } from 'react'
import { ExternalLink, Star, Heart, Award, Sparkles } from 'lucide-react'
import { Tool } from '../lib/supabase'
import { openToolLink } from '../utils/affiliateLinks'

interface ToolCardProps {
  tool: Tool
  viewMode: 'grid' | 'list'
}

function ToolCard({ tool, viewMode }: ToolCardProps) {
  const [imageError, setImageError] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const handleToolClick = () => {
    openToolLink(tool.link)
  }

  const handleImageError = () => {
    setImageError(true)
  }

  // Clean description by removing redundant AI references
  const cleanDescription = tool.description
    .replace(/artificial intelligence/gi, '')
    .replace(/\bAI\b/g, '')
    .replace(/\s+/g, ' ')
    .trim()

  // Determine if tool is new (created in last 30 days)
  const isNew = tool.created_at && 
    new Date(tool.created_at).getTime() > Date.now() - (30 * 24 * 60 * 60 * 1000)

  // Determine if tool is highly rated
  const isHighRated = (tool.popularity_score || 0) >= 8.5

  // List view layout
  if (viewMode === 'list') {
    return (
      <div className="tool-card-list group hover:scale-[1.01] transition-all duration-300">
        <div className="flex items-center space-x-4 w-full">
          {/* Logo with 3D effect */}
          <div className="flex-shrink-0">
            {!imageError && tool.logo_url ? (
              <img
                src={tool.logo_url}
                alt={`${tool.name} logo`}
                className="card-icon tool-logo-3d"
                onError={handleImageError}
                loading="lazy"
              />
            ) : (
              <div className="logo-fallback tool-logo-3d">
                {tool.name.charAt(0).toUpperCase()}
              </div>
            )}
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            {/* Tool Name with badges */}
            <div className="flex items-center mb-2">
              <h3 className="card-title mr-3 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                {tool.name}
              </h3>
              {isNew && (
                <span className="px-2 py-1 bg-gradient-to-r from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 text-green-600 dark:text-green-400 rounded-full text-xs font-medium mr-2">
                  ✨ New
                </span>
              )}
              {isHighRated && (
                <span className="px-2 py-1 bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30 text-yellow-600 dark:text-yellow-400 rounded-full text-xs font-medium">
                  🏆 Top Rated
                </span>
              )}
            </div>
            
            {/* Description */}
            <p className="card-description mb-3 group-hover:text-gray-700 dark:group-hover:text-gray-200 transition-colors">
              {cleanDescription}
            </p>
            
            {/* Bottom Row: Category and Actions */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="category-badge">
                  {tool.category === 'Artificial Intelligence' ? 'AI Tools' : tool.category}
                </span>
                {tool.popularity_score && (
                  <div className="flex items-center space-x-1">
                    <Star className="h-3 w-3 text-yellow-400 fill-current" />
                    <span className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                      {tool.popularity_score.toFixed(1)}
                    </span>
                  </div>
                )}
              </div>
              
              {/* Visit Button */}
              <button
                onClick={handleToolClick}
                className="visit-button group-hover:scale-105 transition-transform"
                title={`Visit ${tool.name}`}
                aria-label={`Visit ${tool.name} website`}
              >
                Visit
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Grid view - Enhanced with premium effects
  return (
    <div 
      className="tool-card neumorphic-card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="card-header">
        {!imageError && tool.logo_url ? (
          <img
            src={tool.logo_url}
            alt={`${tool.name} logo`}
            className={`card-icon tool-logo-3d ${isHovered ? 'floating-element' : ''}`}
            onError={handleImageError}
            loading="lazy"
          />
        ) : (
          <div className={`logo-fallback tool-logo-3d ${isHovered ? 'floating-element' : ''}`}>
            {tool.name.charAt(0).toUpperCase()}
          </div>
        )}
        <div className="card-content">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="card-title">{tool.name}</h3>
            {isNew && (
              <span title="New tool">
                <Sparkles className="h-4 w-4 text-green-500 animate-pulse" />
              </span>
            )}
            {isHighRated && (
              <span title="Top rated">
                <Award className="h-4 w-4 text-yellow-500" />
              </span>
            )}
          </div>
          <p className="card-description">
            {cleanDescription}
          </p>
          {/* Rating display */}
          {tool.popularity_score && (
            <div className="flex items-center space-x-1 mt-2">
              <Star className="h-3 w-3 text-yellow-400 fill-current" />
              <span className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                {tool.popularity_score.toFixed(1)} / 10
              </span>
            </div>
          )}
          {/* Category badge */}
          <div className="mt-3">
            <span className="category-badge">
              {tool.category === 'Artificial Intelligence' ? 'AI Tools' : tool.category}
            </span>
          </div>
        </div>
      </div>
      <div className="card-footer">
        <button
          onClick={handleToolClick}
          className="visit-button"
          title={`Visit ${tool.name}`}
          aria-label={`Visit ${tool.name} website`}
        >
          <span>Visit</span>
          <ExternalLink className="h-3 w-3 ml-1 opacity-0 group-hover:opacity-100 transition-opacity" />
        </button>
      </div>
    </div>
  )
}

export default ToolCard