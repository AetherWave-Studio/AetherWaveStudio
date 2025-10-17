import React, { useState, useEffect } from 'react'
import { Tool } from '../lib/supabase'
import ToolCard from './ToolCard'

interface RecommendationEngineProps {
  currentTool?: Tool
  allTools: Tool[]
}

function RecommendationEngine({ currentTool, allTools }: RecommendationEngineProps) {
  const [recommendations, setRecommendations] = useState<Tool[]>([])

  useEffect(() => {
    if (!currentTool || allTools.length === 0) return

    // Simple recommendation algorithm based on categories, tags, and popularity
    const similarTools = allTools
      .filter(tool => tool.id !== currentTool.id) // Exclude current tool
      .map(tool => {
        let score = 0
        
        // Category match (high weight)
        if (tool.category === currentTool.category) {
          score += 10
        }
        
        // Popularity score (medium weight)
        score += (tool.popularity_score || 0) * 0.1
        
        // Recent tools get slight boost
        const isRecent = new Date(tool.created_at || '').getTime() > Date.now() - (30 * 24 * 60 * 60 * 1000)
        if (isRecent) {
          score += 2
        }
        
        return { ...tool, recommendationScore: score }
      })
      .sort((a, b) => (b.recommendationScore || 0) - (a.recommendationScore || 0))
      .slice(0, 4) // Top 4 recommendations
    
    setRecommendations(similarTools)
  }, [currentTool, allTools])

  if (!currentTool || recommendations.length === 0) {
    return null
  }

  return (
    <div className="recommendations-section">
      <h3 className="heading-md mb-4 flex items-center gap-2">
        <span className="text-2xl">🤖</span>
        Tools like {currentTool.name}
      </h3>
      <div className="recommendations-grid">
        {recommendations.map(tool => (
          <ToolCard key={tool.id} tool={tool} viewMode="grid" />
        ))}
      </div>
    </div>
  )
}

export default RecommendationEngine