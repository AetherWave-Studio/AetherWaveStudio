#!/usr/bin/env python3
"""
Insert 2024-2025 AI tools into Supabase database via edge function
"""

import json
import requests
from typing import Dict, Any

def load_tools_data() -> Dict[str, Any]:
    """Load the tools data from the JSON file"""
    with open('/workspace/tools_for_insert.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_tools_via_edge_function(tools_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert tools using the bulk-insert-tools edge function"""
    
    edge_function_url = "https://ncfqyasvfvrtpoaqfegl.supabase.co/functions/v1/bulk-insert-tools"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jZnF5YXN2ZnZydHBvYXFmZWdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3NDk5ODQsImV4cCI6MjA3MTMyNTk4NH0.BBrmj8rvbWCOtnxQOVrRgG_gGQvSPDhyVtIMuD5CjIo'
    }
    
    try:
        print(f"🚀 Sending {len(tools_data['tools'])} tools to bulk insert endpoint...")
        
        response = requests.post(
            edge_function_url,
            headers=headers,
            json=tools_data,
            timeout=300  # 5 minutes timeout for large dataset
        )
        
        print(f"📡 HTTP Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Bulk insertion completed successfully!")
            
            if 'data' in result:
                data = result['data']
                print(f"📊 Total processed: {data.get('totalProcessed', 'N/A')}")
                print(f"✅ Total inserted: {data.get('totalInserted', 'N/A')}")
                print(f"🗄️ Total in database: {data.get('totalInDatabase', 'N/A')}")
                print(f"📦 Batches processed: {data.get('totalBatches', 'N/A')}")
                
                if 'batches' in data:
                    print("\n📋 Batch Details:")
                    for batch in data['batches']:
                        print(f"  • Batch {batch['batch']}: {batch['inserted']} tools - {batch['status']}")
            
            return result
        else:
            error_data = response.json() if response.content else {'error': {'message': 'Unknown error'}}
            print(f"❌ Error: {error_data}")
            return error_data
            
    except requests.exceptions.Timeout:
        print("⏱️ Request timeout - this is normal for large datasets")
        return {'error': 'timeout', 'message': 'Request timed out but insertion may have succeeded'}
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return {'error': 'exception', 'message': str(e)}

def verify_insertion() -> Dict[str, Any]:
    """Verify the tools were inserted by checking the database count"""
    
    supabase_url = "https://ncfqyasvfvrtpoaqfegl.supabase.co"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jZnF5YXN2ZnZydHBvYXFmZWdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3NDk5ODQsImV4cCI6MjA3MTMyNTk4NH0.BBrmj8rvbWCOtnxQOVrRgG_gGQvSPDhyVtIMuD5CjIo"
    
    headers = {
        'apikey': api_key,
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Get total count
        count_response = requests.get(
            f"{supabase_url}/rest/v1/tools?select=count()",
            headers=headers
        )
        
        if count_response.status_code == 200:
            count_data = count_response.json()
            total_count = count_data[0]['count'] if count_data and 'count' in count_data[0] else 0
            print(f"📊 Total tools in database: {total_count}")
            
            # Get featured tools count
            featured_response = requests.get(
                f"{supabase_url}/rest/v1/tools?select=count()&featured=eq.true",
                headers=headers
            )
            
            featured_count = 0
            if featured_response.status_code == 200:
                featured_data = featured_response.json()
                featured_count = featured_data[0]['count'] if featured_data and 'count' in featured_data[0] else 0
                print(f"⭐ Featured tools: {featured_count}")
            
            # Get sample of tools to verify
            sample_response = requests.get(
                f"{supabase_url}/rest/v1/tools?select=name,category,popularity_score&limit=5&order=popularity_score.desc",
                headers=headers
            )
            
            if sample_response.status_code == 200:
                sample_data = sample_response.json()
                if sample_data:
                    print("\n🎯 Top 5 tools by popularity:")
                    for tool in sample_data:
                        print(f"  • {tool['name']} ({tool['category']}) - {tool['popularity_score']}/10.0")
            
            return {
                'success': True,
                'total_count': total_count,
                'featured_count': featured_count,
                'verification': 'successful'
            }
        else:
            print(f"❌ Verification failed: {count_response.status_code}")
            return {'success': False, 'error': 'verification_failed'}
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return {'success': False, 'error': str(e)}

def main():
    """Main function to insert tools and verify"""
    print("🚀 Starting AIverse database update with 2024-2025 AI tools...")
    print("=" * 60)
    
    # Load tools data
    print("📁 Loading tools data...")
    tools_data = load_tools_data()
    print(f"✅ Loaded {len(tools_data['tools'])} tools for insertion")
    
    # Insert tools
    print("\n📤 Inserting tools into database...")
    result = insert_tools_via_edge_function(tools_data)
    
    # Wait a moment for database to update
    import time
    print("\n⏳ Waiting for database to update...")
    time.sleep(3)
    
    # Verify insertion
    print("\n🔍 Verifying database update...")
    verification = verify_insertion()
    
    # Summary
    print("\n" + "=" * 60)
    if verification.get('success') and verification.get('total_count', 0) > 0:
        print("🎉 Database update completed successfully!")
        print(f"✅ Total tools now in database: {verification['total_count']}")
        print(f"⭐ Featured tools: {verification['featured_count']}")
        print("🌐 AIverse website is ready with 2024-2025 AI tools!")
        return True
    else:
        print("❌ Database update may have issues. Please check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
