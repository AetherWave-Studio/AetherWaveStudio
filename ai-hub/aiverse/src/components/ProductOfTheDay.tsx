import React, { useState, useEffect } from 'react'
import { Award, Star, ExternalLink } from 'lucide-react'
import { supabase, Tool } from '../lib/supabase'
import { openToolLink } from '../utils/affiliateLinks'

function ProductOfTheDay() {
  const [productOfTheDay, setProductOfTheDay] = useState<Tool | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProductOfTheDay()
  }, [])

  async function loadProductOfTheDay() {
    try {
      // Get a featured tool with high popularity score
      const { data, error } = await supabase
        .from('tools')
        .select('*')
        .eq('featured', true)
        .gte('popularity_score', 6.0)
        .order('popularity_score', { ascending: false })
        .limit(1)
        .maybeSingle()

      if (error) throw error
      setProductOfTheDay(data)
    } catch (error) {
      console.error('Error loading product of the day:', error)
      // Fallback: get any tool
      try {
        const { data, error } = await supabase
          .from('tools')
          .select('*')
          .order('popularity_score', { ascending: false })
          .limit(1)
          .maybeSingle()

        if (!error && data) {
          setProductOfTheDay(data)
        }
      } catch (fallbackError) {
        console.error('Error loading fallback product:', fallbackError)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleVisitTool = () => {
    if (productOfTheDay) {
      openToolLink(productOfTheDay.link)
    }
  }

  if (loading) {
    return (
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
        <div className="animate-pulse">
          <div className="flex items-center mb-4">
            <div className="w-6 h-6 bg-white/20 rounded mr-2"></div>
            <div className="w-32 h-6 bg-white/20 rounded"></div>
          </div>
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div className="flex-1">
              <div className="w-48 h-8 bg-white/20 rounded mb-4"></div>
              <div className="w-full h-4 bg-white/20 rounded mb-2"></div>
              <div className="w-3/4 h-4 bg-white/20 rounded mb-4"></div>
            </div>
            <div className="w-32 h-12 bg-white/20 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!productOfTheDay) {
    return null
  }

  return (
    <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute -top-4 -right-4 w-24 h-24 bg-white rounded-full"></div>
        <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-white rounded-full"></div>
      </div>

      <div className="relative">
        {/* Header */}
        <div className="flex items-center mb-6">
          <Award className="h-6 w-6 text-yellow-300 mr-2" />
          <h2 className="text-xl font-poppins font-bold">Product of the Day</h2>
        </div>

        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          {/* Content */}
          <div className="flex-1 lg:mr-8">
            <div className="flex items-center mb-4">
              {/* Logo */}
              {productOfTheDay.logo_url ? (
                <img
                  src={productOfTheDay.logo_url}
                  alt={`${productOfTheDay.name} logo`}
                  className="w-12 h-12 object-cover rounded-xl bg-white/10 mr-4"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                  }}
                />
              ) : (
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-white font-poppins font-bold text-xl mr-4">
                  {productOfTheDay.name.charAt(0).toUpperCase()}
                </div>
              )}
              
              <div>
                <h3 className="text-2xl font-poppins font-bold mb-1">
                  {productOfTheDay.name}
                </h3>
                <div className="flex items-center space-x-3">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white/20 text-white">
                    {productOfTheDay.category}
                  </span>
                  <div className="flex items-center text-sm">
                    <Star className="h-4 w-4 text-yellow-300 fill-current mr-1" />
                    <span>{productOfTheDay.popularity_score || 0}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <p className="text-white/90 text-lg leading-relaxed mb-6 lg:mb-0">
              {productOfTheDay.description}
            </p>
          </div>

          {/* CTA Button */}
          <div className="flex-shrink-0">
            <button
              onClick={handleVisitTool}
              className="inline-flex items-center px-6 py-3 bg-white text-purple-600 font-poppins font-semibold rounded-xl hover:bg-white/90 transition-colors group"
            >
              Explore Now
              <ExternalLink className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductOfTheDay