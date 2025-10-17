import React, { useState, useEffect } from 'react'
import { Link, useLocation, useSearchParams } from 'react-router-dom'
import { 
  Brain, 
  Zap, 
  MessageSquare, 
  Megaphone, 
  Palette, 
  Code, 
  GraduationCap, 
  Mail, 
  Share2, 
  BarChart3, 
  ShoppingCart, 
  Headphones, 
  PenTool, 
  Play,
  X
} from 'lucide-react'
import { supabase } from '../lib/supabase'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

interface Category {
  id: number
  name: string
  slug: string
  tools_count: number
  icon?: string
}

// Icon mapping for categories
const categoryIcons: Record<string, React.ReactNode> = {
  'artificial-intelligence': <Brain className="h-5 w-5" />,
  'productivity': <Zap className="h-5 w-5" />,
  'marketing': <Megaphone className="h-5 w-5" />,
  'developer-tools': <Code className="h-5 w-5" />,
  'design': <Palette className="h-5 w-5" />,
  'chatbots': <MessageSquare className="h-5 w-5" />,
  'social-media': <Share2 className="h-5 w-5" />,
  'content-creation': <PenTool className="h-5 w-5" />,
  'writing': <PenTool className="h-5 w-5" />,
  'customer-support': <Headphones className="h-5 w-5" />,
  'education': <GraduationCap className="h-5 w-5" />,
  'analytics': <BarChart3 className="h-5 w-5" />,
  'email': <Mail className="h-5 w-5" />,
  'video': <Play className="h-5 w-5" />,
  'sales': <ShoppingCart className="h-5 w-5" />
}

function Sidebar({ isOpen, onClose }: SidebarProps) {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const location = useLocation()
  const [searchParams] = useSearchParams()
  const currentCategory = searchParams.get('category')

  useEffect(() => {
    loadCategories()
  }, [])

  async function loadCategories() {
    try {
      const { data, error } = await supabase
        .from('categories')
        .select('*')
        .order('tools_count', { ascending: false })

      if (error) throw error
      setCategories(data || [])
    } catch (error) {
      console.error('Error loading categories:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="md:hidden fixed inset-0 z-40 bg-black bg-opacity-50"
          onClick={onClose}
        />
      )}

      {/* Enhanced Sidebar */}
      <div className={`
        fixed top-16 left-0 h-full w-64 z-50 transform transition-transform duration-300 ease-in-out custom-scrollbar overflow-y-auto
        bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        md:translate-x-0
      `}>
        <div className="p-4">
          {/* Close button for mobile */}
          <div className="md:hidden flex justify-between items-center mb-4">
            <h2 className="heading-md text-gray-900 dark:text-gray-100">Categories</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label="Close sidebar"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Desktop title */}
          <h2 className="hidden md:block heading-md text-gray-900 dark:text-gray-100 mb-4">Categories</h2>

          {/* All Tools Link */}
          <Link
            to="/"
            onClick={onClose}
            className={`
              flex items-center px-3 py-3 rounded-md text-sm font-medium transition-all mb-2 sidebar-category
              ${!currentCategory 
                ? 'bg-purple-50 text-purple-700 border-l-4 border-purple-600 dark:bg-purple-900/20 dark:text-purple-300' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700'
              }
            `}
          >
            <Brain className="h-5 w-5 mr-3" />
            <span className="flex-1">All Tools</span>
            <span className="ml-auto text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full font-inter dark:bg-gray-700 dark:text-gray-300">
              1000
            </span>
          </Link>

          {/* Categories List */}
          {loading ? (
            <div className="space-y-2">
              {[...Array(10)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-12 bg-gray-200 rounded-md dark:bg-gray-700"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-1">
              {categories.map((category) => (
                <Link
                  key={category.id}
                  to={`/?category=${category.slug}`}
                  onClick={onClose}
                  className={`
                    flex items-center px-3 py-3 rounded-md text-sm font-medium transition-all sidebar-category
                    ${currentCategory === category.slug
                      ? 'bg-purple-50 text-purple-700 border-l-4 border-purple-600 dark:bg-purple-900/20 dark:text-purple-300'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700'
                    }
                  `}
                >
                  <span className="mr-3">
                    {categoryIcons[category.slug] || <Brain className="h-5 w-5" />}
                  </span>
                  <span className="flex-1 truncate">{category.name}</span>
                  <span className="ml-2 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full font-inter dark:bg-gray-700 dark:text-gray-300">
                    {category.tools_count}
                  </span>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default Sidebar