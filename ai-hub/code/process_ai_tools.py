#!/usr/bin/env python3
"""
Process extracted AI tools data from multiple sources and combine into a single JSON file.
"""

import json
import os
from typing import List, Dict, Any

def load_extracted_data():
    """Load all extracted data files."""
    extracted_files = [
        '/workspace/extract/insidr_ai_tools.json',
        '/workspace/extract/aiscout_tools.json', 
        '/workspace/extract/geeksforgeeks_ai_directory.json',
        '/workspace/extract/perfectessaywriter_2025_tools.json',
        '/workspace/extract/meetcody_directories.json'
    ]
    
    data = {}
    for file_path in extracted_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                source_name = os.path.basename(file_path).replace('.json', '')
                data[source_name] = content
    
    return data

def process_insidr_tools(data):
    """Process tools from insidr.ai"""
    tools = []
    if 'features' in data:
        for tool in data['features']:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('url', ''),
                'source': 'insidr.ai',
                'category': 'General AI Tools'
            })
    return tools

def process_aiscout_tools(data):
    """Process tools from aiscout.net"""
    tools = []
    if 'extracted_information' in data and isinstance(data['extracted_information'], list):
        for tool in data['extracted_information']:
            tools.append({
                'name': tool.get('tool_name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'source': 'aiscout.net',
                'category': ', '.join(tool.get('categories', []))
            })
    return tools

def process_geeksforgeeks_tools(data):
    """Process tools from geeksforgeeks.org"""
    tools = []
    if 'ai_tools_and_directories' in data:
        for category in data['ai_tools_and_directories']:
            category_name = category.get('category_name', '')
            category_desc = category.get('description', '')
            
            # Add individual tools in the category
            for tool in category.get('tools', []):
                tool_name = tool.get('name', '')
                tool_desc = tool.get('description', category_desc)
                tool_link = tool.get('link', '')
                
                # Skip generic category references and focus on actual tools
                if tool_name and not tool_name.startswith('AI ') and not tool_name.startswith('Best '):
                    tools.append({
                        'name': tool_name,
                        'description': tool_desc,
                        'link': tool_link,
                        'source': 'geeksforgeeks.org',
                        'category': category_name
                    })
    return tools

def process_perfectessaywriter_tools(data):
    """Process tools from perfectessaywriter.ai"""
    tools = []
    if 'features' in data:
        for tool in data['features']:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'source': 'perfectessaywriter.ai',
                'category': tool.get('category', 'General AI Tools')
            })
    return tools

def process_meetcody_tools(data):
    """Process tools from meetcody.ai (these are mainly directories)"""
    tools = []
    if 'features' in data:
        for tool in data['features']:
            # Skip generic examples
            if tool.get('type') == 'AI Tool Directory':
                tools.append({
                    'name': tool.get('name', ''),
                    'description': tool.get('description', ''),
                    'link': tool.get('url', ''),
                    'source': 'meetcody.ai',
                    'category': 'AI Tool Directory'
                })
            elif tool.get('type') == 'Individual AI Tool' and tool.get('url'):
                tools.append({
                    'name': tool.get('name', ''),
                    'description': tool.get('description', ''),
                    'link': tool.get('url', ''),
                    'source': 'meetcody.ai',
                    'category': 'Individual AI Tool'
                })
    return tools

def main():
    """Main processing function"""
    print("Loading extracted data...")
    extracted_data = load_extracted_data()
    
    all_tools = []
    
    # Process each source
    for source_name, source_data in extracted_data.items():
        print(f"Processing {source_name}...")
        
        if source_name == 'insidr_ai_tools':
            tools = process_insidr_tools(source_data)
        elif source_name == 'aiscout_tools':
            tools = process_aiscout_tools(source_data)
        elif source_name == 'geeksforgeeks_ai_directory':
            tools = process_geeksforgeeks_tools(source_data)
        elif source_name == 'perfectessaywriter_2025_tools':
            tools = process_perfectessaywriter_tools(source_data)
        elif source_name == 'meetcody_directories':
            tools = process_meetcody_tools(source_data)
        else:
            tools = []
        
        all_tools.extend(tools)
        print(f"  Added {len(tools)} tools from {source_name}")
    
    # Remove duplicates based on name (case-insensitive)
    seen_names = set()
    unique_tools = []
    
    for tool in all_tools:
        name_lower = tool['name'].lower().strip()
        if name_lower and name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_tools.append(tool)
    
    # Sort by name
    unique_tools.sort(key=lambda x: x['name'].lower())
    
    # Create final output structure
    output = {
        'metadata': {
            'extraction_date': '2025-08-21',
            'total_tools': len(unique_tools),
            'sources': list(extracted_data.keys()),
            'description': 'AI tools extracted from blog and review sites focusing on tool names, descriptions, and links'
        },
        'tools': unique_tools
    }
    
    # Save to output file
    os.makedirs('/workspace/data', exist_ok=True)
    output_file = '/workspace/data/blog_review_tools.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing complete!")
    print(f"Total unique tools extracted: {len(unique_tools)}")
    print(f"Output saved to: {output_file}")
    
    # Print some statistics
    categories = {}
    sources = {}
    
    for tool in unique_tools:
        category = tool.get('category', 'Unknown')
        source = tool.get('source', 'Unknown')
        
        categories[category] = categories.get(category, 0) + 1
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\nTools by source:")
    for source, count in sorted(sources.items()):
        print(f"  {source}: {count}")
    
    print(f"\nTop categories:")
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories[:10]:
        print(f"  {category}: {count}")

if __name__ == "__main__":
    main()