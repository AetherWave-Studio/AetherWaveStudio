import json
import requests

# Supabase configuration
SUPABASE_URL = "https://ncfqyasvfvrtpoaqfegl.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jZnF5YXN2ZnZydHBvYXFmZWdsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTc0OTk4NCwiZXhwIjoyMDcxMzI1OTg0fQ.gI93xKPdJ6L8HsW0s0m0v2kHUF7UQs4RgdF8VJgSHc8"  # This is a placeholder - we need the actual service role key

# Read tools data
with open('tools_for_insertion.json', 'r') as f:
    tools = json.load(f)

print(f"Inserting {len(tools)} tools via API...")

# Process in smaller batches of 50 tools
batch_size = 50
total_batches = (len(tools) + batch_size - 1) // batch_size
inserted_count = 0

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(tools))
    batch_tools = tools[start_idx:end_idx]
    
    # Prepare data for API insertion
    api_data = []
    for tool in batch_tools:
        tool_data = {
            'name': tool['name'],
            'description': tool['description'],
            'link': tool['link'],
            'category': tool['category'],
            'logo_url': tool.get('logo_url'),
            'screenshot_url': tool.get('screenshot_url'),
            'featured': tool.get('featured', False),
            'popularity_score': tool.get('popularity_score', 0.0),
            'source': tool.get('source')
        }
        api_data.append(tool_data)
    
    # Insert via Supabase REST API
    headers = {
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'apikey': SUPABASE_SERVICE_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            f'{SUPABASE_URL}/rest/v1/tools',
            headers=headers,
            json=api_data
        )
        
        if response.status_code == 201:
            inserted_count += len(batch_tools)
            print(f"Batch {batch_num + 1}/{total_batches}: Inserted {len(batch_tools)} tools (Total: {inserted_count})")
        else:
            print(f"Batch {batch_num + 1} failed: {response.status_code} - {response.text}")
            break
            
    except Exception as e:
        print(f"Error inserting batch {batch_num + 1}: {e}")
        break

print(f"Total tools inserted: {inserted_count}")
