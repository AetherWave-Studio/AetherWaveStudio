import React, { useState, useEffect } from 'react'
import { Bell, Sparkles, TrendingUp, Star } from 'lucide-react'

function RealTimeUpdates() {
  const [notifications, setNotifications] = useState<string[]>([])
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    // Simulate real-time updates
    const messages = [
      '🆕 New tool added: Claude AI Assistant - Advanced conversational AI',
      '🔥 Trending: Midjourney reaches 1M users this month',
      '⭐ ChatGPT updated with new image generation features',
      '🚀 Breaking: Google announces Gemini Pro upgrade',
      '💡 Featured: Notion AI gets advanced writing capabilities',
      '📈 Popular: Grammarly introduces voice writing assistant',
      '🎨 New: Adobe Firefly integrates with Creative Suite',
      '🤖 Update: GitHub Copilot adds new programming languages'
    ]
    
    // Add initial notification
    setTimeout(() => {
      setNotifications([messages[0]])
    }, 2000)

    // Add more notifications periodically
    const interval = setInterval(() => {
      setNotifications(prev => {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)]
        // Keep only the last 3 notifications
        const newNotifications = [...prev.slice(-2), randomMessage]
        return newNotifications
      })
    }, 15000) // Every 15 seconds

    return () => clearInterval(interval)
  }, [])

  if (!isVisible || notifications.length === 0) {
    return null
  }

  return (
    <div className="notification-banner">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell className="h-4 w-4 animate-pulse" />
          <div className="flex flex-col gap-1">
            {notifications.map((notification, index) => (
              <div key={`${notification}-${index}`} className="notification-item">
                {notification}
              </div>
            ))}
          </div>
        </div>
        <button
          onClick={() => setIsVisible(false)}
          className="text-white/80 hover:text-white transition-colors p-1"
          aria-label="Dismiss notifications"
        >
          ×
        </button>
      </div>
    </div>
  )
}

export default RealTimeUpdates