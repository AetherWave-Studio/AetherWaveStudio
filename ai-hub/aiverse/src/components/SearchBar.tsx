import React from 'react'
import { Search } from 'lucide-react'
import VoiceSearch from './VoiceSearch'

interface SearchBarProps {
  searchQuery: string
  onSearchChange: (query: string) => void
  placeholder?: string
}

function SearchBar({ searchQuery, onSearchChange, placeholder = "Search AI tools..." }: SearchBarProps) {
  const handleVoiceResult = (transcript: string) => {
    onSearchChange(transcript)
  }

  const clearSearch = () => {
    onSearchChange('')
  }

  return (
    <div className="relative max-w-2xl mx-auto">
      <div className="relative">
        {/* Search Icon */}
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400 dark:text-gray-500" />
        </div>
        
        {/* Search Input */}
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="
            block w-full pl-12 pr-20 py-4 text-lg 
            border-2 border-gray-300 dark:border-gray-600 rounded-2xl 
            bg-white dark:bg-gray-800 
            text-gray-900 dark:text-gray-100 
            focus:outline-none focus:ring-3 focus:ring-purple-500 focus:border-transparent 
            placeholder-gray-500 dark:placeholder-gray-400 
            shadow-sm hover:shadow-md transition-all 
            search-input font-medium
          "
          placeholder={placeholder}
          aria-label="Search AI tools"
        />
        
        {/* Voice Search & Clear Button */}
        <div className="absolute inset-y-0 right-0 pr-2 flex items-center gap-2">
          {/* Clear Button */}
          {searchQuery && (
            <button
              onClick={clearSearch}
              className="p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
              aria-label="Clear search"
              title="Clear search"
            >
              ×
            </button>
          )}
          
          {/* Voice Search Button */}
          <VoiceSearch onSearchResult={handleVoiceResult} />
        </div>
      </div>
      
      {/* Search Suggestions (if needed in future) */}
      {searchQuery && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-10 max-h-60 overflow-y-auto hidden">
          {/* Future: Search suggestions can go here */}
        </div>
      )}
    </div>
  )
}

export default SearchBar