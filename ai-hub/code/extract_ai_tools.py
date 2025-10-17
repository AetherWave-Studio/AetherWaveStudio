#!/usr/bin/env python3
"""
Comprehensive AI Tools Data Extraction Script
Extracts all AI tools data from the GitHub repository sources and creates structured JSON
"""

import json
import re
from typing import Dict, List, Any

def normalize_free_version(value: Any) -> str:
    """Normalize free version indicators to consistent strings"""
    if value is True or value == "Yes" or value == "✅":
        return "Yes"
    elif value is False or value == "No" or value == "❌":
        return "No"
    elif value == "Unknown" or value == "Unsure" or value == "❔":
        return "Unknown"
    else:
        return "Unknown"

def clean_description(description: str) -> str:
    """Clean and normalize descriptions"""
    if not description or description.strip() == ".":
        return ""
    return description.strip()

def extract_tools_from_source(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from a single source file"""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested JSON content
        content = json.loads(data['raw_content'])
        
        # Extract from tools_by_category (README format)
        if 'tools_by_category' in content.get('data', {}):
            for category, category_tools in content['data']['tools_by_category'].items():
                for tool in category_tools:
                    tool_data = {
                        'name': tool.get('name', '').strip(),
                        'title': tool.get('title', '').strip(),
                        'description': clean_description(tool.get('description', '')),
                        'link': tool.get('link', '').strip(),
                        'category': category.strip(),
                        'free_version': normalize_free_version(tool.get('offer_free_version')),
                        'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
                    }
                    if tool_data['name']:  # Only add if name exists
                        tools.append(tool_data)
        
        # Extract from features format (main extraction format)
        if 'features' in content.get('data', {}):
            for feature_category in content['data']['features']:
                category = feature_category.get('category', 'Unknown').strip()
                if 'tools' in feature_category:
                    for tool in feature_category['tools']:
                        tool_data = {
                            'name': tool.get('name', '').strip(),
                            'title': tool.get('title', '').strip(),
                            'description': clean_description(tool.get('description', '')),
                            'link': tool.get('link', '').strip(),
                            'category': category,
                            'free_version': normalize_free_version(tool.get('offer_free_version')),
                            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
                        }
                        if tool_data['name']:  # Only add if name exists
                            tools.append(tool_data)
                            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []
    
    return tools

def merge_and_deduplicate_tools(tools_list1: List[Dict], tools_list2: List[Dict]) -> List[Dict]:
    """Merge two lists of tools and remove duplicates based on name"""
    merged = {}
    
    # Add tools from first list
    for tool in tools_list1:
        key = tool['name'].lower().strip()
        if key and key not in merged:
            merged[key] = tool
    
    # Add tools from second list, preferring ones with more complete data
    for tool in tools_list2:
        key = tool['name'].lower().strip()
        if key:
            if key not in merged:
                merged[key] = tool
            else:
                # If the new tool has a link and the existing one doesn't, replace it
                existing = merged[key]
                if tool.get('link') and not existing.get('link'):
                    merged[key] = tool
                # If the new tool has a better description, update it
                elif (len(tool.get('description', '')) > len(existing.get('description', '')) and 
                      tool.get('description') != '.'):
                    merged[key] = tool
    
    return list(merged.values())

def main():
    """Main extraction function"""
    print("Starting AI Tools Data Extraction...")
    
    # Extract from both sources
    readme_tools = extract_tools_from_source('/workspace/extract/github_readme.json')
    main_tools = extract_tools_from_source('/workspace/extract/github_ai_tools_extraction.json')
    
    print(f"README tools: {len(readme_tools)}")
    print(f"Main extraction tools: {len(main_tools)}")
    
    # Merge and deduplicate
    all_tools = merge_and_deduplicate_tools(readme_tools, main_tools)
    
    # Get categories
    categories = sorted(list(set(tool['category'] for tool in all_tools)))
    
    # Calculate statistics
    free_tools = sum(1 for tool in all_tools if tool['free_version'] == 'Yes')
    paid_tools = sum(1 for tool in all_tools if tool['free_version'] == 'No')
    unknown_tools = sum(1 for tool in all_tools if tool['free_version'] == 'Unknown')
    
    # Create final dataset
    dataset = {
        'metadata': {
            'source_repository': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools',
            'description': 'Comprehensive collection of AI tools extracted from the 1000-AI-collection-tools GitHub repository',
            'extraction_date': '2025-08-21',
            'total_tools': len(all_tools),
            'total_categories': len(categories),
            'categories': categories,
            'statistics': {
                'free_tools': free_tools,
                'paid_tools': paid_tools,
                'unknown_pricing': unknown_tools
            }
        },
        'tools': sorted(all_tools, key=lambda x: (x['category'], x['name']))
    }
    
    # Save to file
    output_file = '/workspace/data/primary_github_tools.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtraction Complete!")
    print(f"Total tools extracted: {len(all_tools)}")
    print(f"Total categories: {len(categories)}")
    print(f"Free tools: {free_tools}")
    print(f"Paid tools: {paid_tools}")
    print(f"Unknown pricing: {unknown_tools}")
    print(f"Data saved to: {output_file}")
    
    # Print sample categories
    print(f"\nCategories found:")
    for i, category in enumerate(categories[:10]):
        category_count = sum(1 for tool in all_tools if tool['category'] == category)
        print(f"  {i+1}. {category} ({category_count} tools)")
    if len(categories) > 10:
        print(f"  ... and {len(categories) - 10} more categories")
    
    # Print sample tools
    print(f"\nSample tools:")
    for i, tool in enumerate(all_tools[:5]):
        print(f"  {i+1}. {tool['name']} ({tool['category']}) - Free: {tool['free_version']}")

if __name__ == "__main__":
    main()