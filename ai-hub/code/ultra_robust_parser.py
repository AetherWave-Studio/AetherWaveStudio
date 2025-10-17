#!/usr/bin/env python3
"""
Ultra-robust AI tools parser that handles truncated and malformed JSON.
"""

import json
import os
import re
from typing import List, Dict, Any

def repair_json(json_str: str) -> str:
    """Attempt to repair truncated/malformed JSON."""
    # Remove trailing incomplete entries
    json_str = json_str.strip()
    
    # If it ends abruptly, try to close it properly
    if not json_str.endswith('}'):
        # Find the last complete object
        brace_count = 0
        last_complete_pos = -1
        
        for i, char in enumerate(json_str):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    last_complete_pos = i
        
        if last_complete_pos > 0:
            json_str = json_str[:last_complete_pos + 1]
    
    return json_str

def extract_tools_with_regex(content: str, source: str) -> List[Dict[str, Any]]:
    """Extract tools using regex patterns as a fallback."""
    tools = []
    
    # Pattern to match tool objects in JSON
    tool_patterns = [
        # Basic tool pattern with name, description, link
        r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"',
        # Alternative pattern with category
        r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"[^}]*?"category":\s*"([^"]*?)"',
        # Pattern for category + tools structure
        r'"category":\s*"([^"]+)"[^}]*?"tools":\s*\[(.*?)\]',
    ]
    
    # Extract using different patterns
    for pattern in tool_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            if len(match) >= 3:
                name = match[0].strip()
                description = match[1].strip() if len(match) > 1 else ""
                link = match[2].strip() if len(match) > 2 else ""
                category = match[3].strip() if len(match) > 3 else "Unknown"
                
                if name and link and link.startswith('http'):
                    tools.append({
                        'name': name,
                        'description': description,
                        'link': link,
                        'category': category,
                        'source': source
                    })
    
    return tools

def extract_from_partial_json(file_path: str, source: str) -> List[Dict[str, Any]]:
    """Extract tools from potentially truncated JSON files."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        raw_content = data.get('raw_content', '')
        if not raw_content:
            return tools
        
        # Try to parse the nested JSON
        try:
            nested_data = json.loads(raw_content)
            # Successfully parsed, extract using normal methods
            tools.extend(extract_from_structured_data(nested_data, source))
        except json.JSONDecodeError:
            # JSON is malformed, try to repair it
            try:
                repaired_json = repair_json(raw_content)
                nested_data = json.loads(repaired_json)
                tools.extend(extract_from_structured_data(nested_data, source))
            except:
                # Still failed, use regex extraction
                tools.extend(extract_tools_with_regex(raw_content, source))
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return tools

def extract_from_structured_data(data: Dict[str, Any], source: str) -> List[Dict[str, Any]]:
    """Extract tools from properly structured JSON data."""
    tools = []
    
    if 'data' not in data:
        return tools
    
    data_section = data['data']
    
    # Handle different structures based on source
    if 'extracted_information_details' in data_section:
        # mahseema structure
        for category_info in data_section['extracted_information_details']:
            category = category_info.get('category', 'Unknown')
            for tool in category_info.get('tools', []):
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool['name'],
                        'description': tool.get('description', ''),
                        'link': tool['link'],
                        'category': category,
                        'source': source
                    })
    
    elif 'tools' in data_section:
        # steven2358 structure
        for tool in data_section['tools']:
            if tool.get('name') and tool.get('link'):
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': tool.get('category', 'Unknown'),
                    'source': source
                })
    
    elif 'ai_tools' in data_section:
        # ai-tools-inc structure
        for tool in data_section['ai_tools']:
            if tool.get('name') and tool.get('link'):
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': tool.get('category', 'Unknown'),
                    'source': source
                })
    
    elif 'features' in data_section:
        # General features structure
        for tool in data_section['features']:
            if tool.get('name') and tool.get('link'):
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': tool.get('category', 'Unknown'),
                    'source': source
                })
    
    return tools

def validate_and_clean_tool(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean a tool entry."""
    # Clean each field
    name = str(tool.get('name', '')).strip()
    description = str(tool.get('description', '')).strip()
    link = str(tool.get('link', '')).strip()
    category = str(tool.get('category', 'Unknown')).strip()
    source = str(tool.get('source', '')).strip()
    
    # Remove any markdown or special formatting
    name = re.sub(r'\*+', '', name)  # Remove asterisks
    description = re.sub(r'\*+', '', description)
    
    # Clean up common artifacts
    if description.startswith('[reviews'):
        description = description.split(']')[-1].strip().lstrip('-').strip()
    
    return {
        'name': name,
        'description': description,
        'link': link,
        'category': category or 'Unknown',
        'source': source
    }

def is_valid_tool(tool: Dict[str, Any]) -> bool:
    """Check if a tool entry is valid."""
    # Check required fields
    name = tool.get('name', '').strip()
    link = tool.get('link', '').strip()
    
    # Must have name and link
    if not name or not link:
        return False
    
    # Link must be valid URL
    if not link.startswith(('http://', 'https://')):
        return False
    
    # Name should not be JSON-like
    if name.startswith(('{', '[', '"')):
        return False
    
    # Name should not be too long (likely a parsing error)
    if len(name) > 100:
        return False
    
    return True

def main():
    """Main extraction function."""
    print("Starting ultra-robust AI tools extraction...")
    
    extract_dir = '/workspace/extract'
    
    repositories = [
        ('mahseema_awesome_ai_tools.json', 'mahseema/awesome-ai-tools'),
        ('steven2358_awesome_generative_ai.json', 'steven2358/awesome-generative-ai'),
        ('ai_tools_inc_awesome_ai_tools.json', 'ai-tools-inc/awesome-ai-tools'),
        ('ghimiresunil_top_ai_tools.json', 'ghimiresunil/Top-AI-Tools'),
        ('re50urces_awesome_ai.json', 're50urces/Awesome-AI'),
        ('jamesmurdza_awesome_ai_devtools.json', 'jamesmurdza/awesome-ai-devtools')
    ]
    
    all_tools = []
    
    for filename, source in repositories:
        file_path = os.path.join(extract_dir, filename)
        print(f"Processing {filename}...")
        
        if os.path.exists(file_path):
            tools = extract_from_partial_json(file_path, source)
            all_tools.extend(tools)
            print(f"  ✓ Extracted {len(tools)} tools")
        else:
            print(f"  ❌ File not found")
    
    print(f"\nTotal tools extracted: {len(all_tools)}")
    
    # Clean and validate tools
    cleaned_tools = []
    seen_keys = set()
    
    for tool in all_tools:
        cleaned_tool = validate_and_clean_tool(tool)
        
        if is_valid_tool(cleaned_tool):
            # Create unique key for deduplication
            key = f"{cleaned_tool['name'].lower()}|{cleaned_tool['link'].lower()}"
            
            if key not in seen_keys:
                seen_keys.add(key)
                cleaned_tools.append(cleaned_tool)
    
    print(f"Tools after cleaning and validation: {len(cleaned_tools)}")
    
    # Create final output
    final_data = {
        'metadata': {
            'total_tools': len(cleaned_tools),
            'extraction_date': '2025-08-21',
            'extraction_method': 'robust_parsing_with_fallback',
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
    
    # Save to file
    os.makedirs('/workspace/data', exist_ok=True)
    output_file = '/workspace/data/additional_github_tools.json'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Successfully saved to {output_file}")
        
        # Comprehensive validation
        print("\nPerforming comprehensive validation...")
        
        # Re-read and validate
        with open(output_file, 'r', encoding='utf-8') as f:
            validation_data = json.load(f)
        
        # Check structure
        assert 'metadata' in validation_data, "Missing metadata"
        assert 'tools' in validation_data, "Missing tools"
        assert validation_data['metadata']['total_tools'] == len(cleaned_tools), "Metadata mismatch"
        
        # Validate all tools
        validation_errors = 0
        for i, tool in enumerate(validation_data['tools']):
            if not is_valid_tool(tool):
                print(f"  ❌ Tool {i} failed validation: {tool.get('name', 'Unknown')}")
                validation_errors += 1
        
        if validation_errors == 0:
            print("✓ All tools passed validation")
        else:
            print(f"❌ {validation_errors} tools failed validation")
        
        # Statistics
        if cleaned_tools:
            categories = {}
            sources = {}
            
            for tool in cleaned_tools:
                category = tool.get('category', 'Unknown')
                source = tool.get('source', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\nExtraction Results:")
            print(f"Sources processed: {len(repositories)}")
            print(f"Tools extracted: {len(cleaned_tools)}")
            print(f"Categories found: {len(categories)}")
            
            print(f"\nSource distribution:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"  {source}: {count} tools")
            
            print(f"\nTop categories:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {category}: {count} tools")
            
            print(f"\nSample tools:")
            for i, tool in enumerate(cleaned_tools[:5]):
                print(f"  {i+1}. {tool['name']}")
                print(f"     Description: {tool['description'][:80]}...")
                print(f"     Category: {tool['category']}")
                print(f"     Link: {tool['link']}")
                print()
        
    except Exception as e:
        print(f"❌ Error saving/validating: {e}")

if __name__ == "__main__":
    main()
