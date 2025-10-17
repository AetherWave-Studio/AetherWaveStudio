import React from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import Sidebar from './Sidebar'
import DarkModeToggle from './DarkModeToggle'
import { useState } from 'react'

function Layout() {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      {/* Skip to main content link for accessibility */}
      <a href="#main-content" className="skip-link sr-only focus:not-sr-only">
        Skip to main content
      </a>
      
      {/* Enhanced Navigation Bar */}
      <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and mobile menu button */}
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Toggle sidebar"
              >
                {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
              <a 
                href="https://aetherwavestudio.com" 
                className="logo-link flex items-center ml-2 md:ml-0"
                aria-label="AIverse - Premium AI Tools Directory"
              >
                <img 
                  src="/aws-logo.png" 
                  alt="AetherWave Studio Ai Tools Directory" 
                  className="aiverse-logo"
                />
              </a>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <a
                href="https://aetherwavestudio.com"
                className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 text-sm font-medium transition-colors font-inter"
              >
                Home
              </a>
              <Link
                to="/about"
                className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 text-sm font-medium transition-colors font-inter"
              >
                About Us
              </Link>
              <a
                href="https://docs.google.com/forms/d/e/1FAIpQLSdnX3LsD5NU1_SMq79IRstx2XsZ-Dt76QlDi44R3OP98vDTwA/viewform?usp=header"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 text-sm font-medium transition-colors font-inter"
              >
                Submit Tool
              </a>
              
              {/* Dark Mode Toggle */}
              <DarkModeToggle />
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center space-x-2">
              <DarkModeToggle />
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Toggle menu"
              >
                <Menu className="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex">
        {/* Enhanced Sidebar */}
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        {/* Main Content */}
        <main id="main-content" className="flex-1 md:ml-64">
          <Outlet />
        </main>
      </div>

      {/* Mobile navigation menu overlay */}
      {userMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black bg-opacity-50" onClick={() => setUserMenuOpen(false)}>
          <div className="absolute top-16 right-4 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 border dark:border-gray-700">
            <a
              href="https://aetherwavestudio.com"
              className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 font-inter transition-colors"
              onClick={() => setUserMenuOpen(false)}
            >
              Home
            </a>
            <Link
              to="/about"
              className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 font-inter transition-colors"
              onClick={() => setUserMenuOpen(false)}
            >
              About Us
            </Link>
            <a
              href="https://docs.google.com/forms/d/e/1FAIpQLSdnX3LsD5NU1_SMq79IRstx2XsZ-Dt76QlDi44R3OP98vDTwA/viewform?usp=header"
              target="_blank"
              rel="noopener noreferrer"
              className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 font-inter transition-colors"
              onClick={() => setUserMenuOpen(false)}
            >
              Submit Tool
            </a>
          </div>
        </div>
      )}
    </div>
  )
}

export default Layout