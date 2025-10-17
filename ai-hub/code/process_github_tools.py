#!/usr/bin/env python3
"""
Complete AI Tools Data Processor
Processes the extracted GitHub repository data into the requested JSON format
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any

def load_extracted_data():
    """Load the extracted data from the JSON file"""
    try:
        with open('/workspace/extract/complete_github_tools_extraction.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading extracted data: {e}")
        return None

def process_free_version_status(status: str) -> str:
    """Convert emoji status to text description"""
    status_map = {
        "✅": "Yes",
        "❌": "No", 
        "❔": "Unknown"
    }
    return status_map.get(status, "Unknown")

def clean_description(description: str) -> str:
    """Clean and normalize description text"""
    if not description or description.strip() == "." or description.strip() == "":
        return "No description available"
    
    # Clean up extra whitespace and newlines
    cleaned = re.sub(r'\s+', ' ', description.strip())
    
    # Remove trailing periods if they appear to be artifacts
    if cleaned.endswith('.') and not cleaned.endswith('...'):
        cleaned = cleaned[:-1]
    
    return cleaned

def clean_url(url: str) -> str:
    """Clean and normalize URLs"""
    if not url:
        return ""
    
    # Ensure URLs have proper protocol
    if url.startswith('http://') or url.startswith('https://'):
        return url
    elif url.startswith('//'):
        return f"https:{url}"
    else:
        return f"https://{url}"

def process_tools_data(extracted_data: Dict) -> List[Dict[str, Any]]:
    """Process the extracted tools data into the requested format"""
    tools_list = []
    
    # Navigate to the ai_tools data
    ai_tools_data = extracted_data.get('results', {}).get('https://github.com/yousefebrahimi0/1000-AI-collection-tools', {}).get('content', {}).get('raw_content', '')
    
    if isinstance(ai_tools_data, str):
        # Parse the JSON string
        try:
            parsed_data = json.loads(ai_tools_data)
            ai_tools_categories = parsed_data.get('data', {}).get('extracted_information', {}).get('ai_tools', [])
        except:
            return tools_list
    else:
        ai_tools_categories = ai_tools_data.get('data', {}).get('extracted_information', {}).get('ai_tools', [])
    
    for category_data in ai_tools_categories:
        category_name = category_data.get('category', 'Uncategorized')
        tools = category_data.get('tools', [])
        
        for tool in tools:
            processed_tool = {
                "name": tool.get('name', '').strip(),
                "title": tool.get('title', '').strip(),
                "description": clean_description(tool.get('description', '')),
                "link": clean_url(tool.get('link', '')),
                "category": category_name,
                "free_version": process_free_version_status(tool.get('free_version_status', '❔')),
                "source": "https://github.com/yousefebrahimi0/1000-AI-collection-tools"
            }
            
            # Only add tools with valid names and links
            if processed_tool["name"] and processed_tool["link"]:
                tools_list.append(processed_tool)
    
    return tools_list

def create_comprehensive_dataset():
    """Create the comprehensive AI tools dataset"""
    print("Loading extracted data...")
    extracted_data = load_extracted_data()
    
    if not extracted_data:
        print("Failed to load extracted data")
        return
    
    print("Processing tools data...")
    tools_list = process_tools_data(extracted_data)
    
    print(f"Processed {len(tools_list)} tools from the GitHub repository")
    
    # Create comprehensive dataset structure
    dataset = {
        "metadata": {
            "source_repository": "https://github.com/yousefebrahimi0/1000-AI-collection-tools",
            "description": "Complete collection of 1000+ AI tools extracted from the GitHub repository",
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "extraction_method": "comprehensive_parsing",
            "total_tools": len(tools_list),
            "data_format": "Complete extraction with structured parsing of repository content"
        },
        "tools": tools_list
    }
    
    # Generate category statistics
    category_stats = {}
    for tool in tools_list:
        category = tool["category"]
        category_stats[category] = category_stats.get(category, 0) + 1
    
    dataset["metadata"]["categories"] = list(category_stats.keys())
    dataset["metadata"]["category_distribution"] = category_stats
    dataset["metadata"]["total_categories"] = len(category_stats)
    
    # Save the dataset
    output_file = '/workspace/data/primary_github_tools.json'
    print(f"Saving comprehensive dataset to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully created comprehensive dataset!")
    print(f"📊 Total tools: {len(tools_list)}")
    print(f"📂 Total categories: {len(category_stats)}")
    print(f"🔗 Source: https://github.com/yousefebrahimi0/1000-AI-collection-tools")
    
    # Display top categories
    print("\n📈 Top 10 categories by tool count:")
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    for i, (category, count) in enumerate(sorted_categories[:10], 1):
        print(f"   {i:2d}. {category}: {count} tools")
    
    return dataset

if __name__ == "__main__":
    create_comprehensive_dataset()
