#!/usr/bin/env python3
"""
Robust JSON Parser for AI Tools Data
Handles malformed JSON and escape character issues
"""

import json
import re
from typing import Dict, List, Any, Optional

def fix_json_escape_issues(content: str) -> str:
    """Fix common JSON escape character issues"""
    # Fix backslash issues in Japanese text and other problematic strings
    content = re.sub(r'\\(?!["\\/bfnrtux])', r'\\\\', content)
    
    # Fix specific problematic patterns we've seen
    content = content.replace('\\*', '*')
    content = content.replace('\\"', '"')
    
    # Fix unterminated strings by finding and completing them
    # Look for strings that start with " but don't have a closing "
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # If line has unmatched quotes, try to fix it
        quote_count = line.count('"') - line.count('\\"')
        if quote_count % 2 != 0:
            # Odd number of quotes - try to close the string properly
            if line.strip().endswith(',') or line.strip().endswith('{') or line.strip().endswith('}'):
                line = line.rstrip() + '"'
            elif not line.strip().endswith('"'):
                line = line + '"'
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def extract_tools_with_regex(content: str) -> List[Dict[str, Any]]:
    """Extract tools using regex patterns when JSON parsing fails"""
    tools = []
    
    # Pattern to match complete tool objects
    tool_pattern = r'\{\s*"name":\s*"([^"]*)"[^}]*?"title":\s*"([^"]*)"[^}]*?"description":\s*"([^"]*)"[^}]*?"offer_free_version":\s*([^,}]*)[^}]*?"link":\s*"([^"]*)"[^}]*?\}'
    
    matches = re.findall(tool_pattern, content, re.DOTALL)
    
    for match in matches:
        name, title, description, free_version, link = match
        
        # Clean up the free_version value
        free_version = free_version.strip().strip('"').strip(',')
        if free_version.lower() == 'true':
            free_version = 'Yes'
        elif free_version.lower() == 'false':
            free_version = 'No'
        elif free_version.lower() in ['unknown', '"unknown"']:
            free_version = 'Unknown'
        else:
            free_version = 'Unknown'
        
        tool = {
            'name': name.strip(),
            'title': title.strip(),
            'description': description.strip(),
            'link': link.strip(),
            'free_version': free_version,
            'category': 'Unknown'  # Will be determined by context
        }
        tools.append(tool)
    
    return tools

def extract_categories_and_tools(content: str) -> Dict[str, List[Dict]]:
    """Extract tools organized by categories"""
    result = {}
    
    # Look for category sections in the format: "Category Name": [...]
    category_pattern = r'"([^"]+)":\s*\[\s*\{([^]]+)\]\s*\}'
    
    category_matches = re.finditer(category_pattern, content, re.DOTALL)
    
    for category_match in category_matches:
        category_name = category_match.group(1)
        category_content = category_match.group(2)
        
        # Skip if this doesn't look like a tool category
        if not re.search(r'"name":', category_content):
            continue
        
        # Extract tools from this category
        tools = extract_tools_with_regex('{' + category_content + '}')
        
        # Set category for all tools
        for tool in tools:
            tool['category'] = category_name
        
        if tools:
            result[category_name] = tools
    
    return result

def extract_from_chunked_content(file_path: str, chunk_size: int = 20000) -> List[Dict[str, Any]]:
    """Extract tools by reading file in chunks to handle large files"""
    all_tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract the JSON content from the wrapper
        if content.startswith('{"raw_content":'):
            # This is a wrapped JSON - extract the inner content
            try:
                wrapper = json.loads(content)
                if 'raw_content' in wrapper:
                    content = wrapper['raw_content']
                    # Now we have the actual content, but it might still be JSON-encoded
                    if content.startswith('{'):
                        try:
                            content = json.loads(content)
                            if isinstance(content, dict) and 'data' in content:
                                content = json.dumps(content)
                        except:
                            pass  # Content is already a string
            except:
                pass  # Fall back to regex extraction
        
        # Use regex to find tool entries
        tools = extract_tools_with_regex(content)
        all_tools.extend(tools)
        
        # Also try to extract category-organized data
        categories_tools = extract_categories_and_tools(content)
        for category, category_tools in categories_tools.items():
            all_tools.extend(category_tools)
        
        # Remove duplicates based on name
        seen_names = set()
        unique_tools = []
        for tool in all_tools:
            name_key = tool['name'].lower().strip()
            if name_key and name_key not in seen_names:
                seen_names.add(name_key)
                unique_tools.append(tool)
        
        return unique_tools
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def find_more_tools_patterns(content: str) -> List[Dict[str, Any]]:
    """Find additional tool patterns that might be missed"""
    tools = []
    
    # Pattern for simple name-link pairs
    simple_pattern = r'"([^"]+)":\s*{\s*"link":\s*"([^"]+)"[^}]*?}'
    simple_matches = re.findall(simple_pattern, content)
    
    for name, link in simple_matches:
        if name and link and 'http' in link:
            tool = {
                'name': name.strip(),
                'title': '',
                'description': '',
                'link': link.strip(),
                'free_version': 'Unknown',
                'category': 'Unknown'
            }
            tools.append(tool)
    
    # Pattern for tools with different structure
    alt_pattern = r'"name":\s*"([^"]*)"[^}]*?"link":\s*"([^"]*)"[^}]*?"description":\s*"([^"]*)"'
    alt_matches = re.findall(alt_pattern, content, re.DOTALL)
    
    for name, link, description in alt_matches:
        tool = {
            'name': name.strip(),
            'title': '',
            'description': description.strip(),
            'link': link.strip(),
            'free_version': 'Unknown',
            'category': 'Unknown'
        }
        tools.append(tool)
    
    return tools

def main():
    """Main extraction function using robust parsing"""
    print("Starting robust AI tools extraction...")
    
    all_tools = []
    
    # Process both extraction files
    files = [
        '/workspace/extract/github_readme.json',
        '/workspace/extract/github_ai_tools_extraction.json'
    ]
    
    for file_path in files:
        print(f"\nProcessing {file_path}...")
        tools = extract_from_chunked_content(file_path)
        print(f"Extracted {len(tools)} tools from {file_path}")
        all_tools.extend(tools)
        
        # Try alternative extraction methods
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            additional_tools = find_more_tools_patterns(content)
            print(f"Found {len(additional_tools)} additional tools with alternative patterns")
            all_tools.extend(additional_tools)
        except Exception as e:
            print(f"Error in alternative extraction: {e}")
    
    # Remove duplicates
    seen_names = set()
    unique_tools = []
    for tool in all_tools:
        name_key = tool['name'].lower().strip()
        if name_key and name_key not in seen_names and len(name_key) > 1:
            seen_names.add(name_key)
            # Add source information
            tool['source'] = 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
            unique_tools.append(tool)
    
    print(f"\nTotal unique tools extracted: {len(unique_tools)}")
    
    # Analyze categories
    categories = {}
    for tool in unique_tools:
        category = tool.get('category', 'Unknown')
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print(f"Categories found: {len(categories)}")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} tools")
    
    return unique_tools

if __name__ == "__main__":
    tools = main()
    print(f"\nFinal count: {len(tools)} tools extracted")
