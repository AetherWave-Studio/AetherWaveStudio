#!/usr/bin/env python3
"""
Script to process AI tools data from multiple directory websites and create a unified dataset.
"""

import json
import os
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import re

def clean_url(url: str, source_domain: str = None) -> str:
    """Clean and normalize URLs"""
    if not url:
        return ""
    
    # Handle relative URLs
    if url.startswith('/') and source_domain:
        return urljoin(f"https://{source_domain}", url)
    
    # Handle URLs that don't start with http/https
    if not url.startswith(('http://', 'https://')):
        if '.' in url:
            return f"https://{url}"
        elif source_domain:
            return urljoin(f"https://{source_domain}", url)
    
    return url

def clean_description(description: str) -> str:
    """Clean and truncate descriptions to one line"""
    if not description or description == "null":
        return ""
    
    # Remove extra whitespace and newlines
    description = re.sub(r'\s+', ' ', description.strip())
    
    # Truncate if too long (keep to ~150 characters for readability)
    if len(description) > 150:
        description = description[:147] + "..."
    
    return description

def normalize_categories(categories: List[str]) -> List[str]:
    """Normalize and clean category names"""
    if not categories:
        return []
    
    normalized = []
    for cat in categories:
        if cat and cat.strip():
            # Clean up category names
            cat = cat.strip().title()
            # Normalize common variations
            cat_mapping = {
                'Chatbots & Virtual Companions': 'AI Chatbots',
                'Image Generation & Editing': 'Image Generation',
                'Art & Creative Design': 'Design & Art',
                'Writing & Editing': 'Writing Tools',
                'Office & Productivity': 'Productivity',
                'Coding & Development': 'Development Tools',
                'Research & Data Analysis': 'Data Analysis',
                'Video Generation': 'Video Tools',
                'Social Media': 'Social Media Tools',
                'Ai Executive Assistants': 'AI Assistants',
                'Ai Agents': 'AI Agents',
                'Mental Health': 'Health & Wellness'
            }
            normalized.append(cat_mapping.get(cat, cat))
    
    return list(set(normalized))  # Remove duplicates

def extract_actual_url(url: str) -> str:
    """Extract actual website URL from directory tool pages"""
    # These are internal directory URLs, we need the actual tool website
    # For now, we'll keep them as they may contain useful redirects
    return url

def process_topai_tools(file_path: str) -> List[Dict[str, Any]]:
    """Process data from topai.tools"""
    print("Processing TopAI.tools data...")
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        extracted_info = data.get('extracted_information', [])
        for tool in extracted_info:
            if tool.get('tool_name'):
                tools.append({
                    'name': tool['tool_name'],
                    'description': clean_description(tool.get('description', '')),
                    'website': extract_actual_url(tool.get('official_website_url', '')),
                    'category': normalize_categories(tool.get('category_classifications', [])),
                    'source': 'topai.tools'
                })
        
        print(f"Extracted {len(tools)} tools from TopAI.tools")
        return tools
        
    except Exception as e:
        print(f"Error processing TopAI.tools: {e}")
        return []

def process_aitools_fyi(file_path: str) -> List[Dict[str, Any]]:
    """Process data from aitools.fyi"""
    print("Processing AITools.fyi data...")
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        extracted_info = data.get('extracted_information', [])
        for tool in extracted_info:
            if tool.get('tool_name'):
                tools.append({
                    'name': tool['tool_name'],
                    'description': clean_description(tool.get('description', '')),
                    'website': extract_actual_url(tool.get('website_link', '')),
                    'category': normalize_categories(tool.get('category_tags', [])),
                    'source': 'aitools.fyi'
                })
        
        print(f"Extracted {len(tools)} tools from AITools.fyi")
        return tools
        
    except Exception as e:
        print(f"Error processing AITools.fyi: {e}")
        return []

def process_toolify_ai(file_path: str) -> List[Dict[str, Any]]:
    """Process data from toolify.ai"""
    print("Processing Toolify.ai data...")
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the nested JSON structure
        data = json.loads(content)
        if 'raw_content' in data:
            nested_data = json.loads(data['raw_content'])
            extracted_info = nested_data.get('data', {}).get('extracted_information', [])
        else:
            extracted_info = data.get('extracted_information', [])
        
        for tool in extracted_info:
            if tool.get('tool_name'):
                tools.append({
                    'name': tool['tool_name'],
                    'description': clean_description(tool.get('description', '')),
                    'website': extract_actual_url(tool.get('website_url', '')),
                    'category': normalize_categories(tool.get('categories', [])),
                    'source': 'toolify.ai'
                })
        
        print(f"Extracted {len(tools)} tools from Toolify.ai")
        return tools
        
    except Exception as e:
        print(f"Error processing Toolify.ai: {e}")
        return []

def process_theresanaiforthat(file_path: str) -> List[Dict[str, Any]]:
    """Process data from theresanaiforthat.com"""
    print("Processing TheresAnAIForThat.com data...")
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the nested JSON structure
        data = json.loads(content)
        if 'raw_content' in data:
            nested_data = json.loads(data['raw_content'])
            extracted_info = nested_data.get('data', {}).get('extracted_information', [])
        else:
            extracted_info = data.get('extracted_information', [])
        
        for tool in extracted_info:
            if tool.get('name'):
                tools.append({
                    'name': tool['name'],
                    'description': clean_description(tool.get('description', '')),
                    'website': extract_actual_url(tool.get('website_url', '')),
                    'category': normalize_categories(tool.get('categories', [])),
                    'source': 'theresanaiforthat.com'
                })
        
        print(f"Extracted {len(tools)} tools from TheresAnAIForThat.com")
        return tools
        
    except Exception as e:
        print(f"Error processing TheresAnAIForThat.com: {e}")
        return []

def remove_duplicates(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate tools based on name similarity"""
    seen_names = set()
    unique_tools = []
    
    for tool in tools:
        # Normalize name for comparison
        normalized_name = tool['name'].lower().replace(' ', '').replace('-', '').replace('_', '')
        
        if normalized_name not in seen_names:
            seen_names.add(normalized_name)
            unique_tools.append(tool)
        else:
            print(f"Removing duplicate: {tool['name']} from {tool['source']}")
    
    return unique_tools

def ensure_category_diversity(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ensure diverse representation across categories"""
    category_counts = {}
    for tool in tools:
        for cat in tool['category']:
            category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} tools")
    
    return tools

def main():
    """Main processing function"""
    print("Starting AI Tools Data Processing...")
    
    # Create data directory if it doesn't exist
    os.makedirs('/workspace/data', exist_ok=True)
    
    all_tools = []
    
    # Process each source
    extract_dir = '/workspace/extract'
    
    # TopAI Tools
    topai_file = os.path.join(extract_dir, 'topai_tools_extraction.json')
    if os.path.exists(topai_file):
        all_tools.extend(process_topai_tools(topai_file))
    
    # AITools.fyi
    aitools_file = os.path.join(extract_dir, 'aitools_fyi_extraction.json')
    if os.path.exists(aitools_file):
        all_tools.extend(process_aitools_fyi(aitools_file))
    
    # Toolify.ai
    toolify_file = os.path.join(extract_dir, 'toolify_ai_extraction.json')
    if os.path.exists(toolify_file):
        all_tools.extend(process_toolify_ai(toolify_file))
    
    # TheresAnAIForThat.com
    theresanai_file = os.path.join(extract_dir, 'theresanaiforthat_extraction.json')
    if os.path.exists(theresanai_file):
        all_tools.extend(process_theresanaiforthat(theresanai_file))
    
    print(f"\nTotal tools collected: {len(all_tools)}")
    
    # Remove duplicates
    unique_tools = remove_duplicates(all_tools)
    print(f"Unique tools after deduplication: {len(unique_tools)}")
    
    # Ensure category diversity
    final_tools = ensure_category_diversity(unique_tools)
    
    # Create final dataset
    final_dataset = {
        'metadata': {
            'total_tools': len(final_tools),
            'sources': ['topai.tools', 'aitools.fyi', 'toolify.ai', 'theresanaiforthat.com'],
            'collection_date': '2025-08-21',
            'description': 'AI tools collected from major AI tool directory websites'
        },
        'tools': final_tools
    }
    
    # Save to JSON file
    output_file = '/workspace/data/directory_sites_tools.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\nDataset saved to: {output_file}")
    print(f"Final dataset contains {len(final_tools)} unique AI tools")
    
    # Print summary by source
    source_counts = {}
    for tool in final_tools:
        source = tool['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print("\nTools by source:")
    for source, count in source_counts.items():
        print(f"  {source}: {count} tools")

if __name__ == "__main__":
    main()
