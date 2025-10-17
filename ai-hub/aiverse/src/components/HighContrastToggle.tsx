import React, { useState, useEffect } from 'react'
import { Contrast } from 'lucide-react'

function HighContrastToggle() {
  const [highContrast, setHighContrast] = useState(false)

  useEffect(() => {
    // Check for saved high contrast preference or system preference
    const savedContrast = localStorage.getItem('highContrast')
    if (savedContrast) {
      const isHighContrast = savedContrast === 'true'
      setHighContrast(isHighContrast)
      updateHighContrast(isHighContrast)
    }
  }, [])

  const updateHighContrast = (isHighContrast: boolean) => {
    const root = window.document.documentElement
    if (isHighContrast) {
      root.setAttribute('data-contrast', 'high')
    } else {
      root.removeAttribute('data-contrast')
    }
  }

  const toggleHighContrast = () => {
    const newHighContrast = !highContrast
    setHighContrast(newHighContrast)
    localStorage.setItem('highContrast', newHighContrast.toString())
    updateHighContrast(newHighContrast)
  }

  return (
    <button
      onClick={toggleHighContrast}
      className={`
        p-2 rounded-lg transition-all duration-300 ease-in-out
        ${
          highContrast
            ? 'bg-white text-black border-2 border-black'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
        }
        focus:outline-none focus:ring-3 focus:ring-purple-500 focus:ring-offset-2
      `}
      title={highContrast ? 'Disable high contrast' : 'Enable high contrast'}
      aria-label={highContrast ? 'Disable high contrast mode' : 'Enable high contrast mode'}
      aria-pressed={highContrast}
    >
      <Contrast className="h-5 w-5" />
      <span className="sr-only">
        {highContrast ? 'Disable' : 'Enable'} high contrast mode
      </span>
    </button>
  )
}

export default HighContrastToggle