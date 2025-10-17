import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import LoadingSpinner from '../components/LoadingSpinner'
import { CheckCircle, XCircle } from 'lucide-react'

function AuthCallback() {
  const navigate = useNavigate()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    handleAuthCallback()
  }, [])

  async function handleAuthCallback() {
    try {
      // Get the hash fragment from the URL
      const hashFragment = window.location.hash

      if (hashFragment && hashFragment.length > 0) {
        // Exchange the auth code for a session
        const { data, error } = await supabase.auth.exchangeCodeForSession(hashFragment)

        if (error) {
          console.error('Error exchanging code for session:', error.message)
          setStatus('error')
          setMessage(error.message)
          
          // Redirect to login with error after delay
          setTimeout(() => {
            navigate('/login?error=' + encodeURIComponent(error.message))
          }, 3000)
          return
        }

        if (data.session) {
          setStatus('success')
          setMessage('Email verified successfully! Redirecting to dashboard...')
          
          // Successfully signed in, redirect to app
          setTimeout(() => {
            navigate('/')
          }, 2000)
          return
        }
      }

      // If we get here, something went wrong
      setStatus('error')
      setMessage('No session found or invalid callback')
      setTimeout(() => {
        navigate('/login?error=No session found')
      }, 3000)
    } catch (error: any) {
      console.error('Auth callback error:', error)
      setStatus('error')
      setMessage(error.message || 'Authentication failed')
      
      setTimeout(() => {
        navigate('/login?error=' + encodeURIComponent(error.message || 'Authentication failed'))
      }, 3000)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="text-center">
            {status === 'loading' && (
              <>
                <LoadingSpinner size="lg" text="Verifying your account..." />
              </>
            )}
            
            {status === 'success' && (
              <>
                <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
                <h2 className="text-2xl font-poppins font-bold text-gray-900 mb-4">
                  Email Verified!
                </h2>
                <p className="text-gray-600">{message}</p>
              </>
            )}
            
            {status === 'error' && (
              <>
                <XCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
                <h2 className="text-2xl font-poppins font-bold text-gray-900 mb-4">
                  Verification Failed
                </h2>
                <p className="text-gray-600 mb-4">{message}</p>
                <p className="text-sm text-gray-500">Redirecting to login page...</p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuthCallback