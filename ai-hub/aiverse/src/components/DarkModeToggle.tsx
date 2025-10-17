import React, { useState, useEffect } from 'react'
import { Moon, Sun, Monitor } from 'lucide-react'
import HighContrastToggle from './HighContrastToggle'

type Theme = 'light' | 'dark' | 'system'

function DarkModeToggle() {
  const [theme, setTheme] = useState<Theme>('system')

  useEffect(() => {
    // Get saved theme preference or default to system
    const savedTheme = localStorage.getItem('theme') as Theme || 'system'
    setTheme(savedTheme)
    applyTheme(savedTheme)

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = () => {
      if (theme === 'system') {
        applyTheme('system')
      }
    }
    
    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [])

  const applyTheme = (newTheme: Theme) => {
    const root = window.document.documentElement
    
    if (newTheme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      root.setAttribute('data-theme', systemTheme)
      if (systemTheme === 'dark') {
        root.classList.add('dark')
      } else {
        root.classList.remove('dark')
      }
    } else {
      root.setAttribute('data-theme', newTheme)
      if (newTheme === 'dark') {
        root.classList.add('dark')
      } else {
        root.classList.remove('dark')
      }
    }
  }

  const handleThemeChange = (newTheme: Theme) => {
    setTheme(newTheme)
    localStorage.setItem('theme', newTheme)
    applyTheme(newTheme)
  }

  const getIcon = () => {
    switch (theme) {
      case 'light':
        return <Sun className="h-4 w-4" />
      case 'dark':
        return <Moon className="h-4 w-4" />
      case 'system':
        return <Monitor className="h-4 w-4" />
    }
  }

  const getNextTheme = (): Theme => {
    switch (theme) {
      case 'light':
        return 'dark'
      case 'dark':
        return 'system'
      case 'system':
        return 'light'
    }
  }

  const getThemeLabel = () => {
    switch (theme) {
      case 'light':
        return 'Light mode'
      case 'dark':
        return 'Dark mode'
      case 'system':
        return 'System mode'
    }
  }

  return (
    <div className="flex items-center gap-2">
      {/* Theme Toggle */}
      <button
        onClick={() => handleThemeChange(getNextTheme())}
        className="
          relative inline-flex items-center justify-center
          w-12 h-6 rounded-full
          transition-all duration-300 ease-in-out
          focus:outline-none focus:ring-3 focus:ring-purple-500 focus:ring-offset-2
          group hover:scale-105
        "
        aria-label={`Currently in ${getThemeLabel()}, click to switch to ${getNextTheme()} mode`}
        title={`Switch to ${getNextTheme()} mode`}
      >
        {/* Toggle background with gradient */}
        <span
          className={`
            absolute inset-0 rounded-full transition-all duration-300
            ${
              theme === 'dark'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg'
                : theme === 'light'
                ? 'bg-gradient-to-r from-yellow-400 to-orange-400 shadow-lg'
                : 'bg-gradient-to-r from-gray-400 to-gray-600 shadow-lg'
            }
          `}
        />
        
        {/* Toggle button */}
        <span
          className={`
            relative inline-block w-5 h-5 bg-white rounded-full shadow-lg
            transform transition-all duration-300 ease-in-out
            ${
              theme === 'dark'
                ? 'translate-x-6'
                : theme === 'light'
                ? 'translate-x-0.5'
                : 'translate-x-3'
            }
            flex items-center justify-center
            group-hover:scale-110
          `}
        >
          {getIcon()}
        </span>
      </button>
      
      {/* High Contrast Toggle */}
      <HighContrastToggle />
    </div>
  )
}

export default DarkModeToggle
