import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Search, Filter, Grid, List, Star, Award, Sparkles } from 'lucide-react'
import { supabase, Tool } from '../lib/supabase'
import ToolCard from '../components/ToolCard'
import TopRecommendationOfTheDay from '../components/TopRecommendationOfTheDay'
import NewToolsThisMonth from '../components/NewToolsThisMonth'
import SearchBar from '../components/SearchBar'
import LoadingSpinner from '../components/LoadingSpinner'
import AdvancedFilters from '../components/AdvancedFilters'
import RealTimeUpdates from '../components/RealTimeUpdates'
import InfiniteScroll from '../components/InfiniteScroll'
import RecommendationEngine from '../components/RecommendationEngine'

type SortOption = 'popularity' | 'alphabetical' | 'newest'
type ViewMode = 'grid' | 'list'

interface FilterState {
  pricing: string[]
  rating: string
  categories: string[]
  features: string[]
  recent: boolean
}

function HomePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [allTools, setAllTools] = useState<Tool[]>([])
  const [displayedTools, setDisplayedTools] = useState<Tool[]>([])
  const [filteredTools, setFilteredTools] = useState<Tool[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '')
  const [sortBy, setSortBy] = useState<SortOption>('popularity')
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  
  const [filters, setFilters] = useState<FilterState>({
    pricing: [],
    rating: '',
    categories: [],
    features: [],
    recent: false
  })
  
  const category = searchParams.get('category')
  const toolsPerPage = 20

  useEffect(() => {
    loadAllTools()
  }, [])

  useEffect(() => {
    filterAndSortTools()
  }, [allTools, searchQuery, category, sortBy, filters])

  useEffect(() => {
    // Update search params when search query changes
    if (searchQuery) {
      setSearchParams(prev => {
        const newParams = new URLSearchParams(prev)
        newParams.set('search', searchQuery)
        return newParams
      })
    } else {
      setSearchParams(prev => {
        const newParams = new URLSearchParams(prev)
        newParams.delete('search')
        return newParams
      })
    }
  }, [searchQuery, setSearchParams])

  useEffect(() => {
    // Reset displayed tools when filters change
    setDisplayedTools(filteredTools.slice(0, toolsPerPage))
    setCurrentPage(1)
    setHasMore(filteredTools.length > toolsPerPage)
  }, [filteredTools])

  async function loadAllTools() {
    try {
      const { data, error } = await supabase
        .from('tools')
        .select('*')
        .order('popularity_score', { ascending: false })

      if (error) throw error
      setAllTools(data || [])
    } catch (error) {
      console.error('Error loading tools:', error)
    } finally {
      setLoading(false)
    }
  }

  function filterAndSortTools() {
    let filtered = [...allTools]

    // Filter by category
    if (category) {
      filtered = filtered.filter(tool => 
        tool.category.toLowerCase().replace(' ', '-') === category
      )
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(tool => 
        tool.name.toLowerCase().includes(query) ||
        tool.description.toLowerCase().includes(query) ||
        tool.category.toLowerCase().includes(query)
      )
    }

    // Apply advanced filters
    if (filters.pricing.length > 0) {
      // For now, we'll use a simple pricing detection based on common terms
      filtered = filtered.filter(tool => {
        const desc = tool.description.toLowerCase()
        if (filters.pricing.includes('Free') && (desc.includes('free') || desc.includes('open source'))) return true
        if (filters.pricing.includes('Paid') && (desc.includes('paid') || desc.includes('premium') || desc.includes('subscription'))) return true
        if (filters.pricing.includes('Freemium') && desc.includes('freemium')) return true
        return filters.pricing.length === 0
      })
    }

    if (filters.rating) {
      const minRating = parseFloat(filters.rating)
      filtered = filtered.filter(tool => (tool.popularity_score || 0) >= minRating)
    }

    if (filters.categories.length > 0) {
      filtered = filtered.filter(tool => 
        filters.categories.some(cat => tool.category.toLowerCase().includes(cat.toLowerCase()))
      )
    }

    if (filters.recent) {
      const thirtyDaysAgo = new Date()
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
      filtered = filtered.filter(tool => 
        new Date(tool.created_at || '') >= thirtyDaysAgo
      )
    }

    // Enhanced sorting logic
    switch (sortBy) {
      case 'popularity':
        filtered.sort((a, b) => {
          const classicTools = ['ChatGPT', 'Grammarly', 'Midjourney', 'Adobe Photoshop', 'AWS AI']
          const aIsClassic = classicTools.some(classic => a.name.includes(classic))
          const bIsClassic = classicTools.some(classic => b.name.includes(classic))
          
          const aIsNew = new Date(a.created_at || '').getFullYear() === 2025
          const bIsNew = new Date(b.created_at || '').getFullYear() === 2025
          
          if (aIsNew && !bIsNew) return -1
          if (!aIsNew && bIsNew) return 1
          if (!aIsClassic && bIsClassic) return -1
          if (aIsClassic && !bIsClassic) return 1
          
          return (b.popularity_score || 0) - (a.popularity_score || 0)
        })
        break
      case 'alphabetical':
        filtered.sort((a, b) => a.name.localeCompare(b.name))
        break
      case 'newest':
        filtered.sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime())
        break
    }

    setFilteredTools(filtered)
  }

  const loadMoreTools = () => {
    if (loadingMore || !hasMore) return
    
    setLoadingMore(true)
    
    // Simulate loading delay for better UX
    setTimeout(() => {
      const nextPage = currentPage + 1
      const startIndex = (nextPage - 1) * toolsPerPage
      const endIndex = startIndex + toolsPerPage
      const newTools = filteredTools.slice(startIndex, endIndex)
      
      setDisplayedTools(prev => [...prev, ...newTools])
      setCurrentPage(nextPage)
      setHasMore(endIndex < filteredTools.length)
      setLoadingMore(false)
    }, 800)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner />
          <p className="mt-4 text-gray-600 dark:text-gray-400 font-medium">
            Loading amazing AI tools...
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Real-time Updates Banner */}
        <RealTimeUpdates />

        {/* Enhanced Search Bar with Voice Search */}
        <div className="mb-8">
          <div className="search-filter-container max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <SearchBar 
                  searchQuery={searchQuery}
                  onSearchChange={setSearchQuery}
                  placeholder="🎯 Search AI tools by name, description, or category..."
                />
              </div>
              <div className="md:w-64">
                <select
                  value={category || ''}
                  onChange={(e) => {
                    if (e.target.value) {
                      setSearchParams({ category: e.target.value })
                    } else {
                      setSearchParams({})
                    }
                  }}
                  className="w-full px-4 py-4 text-lg border-2 border-gray-300 dark:border-gray-600 rounded-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-3 focus:ring-purple-500 focus:border-transparent shadow-sm hover:shadow-md transition-all font-medium"
                >
                  <option value="">🏷️ Filter by Category</option>
                  <option value="artificial-intelligence">🤖 Artificial Intelligence</option>
                  <option value="productivity">📈 Productivity</option>
                  <option value="marketing">📢 Marketing</option>
                  <option value="design">🎨 Design</option>
                  <option value="writing">✍️ Writing</option>
                  <option value="video">🎥 Video</option>
                  <option value="developer-tools">⚙️ Developer Tools</option>
                  <option value="education">📚 Education</option>
                  <option value="social-media">📱 Social Media</option>
                  <option value="content-creation">📝 Content Creation</option>
                  <option value="seo">🔍 SEO</option>
                  <option value="chatbots">💬 Chatbots</option>
                  <option value="data-analysis">📊 Data Analysis</option>
                  <option value="e-commerce">🛒 E-commerce</option>
                  <option value="research">🔬 Research</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Advanced Filters */}
        <AdvancedFilters 
          filters={filters}
          onFiltersChange={setFilters}
          isVisible={showAdvancedFilters}
          onToggle={() => setShowAdvancedFilters(!showAdvancedFilters)}
        />

        {/* Top Recommendation of the Day - only show on homepage without filters */}
        {!category && !searchQuery && !showAdvancedFilters && (
          <div className="mb-8">
            <TopRecommendationOfTheDay />
          </div>
        )}

        {/* New Tools This Month Section - only show on homepage without filters */}
        {!category && !searchQuery && !showAdvancedFilters && (
          <div className="mb-8">
            <NewToolsThisMonth />
          </div>
        )}

        {/* Enhanced Filter and Sort Controls */}
        <div id="all-ai-tools" className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div className="flex items-center space-x-4">
            <h1 className="heading-section text-gray-900 dark:text-gray-100">
              {category 
                ? `${category.charAt(0).toUpperCase() + category.slice(1).replace('-', ' ')} Tools` 
                : searchQuery 
                ? `Search Results for "${searchQuery}"` 
                : 'All AI Tools'
              }
            </h1>
            <span className="body-md text-gray-500 dark:text-gray-400">
              ({filteredTools.length} tools)
            </span>
            {filteredTools.length > 100 && (
              <span className="px-2 py-1 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 text-purple-600 dark:text-purple-400 rounded-full text-xs font-medium">
                🔥 Huge Collection!
              </span>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {/* Advanced Filters Toggle */}
            <AdvancedFilters 
              filters={filters}
              onFiltersChange={setFilters}
              isVisible={showAdvancedFilters}
              onToggle={() => setShowAdvancedFilters(!showAdvancedFilters)}
            />

            {/* Enhanced Sort Dropdown */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="px-4 py-2 border-2 border-gray-300 dark:border-gray-600 rounded-full text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-3 focus:ring-purple-500 focus:border-transparent font-medium transition-all hover:scale-105"
            >
              <option value="popularity">🏆 Most Popular</option>
              <option value="newest">✨ Newest First</option>
              <option value="alphabetical">🔤 A-Z</option>
            </select>

            {/* Enhanced View Mode Toggle */}
            <div className="flex border-2 border-gray-300 dark:border-gray-600 rounded-full overflow-hidden bg-white dark:bg-gray-800">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 transition-all ${
                  viewMode === 'grid' 
                    ? 'bg-gradient-to-r from-purple-100 to-blue-100 text-purple-600 dark:from-purple-900/30 dark:to-blue-900/30 dark:text-purple-400 scale-110' 
                    : 'text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 hover:scale-105'
                }`}
                title="Grid view"
                aria-label="Switch to grid view"
              >
                <Grid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 transition-all ${
                  viewMode === 'list' 
                    ? 'bg-gradient-to-r from-purple-100 to-blue-100 text-purple-600 dark:from-purple-900/30 dark:to-blue-900/30 dark:text-purple-400 scale-110' 
                    : 'text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 hover:scale-105'
                }`}
                title="List view"
                aria-label="Switch to list view"
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Tools Grid/List with Infinite Scroll */}
        {filteredTools.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-gray-400 mb-4 floating-element">
              <Search className="h-16 w-16 mx-auto" />
            </div>
            <h3 className="heading-md text-gray-900 dark:text-gray-100 mb-2">
              No tools found
            </h3>
            <p className="body-enhanced text-gray-500 dark:text-gray-400 mb-4">
              {searchQuery 
                ? `No tools match your search for "${searchQuery}"` 
                : category 
                ? `No tools found in the ${category} category` 
                : 'No tools available'
              }
            </p>
            {(searchQuery || category || Object.values(filters).some(f => Array.isArray(f) ? f.length > 0 : f)) && (
              <button
                onClick={() => {
                  setSearchQuery('')
                  setSearchParams({})
                  setFilters({
                    pricing: [],
                    rating: '',
                    categories: [],
                    features: [],
                    recent: false
                  })
                }}
                className="btn-primary btn-large"
              >
                Clear all filters and see all tools
              </button>
            )}
          </div>
        ) : (
          <>
            {/* Infinite Scroll Component */}
            <InfiniteScroll
              tools={displayedTools}
              loading={loadingMore}
              hasMore={hasMore}
              onLoadMore={loadMoreTools}
              viewMode={viewMode}
            />

            {/* AI Recommendations */}
            {displayedTools.length > 0 && !searchQuery && !category && (
              <div className="mt-12">
                <RecommendationEngine
                  currentTool={displayedTools[0]} // Use first tool as reference
                  allTools={allTools}
                />
              </div>
            )}
          </>
        )}
      </div>

      {/* Enhanced MiniMax Credit */}
      <div className="minimax-credit">
        Built with ❤️ by MiniMax Agent
      </div>
    </div>
  )
}

export default HomePage