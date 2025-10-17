import React, { useState, useEffect, useCallback } from 'react'
import { Tool } from '../lib/supabase'
import ToolCard from './ToolCard'
import LoadingSpinner from './LoadingSpinner'

interface InfiniteScrollProps {
  tools: Tool[]
  loading: boolean
  hasMore: boolean
  onLoadMore: () => void
  viewMode: 'grid' | 'list'
}

function InfiniteScroll({ tools, loading, hasMore, onLoadMore, viewMode }: InfiniteScrollProps) {
  const [page, setPage] = useState(1)
  const toolsPerPage = 20
  
  // Calculate total pages for display
  const totalPages = Math.ceil(tools.length / toolsPerPage)
  const currentPage = Math.ceil(tools.length / toolsPerPage)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          onLoadMore()
        }
      },
      { 
        threshold: 0.1,
        rootMargin: '100px' // Load more content 100px before reaching the bottom
      }
    )

    const target = document.querySelector('#scroll-trigger')
    if (target) {
      observer.observe(target)
    }

    return () => {
      if (target) {
        observer.unobserve(target)
      }
      observer.disconnect()
    }
  }, [hasMore, loading, onLoadMore])

  return (
    <>
      {/* Page Indicator */}
      {tools.length > 0 && (
        <div className="flex justify-center mb-6">
          <div className="bg-white dark:bg-gray-800 px-4 py-2 rounded-full shadow-sm border border-gray-200 dark:border-gray-700">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Showing {tools.length} tools
              {totalPages > 1 && (
                <span className="ml-2 px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-full text-xs font-medium">
                  Page {currentPage}
                </span>
              )}
            </span>
          </div>
        </div>
      )}

      {/* Tools Grid */}
      <div className={`
        ${viewMode === 'grid' 
          ? 'tools-grid-advanced' 
          : 'space-y-4'
        }
      `}>
        {tools.map((tool, index) => (
          <ToolCard 
            key={`${tool.id}-${index}`} 
            tool={tool} 
            viewMode={viewMode} 
          />
        ))}
      </div>

      {/* Infinite Scroll Trigger */}
      <div id="scroll-trigger" className="h-10" />

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center py-8">
          <div className="flex items-center gap-3">
            <LoadingSpinner />
            <span className="text-gray-600 dark:text-gray-400 font-medium">
              Loading more amazing AI tools...
            </span>
          </div>
        </div>
      )}

      {/* End of Results */}
      {!hasMore && tools.length > 0 && (
        <div className="text-center py-12">
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 rounded-full">
            <span className="text-purple-600 dark:text-purple-400 font-medium">
              🎉 You've discovered all {tools.length} AI tools!
            </span>
          </div>
          <p className="text-gray-500 dark:text-gray-400 mt-4 text-sm">
            Check back soon for new additions to our directory
          </p>
        </div>
      )}
    </>
  )
}

export default InfiniteScroll