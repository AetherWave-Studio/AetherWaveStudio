#!/usr/bin/env python3
"""
Parse extracted AI tools from GitHub repositories and create a consolidated JSON file.
"""

import json
import os
from typing import List, Dict, Any

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def extract_tools_from_mahseema(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from mahseema/awesome-ai-tools repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        extracted_info = raw_content.get('data', {}).get('extracted_information_details', [])
        
        for category_data in extracted_info:
            category = category_data.get('category', 'Unknown')
            category_tools = category_data.get('tools', [])
            
            for tool in category_tools:
                tools.append({
                    'name': tool.get('name', ''),
                    'description': tool.get('description', ''),
                    'link': tool.get('link', ''),
                    'category': category,
                    'source': 'mahseema/awesome-ai-tools'
                })
    except Exception as e:
        print(f"Error extracting from mahseema data: {e}")
    
    return tools

def extract_tools_from_steven2358(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from steven2358/awesome-generative-ai repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        tools_data = raw_content.get('data', {}).get('tools', [])
        
        for tool in tools_data:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'category': tool.get('category', ''),
                'source': 'steven2358/awesome-generative-ai'
            })
    except Exception as e:
        print(f"Error extracting from steven2358 data: {e}")
    
    return tools

def extract_tools_from_ai_tools_inc(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from ai-tools-inc/awesome-ai-tools repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        ai_tools_data = raw_content.get('data', {}).get('ai_tools', [])
        
        for tool in ai_tools_data:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'category': tool.get('category', ''),
                'source': 'ai-tools-inc/awesome-ai-tools'
            })
    except Exception as e:
        print(f"Error extracting from ai-tools-inc data: {e}")
    
    return tools

def extract_tools_from_ghimiresunil(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from ghimiresunil/Top-AI-Tools repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        features_data = raw_content.get('data', {}).get('features', [])
        
        for tool in features_data:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'category': tool.get('category', ''),
                'source': 'ghimiresunil/Top-AI-Tools'
            })
    except Exception as e:
        print(f"Error extracting from ghimiresunil data: {e}")
    
    return tools

def extract_tools_from_re50urces(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from re50urces/Awesome-AI repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        features_data = raw_content.get('data', {}).get('features', [])
        
        for tool in features_data:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'category': tool.get('category', ''),
                'source': 're50urces/Awesome-AI'
            })
    except Exception as e:
        print(f"Error extracting from re50urces data: {e}")
    
    return tools

def extract_tools_from_jamesmurdza(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tools from jamesmurdza/awesome-ai-devtools repository data."""
    tools = []
    try:
        raw_content = json.loads(data.get('raw_content', '{}'))
        features_data = raw_content.get('data', {}).get('features', [])
        
        for tool in features_data:
            tools.append({
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'link': tool.get('link', ''),
                'category': tool.get('category', ''),
                'source': 'jamesmurdza/awesome-ai-devtools'
            })
    except Exception as e:
        print(f"Error extracting from jamesmurdza data: {e}")
    
    return tools

def clean_and_validate_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean and validate tool data."""
    cleaned_tools = []
    seen_names = set()
    
    for tool in tools:
        # Skip if no name or empty name
        if not tool.get('name', '').strip():
            continue
            
        # Skip if no link or invalid link
        link = tool.get('link', '').strip()
        if not link or link == 'null' or link == '':
            continue
            
        # Clean up the data
        cleaned_tool = {
            'name': tool.get('name', '').strip(),
            'description': tool.get('description', '').strip(),
            'link': link,
            'category': tool.get('category', '').strip() or 'Unknown',
            'source': tool.get('source', '').strip()
        }
        
        # Avoid duplicates based on name (case-insensitive)
        name_key = cleaned_tool['name'].lower()
        if name_key not in seen_names:
            seen_names.add(name_key)
            cleaned_tools.append(cleaned_tool)
    
    return cleaned_tools

def main():
    """Main function to process all repositories and create consolidated JSON."""
    print("Starting AI tools extraction...")
    
    # Define file paths
    extract_dir = '/workspace/extract'
    files_to_process = [
        ('mahseema_awesome_ai_tools.json', extract_tools_from_mahseema),
        ('steven2358_awesome_generative_ai.json', extract_tools_from_steven2358),
        ('ai_tools_inc_awesome_ai_tools.json', extract_tools_from_ai_tools_inc),
        ('ghimiresunil_top_ai_tools.json', extract_tools_from_ghimiresunil),
        ('re50urces_awesome_ai.json', extract_tools_from_re50urces),
        ('jamesmurdza_awesome_ai_devtools.json', extract_tools_from_jamesmurdza)
    ]
    
    all_tools = []
    
    # Process each file
    for filename, extractor_func in files_to_process:
        file_path = os.path.join(extract_dir, filename)
        print(f"Processing {filename}...")
        
        data = load_json_file(file_path)
        if data:
            tools = extractor_func(data)
            all_tools.extend(tools)
            print(f"  Extracted {len(tools)} tools from {filename}")
        else:
            print(f"  Failed to load {filename}")
    
    print(f"Total tools before cleaning: {len(all_tools)}")
    
    # Clean and validate tools
    cleaned_tools = clean_and_validate_tools(all_tools)
    print(f"Total tools after cleaning: {len(cleaned_tools)}")
    
    # Create final data structure
    final_data = {
        'metadata': {
            'total_tools': len(cleaned_tools),
            'extraction_date': '2025-08-21',
            'sources': [
                'https://github.com/mahseema/awesome-ai-tools',
                'https://github.com/steven2358/awesome-generative-ai',
                'https://github.com/ai-tools-inc/awesome-ai-tools',
                'https://github.com/ghimiresunil/Top-AI-Tools',
                'https://github.com/re50urces/Awesome-AI',
                'https://github.com/jamesmurdza/awesome-ai-devtools'
            ]
        },
        'tools': cleaned_tools
    }
    
    # Ensure data directory exists
    os.makedirs('/workspace/data', exist_ok=True)
    
    # Save to JSON file
    output_file = '/workspace/data/additional_github_tools.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(cleaned_tools)} tools to {output_file}")
        
        # Print some statistics
        categories = {}
        sources = {}
        for tool in cleaned_tools:
            category = tool.get('category', 'Unknown')
            source = tool.get('source', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\nCategory distribution:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {category}: {count} tools")
            
        print(f"\nSource distribution:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count} tools")
            
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

if __name__ == "__main__":
    main()