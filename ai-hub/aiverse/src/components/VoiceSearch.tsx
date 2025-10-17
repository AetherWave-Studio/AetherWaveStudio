import React, { useState } from 'react'
import { Mic, MicOff } from 'lucide-react'

interface VoiceSearchProps {
  onSearchResult: (result: string) => void
}

function VoiceSearch({ onSearchResult }: VoiceSearchProps) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isSupported, setIsSupported] = useState(true)

  const startVoiceSearch = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setIsSupported(false)
      alert('Voice search is not supported in your browser. Please use Chrome, Safari, or Edge.')
      return
    }

    const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition
    const recognition = new SpeechRecognition()
    
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'en-US'

    recognition.onstart = () => {
      setIsListening(true)
      setTranscript('')
    }

    recognition.onend = () => {
      setIsListening(false)
    }
    
    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript
      setTranscript(speechResult)
      onSearchResult(speechResult)
      setIsListening(false)
    }

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      setIsListening(false)
      if (event.error === 'not-allowed') {
        alert('Microphone access denied. Please allow microphone access and try again.')
      }
    }

    recognition.start()
  }

  if (!isSupported) {
    return null
  }

  return (
    <div className="relative">
      <button 
        className={`voice-search-btn ${isListening ? 'listening' : ''}`}
        onClick={startVoiceSearch}
        disabled={isListening}
        aria-label={isListening ? 'Listening for voice input...' : 'Start voice search'}
        title={isListening ? 'Listening...' : 'Voice search'}
      >
        {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
        {isListening && <div className="pulse-animation" />}
      </button>
      
      {transcript && (
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 p-2 bg-gray-800 text-white text-sm rounded whitespace-nowrap z-10">
          "{transcript}"
        </div>
      )}
    </div>
  )
}

// Add type declarations for SpeechRecognition
declare global {
  interface Window {
    webkitSpeechRecognition: any
    SpeechRecognition: any
  }
}

export default VoiceSearch