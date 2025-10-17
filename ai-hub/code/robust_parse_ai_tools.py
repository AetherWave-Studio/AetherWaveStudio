#!/usr/bin/env python3
"""
Parse extracted AI tools from GitHub repositories with robust JSON handling.
"""

import json
import os
import re
from typing import List, Dict, Any

def safe_json_loads(content: str) -> Dict[str, Any]:
    """Safely load JSON content with error handling."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {}

def extract_tools_from_raw_content(content: str, source: str) -> List[Dict[str, Any]]:
    """Extract tools from raw content using regex patterns."""
    tools = []
    
    # Pattern to match tool entries in various formats
    patterns = [
        # Pattern for name, description, link structure
        r'"name":\s*"([^"]+)"[^}]*"description":\s*"([^"]*)"[^}]*"link":\s*"([^"]*)"[^}]*"category":\s*"([^"]*)"',
        # Alternative pattern
        r'"name":\s*"([^"]+)"[^}]*"link":\s*"([^"]*)"[^}]*"description":\s*"([^"]*)"[^}]*"category":\s*"([^"]*)"',
        # Pattern for markdown-like structure
        r'\[([^\]]+)\]\(([^)]+)\)[^-]*-\s*([^\\n]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            if len(match) >= 3:
                if len(match) == 4:  # name, description, link, category
                    name, description, link, category = match
                elif len(match) == 3:  # name, link, description (markdown style)
                    name, link, description = match
                    category = "Unknown"
                
                # Clean up the extracted data
                name = name.strip()
                description = description.strip()
                link = link.strip()
                category = category.strip() if len(match) == 4 else "Unknown"
                
                if name and link and not link.startswith('null'):
                    tools.append({
                        'name': name,
                        'description': description,
                        'link': link,
                        'category': category,
                        'source': source
                    })
    
    return tools

def extract_from_file_content(file_path: str, source: str) -> List[Dict[str, Any]]:
    """Extract tools from a file using multiple strategies."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First try to parse as JSON
        try:
            data = json.loads(content)
            raw_content_str = data.get('raw_content', '')
            if raw_content_str:
                # Try to parse the nested JSON
                try:
                    nested_data = json.loads(raw_content_str)
                    tools.extend(extract_structured_data(nested_data, source))
                except:
                    # If nested JSON fails, try regex extraction
                    tools.extend(extract_tools_from_raw_content(raw_content_str, source))
        except:
            # If main JSON parsing fails, try regex on entire content
            tools.extend(extract_tools_from_raw_content(content, source))
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return tools

def extract_structured_data(data: Dict[str, Any], source: str) -> List[Dict[str, Any]]:
    """Extract tools from structured data."""
    tools = []
    
    # Handle different data structures
    if 'data' in data:
        data_section = data['data']
        
        # Check for different tool structures
        for key in ['tools', 'ai_tools', 'features', 'extracted_information_details']:
            if key in data_section:
                items = data_section[key]
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            if key == 'extracted_information_details':
                                # Handle mahseema structure
                                category = item.get('category', 'Unknown')
                                for tool in item.get('tools', []):
                                    tools.append({
                                        'name': tool.get('name', ''),
                                        'description': tool.get('description', ''),
                                        'link': tool.get('link', ''),
                                        'category': category,
                                        'source': source
                                    })
                            else:
                                # Handle direct tool structure
                                tools.append({
                                    'name': item.get('name', ''),
                                    'description': item.get('description', ''),
                                    'link': item.get('link', ''),
                                    'category': item.get('category', 'Unknown'),
                                    'source': source
                                })
    
    return tools

def manual_extraction_patterns(content: str, source: str) -> List[Dict[str, Any]]:
    """Manual extraction using content-specific patterns."""
    tools = []
    
    # Extract GitHub Copilot pattern
    github_pattern = r'GitHub Copilot[^"]*"([^"]*)"[^"]*"([^"]*)"'
    matches = re.findall(github_pattern, content, re.IGNORECASE)
    for match in matches:
        if len(match) >= 2:
            tools.append({
                'name': 'GitHub Copilot',
                'description': match[0],
                'link': match[1],
                'category': 'Developer Tools',
                'source': source
            })
    
    # Extract ChatGPT pattern
    chatgpt_pattern = r'ChatGPT[^"]*"([^"]*)"[^"]*"([^"]*)"'
    matches = re.findall(chatgpt_pattern, content, re.IGNORECASE)
    for match in matches:
        if len(match) >= 2:
            tools.append({
                'name': 'ChatGPT',
                'description': match[0],
                'link': match[1],
                'category': 'Conversational AI',
                'source': source
            })
    
    # Extract general tool patterns
    tool_patterns = [
        r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"',
        r'\*\*([^*]+)\*\*[^-]*?-\s*([^\\n]+?)(?:https?://[^\\s]+)',
        r'\[([^\]]+)\]\(([^)]+)\)[^-]*?-\s*([^\\n]+)',
    ]
    
    for pattern in tool_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        for match in matches:
            if len(match) >= 3:
                name = match[0].strip()
                description = match[1].strip() if len(match) > 1 else ""
                link = match[2].strip() if len(match) > 2 else match[1].strip()
                
                # Basic validation
                if name and link and link.startswith('http'):
                    tools.append({
                        'name': name,
                        'description': description,
                        'link': link,
                        'category': 'Unknown',
                        'source': source
                    })
    
    return tools

def main():
    """Main function to process all repositories and create consolidated JSON."""
    print("Starting AI tools extraction with robust parsing...")
    
    # Define repositories and their extracted files
    repositories = [
        ('mahseema_awesome_ai_tools.json', 'mahseema/awesome-ai-tools'),
        ('steven2358_awesome_generative_ai.json', 'steven2358/awesome-generative-ai'),
        ('ai_tools_inc_awesome_ai_tools.json', 'ai-tools-inc/awesome-ai-tools'),
        ('ghimiresunil_top_ai_tools.json', 'ghimiresunil/Top-AI-Tools'),
        ('re50urces_awesome_ai.json', 're50urces/Awesome-AI'),
        ('jamesmurdza_awesome_ai_devtools.json', 'jamesmurdza/awesome-ai-devtools')
    ]
    
    all_tools = []
    extract_dir = '/workspace/extract'
    
    # Process each repository
    for filename, source in repositories:
        file_path = os.path.join(extract_dir, filename)
        print(f"Processing {filename}...")
        
        if os.path.exists(file_path):
            tools = extract_from_file_content(file_path, source)
            
            # If no tools found, try manual extraction
            if not tools:
                print(f"  No structured tools found, trying manual extraction...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tools = manual_extraction_patterns(content, source)
            
            all_tools.extend(tools)
            print(f"  Extracted {len(tools)} tools from {filename}")
        else:
            print(f"  File not found: {filename}")
    
    print(f"Total tools extracted: {len(all_tools)}")
    
    # Clean and deduplicate tools
    seen = set()
    cleaned_tools = []
    
    for tool in all_tools:
        name = tool.get('name', '').strip()
        link = tool.get('link', '').strip()
        
        # Skip invalid entries
        if not name or not link or not link.startswith('http'):
            continue
            
        # Create a unique key for deduplication
        key = (name.lower(), link.lower())
        if key not in seen:
            seen.add(key)
            cleaned_tools.append({
                'name': name,
                'description': tool.get('description', '').strip(),
                'link': link,
                'category': tool.get('category', 'Unknown').strip() or 'Unknown',
                'source': tool.get('source', '').strip()
            })
    
    print(f"Tools after cleaning and deduplication: {len(cleaned_tools)}")
    
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
        
        # Print statistics
        if cleaned_tools:
            categories = {}
            sources = {}
            for tool in cleaned_tools:
                category = tool.get('category', 'Unknown')
                source = tool.get('source', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\nTop categories:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {category}: {count} tools")
                
            print(f"\nSource distribution:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"  {source}: {count} tools")
        
        # Show sample tools
        print(f"\nSample tools:")
        for i, tool in enumerate(cleaned_tools[:5]):
            print(f"  {i+1}. {tool['name']}: {tool['description'][:50]}...")
            
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

if __name__ == "__main__":
    main()