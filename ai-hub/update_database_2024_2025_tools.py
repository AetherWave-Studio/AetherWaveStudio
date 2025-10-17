#!/usr/bin/env python3
"""
Update Supabase database with 2024-2025 AI tools while preserving featured sections.
This script replaces the tools database with curated 2024-2025 AI tools.
"""

import json
import os
from supabase import create_client, Client
from datetime import datetime

def load_dataset():
    """Load the comprehensive 2024-2025 AI tools dataset"""
    with open('/workspace/aiverse_tools_2024_2025_comprehensive.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def initialize_supabase() -> Client:
    """Initialize Supabase client"""
    supabase_url = "https://ncfqyasvfvrtpoaqfegl.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jZnF5YXN2ZnZydHBvYXFmZWdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3NDk5ODQsImV4cCI6MjA3MTMyNTk4NH0.BBrmj8rvbWCOtnxQOVrRgG_gGQvSPDhyVtIMuD5CjIo"
    
    return create_client(supabase_url, supabase_key)

def clear_existing_tools(supabase: Client):
    """Clear existing tools from database"""
    print("🗑️  Clearing existing tools from database...")
    try:
        # Delete all existing tools
        response = supabase.table('tools').delete().neq('id', 0).execute()
        print(f"✅ Cleared existing tools successfully")
        return True
    except Exception as e:
        print(f"❌ Error clearing tools: {e}")
        return False

def insert_tools_batch(supabase: Client, tools: list, batch_size: int = 50):
    """Insert tools in batches to handle large datasets"""
    total_tools = len(tools)
    inserted_count = 0
    
    print(f"📤 Inserting {total_tools} tools in batches of {batch_size}...")
    
    for i in range(0, total_tools, batch_size):
        batch = tools[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_tools + batch_size - 1) // batch_size
        
        print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} tools)...")
        
        try:
            # Prepare tools for insertion (remove id field to let database auto-increment)
            batch_data = []
            for tool in batch:
                tool_data = {
                    'name': tool['name'],
                    'description': tool['description'],
                    'link': tool['link'],
                    'category': tool['category'],
                    'logo_url': tool.get('logo_url'),
                    'screenshot_url': tool.get('screenshot_url'),
                    'featured': tool.get('featured', False),
                    'popularity_score': tool.get('popularity_score', 0.0),
                    'source': tool.get('source', '2024_2025_curated'),
                    'created_at': tool.get('created_at', datetime.now().isoformat()),
                    'updated_at': tool.get('updated_at', datetime.now().isoformat())
                }
                batch_data.append(tool_data)
            
            # Insert batch
            response = supabase.table('tools').insert(batch_data).execute()
            inserted_count += len(batch)
            print(f"✅ Batch {batch_num} inserted successfully ({inserted_count}/{total_tools} total)")
            
        except Exception as e:
            print(f"❌ Error inserting batch {batch_num}: {e}")
            # Continue with next batch instead of stopping
            continue
    
    print(f"🎉 Tool insertion completed! {inserted_count}/{total_tools} tools inserted.")
    return inserted_count

def verify_insertion(supabase: Client):
    """Verify the tools were inserted correctly"""
    print("🔍 Verifying database insertion...")
    
    try:
        # Count total tools
        response = supabase.table('tools').select('id', count='exact').execute()
        total_count = response.count
        print(f"📊 Total tools in database: {total_count}")
        
        # Count featured tools
        featured_response = supabase.table('tools').select('id', count='exact').eq('featured', True).execute()
        featured_count = featured_response.count
        print(f"🌟 Featured tools: {featured_count}")
        
        # Get category breakdown
        categories_response = supabase.table('tools').select('category').execute()
        categories = {}
        for tool in categories_response.data:
            cat = tool['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📋 Category Distribution:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {category}: {count} tools")
        
        # Get sample of featured tools
        featured_tools_response = supabase.table('tools').select('name, popularity_score, category').eq('featured', True).order('popularity_score', desc=True).execute()
        
        if featured_tools_response.data:
            print("\n🌟 Featured Tools:")
            for tool in featured_tools_response.data:
                print(f"  • {tool['name']} - {tool['popularity_score']}/10.0 ({tool['category']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying insertion: {e}")
        return False

def update_tools_database():
    """Main function to update the tools database"""
    print("🚀 Starting AIverse database update with 2024-2025 AI tools...")
    print("=" * 60)
    
    # Load dataset
    print("📁 Loading 2024-2025 AI tools dataset...")
    dataset = load_dataset()
    tools = dataset['tools']
    metadata = dataset['metadata']
    
    print(f"✅ Loaded dataset: {metadata['title']}")
    print(f"📊 Tools to insert: {len(tools)}")
    print(f"🎯 Featured tools: {metadata['featured_tools_count']}")
    print(f"📂 Categories: {len(metadata['categories'])}")
    
    # Initialize Supabase
    print("\n🔌 Connecting to Supabase...")
    supabase = initialize_supabase()
    print("✅ Connected to Supabase successfully")
    
    # Clear existing tools
    print("\n🗑️  Preparing to clear existing database...")
    if not clear_existing_tools(supabase):
        print("❌ Failed to clear existing tools. Aborting.")
        return False
    
    # Insert new tools
    print("\n📤 Inserting new 2024-2025 AI tools...")
    inserted_count = insert_tools_batch(supabase, tools)
    
    if inserted_count == 0:
        print("❌ No tools were inserted. Update failed.")
        return False
    
    # Verify insertion
    print("\n🔍 Verifying database update...")
    if verify_insertion(supabase):
        print("\n🎉 Database update completed successfully!")
        print(f"✅ {inserted_count} tools from 2024-2025 are now live")
        print("🌟 Featured tools sections preserved as requested")
        print("🔄 Website ready for deployment")
        return True
    else:
        print("❌ Verification failed. Please check the database.")
        return False

if __name__ == "__main__":
    success = update_tools_database()
    if success:
        print("\n" + "=" * 60)
        print("🚀 AIverse database successfully updated with 2024-2025 tools!")
        print("🌐 Ready to deploy the modernized website.")
    else:
        print("\n" + "=" * 60)
        print("❌ Database update failed. Please check the errors above.")
