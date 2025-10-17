import React, { useState } from 'react'
import { Filter, X } from 'lucide-react'

interface FilterState {
  pricing: string[]
  rating: string
  categories: string[]
  features: string[]
  recent: boolean
}

interface AdvancedFiltersProps {
  filters: FilterState
  onFiltersChange: (filters: FilterState) => void
  isVisible: boolean
  onToggle: () => void
}

function AdvancedFilters({ filters, onFiltersChange, isVisible, onToggle }: AdvancedFiltersProps) {
  const handleFilterChange = (category: keyof FilterState, value: any, checked?: boolean) => {
    if (category === 'pricing' || category === 'categories' || category === 'features') {
      const currentArray = filters[category] as string[]
      let newArray
      if (checked) {
        newArray = [...currentArray, value]
      } else {
        newArray = currentArray.filter(item => item !== value)
      }
      onFiltersChange({ ...filters, [category]: newArray })
    } else {
      onFiltersChange({ ...filters, [category]: value })
    }
  }

  const clearAllFilters = () => {
    onFiltersChange({
      pricing: [],
      rating: '',
      categories: [],
      features: [],
      recent: false
    })
  }

  const hasActiveFilters = filters.pricing.length > 0 || 
                          filters.rating || 
                          filters.categories.length > 0 || 
                          filters.features.length > 0 || 
                          filters.recent

  if (!isVisible) {
    return (
      <button
        onClick={onToggle}
        className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 rounded-full text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all"
        aria-label="Show advanced filters"
      >
        <Filter className="h-4 w-4" />
        Advanced Filters
        {hasActiveFilters && (
          <span className="bg-purple-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {filters.pricing.length + filters.categories.length + filters.features.length + (filters.rating ? 1 : 0) + (filters.recent ? 1 : 0)}
          </span>
        )}
      </button>
    )
  }

  return (
    <div className="advanced-filters filter-transition">
      <div className="flex items-center justify-between mb-4">
        <h3 className="heading-md text-gray-900 dark:text-gray-100">
          Advanced Filters
        </h3>
        <div className="flex items-center gap-2">
          {hasActiveFilters && (
            <button
              onClick={clearAllFilters}
              className="text-sm text-purple-600 hover:text-purple-700 font-medium"
            >
              Clear All
            </button>
          )}
          <button
            onClick={onToggle}
            className="p-1 rounded-md text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
            aria-label="Hide advanced filters"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Pricing Filter */}
        <div className="filter-group">
          <label>Pricing</label>
          <div className="multi-select">
            {['Free', 'Paid', 'Freemium'].map(option => (
              <label key={option} className="checkbox-label">
                <input 
                  type="checkbox"
                  checked={filters.pricing.includes(option)}
                  onChange={(e) => handleFilterChange('pricing', option, e.target.checked)}
                />
                {option}
              </label>
            ))}
          </div>
        </div>

        {/* Rating Filter */}
        <div className="filter-group">
          <label>Minimum Rating</label>
          <select 
            value={filters.rating || ''}
            onChange={(e) => handleFilterChange('rating', e.target.value)}
            className="w-full px-3 py-2 border-2 border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">Any Rating</option>
            <option value="4">4+ Stars</option>
            <option value="4.5">4.5+ Stars</option>
            <option value="5">5 Stars Only</option>
          </select>
        </div>

        {/* Categories Filter */}
        <div className="filter-group">
          <label>Categories</label>
          <div className="multi-select">
            {['Design', 'Writing', 'Productivity', 'Developer Tools'].map(option => (
              <label key={option} className="checkbox-label">
                <input 
                  type="checkbox"
                  checked={filters.categories.includes(option)}
                  onChange={(e) => handleFilterChange('categories', option, e.target.checked)}
                />
                {option}
              </label>
            ))}
          </div>
        </div>

        {/* Recent Filter */}
        <div className="filter-group">
          <label>Recently Added</label>
          <button 
            className={`filter-chip w-full ${filters.recent ? 'active' : ''}`}
            onClick={() => handleFilterChange('recent', !filters.recent)}
          >
            Last 30 Days
          </button>
        </div>
      </div>
    </div>
  )
}

export default AdvancedFilters