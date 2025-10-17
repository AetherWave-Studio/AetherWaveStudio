import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ncfqyasvfvrtpoaqfegl.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jZnF5YXN2ZnZydHBvYXFmZWdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3NDk5ODQsImV4cCI6MjA3MTMyNTk4NH0.BBrmj8rvbWCOtnxQOVrRgG_gGQvSPDhyVtIMuD5CjIo'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export interface Tool {
  id: number
  name: string
  description: string
  link: string
  category: string
  logo_url?: string
  screenshot_url?: string
  featured: boolean
  popularity_score: number
  source?: string
  created_at?: string
  updated_at?: string
  tags?: string[]
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  icon?: string
  tools_count: number
  created_at?: string
}

export interface UserProfile {
  id: string
  email?: string
  full_name?: string
  avatar_url?: string
  created_at?: string
  updated_at?: string
}

export interface UserSubmission {
  id: number
  user_id?: string
  name: string
  description: string
  link: string
  category: string
  logo_url?: string
  status: 'pending' | 'approved' | 'rejected'
  admin_notes?: string
  submitted_at?: string
  reviewed_at?: string
}

export interface UserFavorite {
  id: number
  user_id: string
  tool_id: number
  created_at?: string
}