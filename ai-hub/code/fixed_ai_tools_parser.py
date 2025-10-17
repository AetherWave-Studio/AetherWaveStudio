#!/usr/bin/env python3
"""
Fixed robust parser for AI tools extraction from GitHub repositories.
"""

import json
import os
import re
from typing import List, Dict, Any

def safe_json_parse(content: str) -> Dict[str, Any]:
    """Safely parse JSON with proper error handling and cleaning."""
    try:
        # First, try direct JSON parsing
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            # Try fixing common issues like trailing commas
            content = re.sub(r',(\s*[}\]])', r'\1', content)
            return json.loads(content)
        except:
            return {}

def extract_from_mahseema(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from mahseema/awesome-ai-tools repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            extracted_details = nested_data.get('data', {}).get('extracted_information_details', [])
            
            for category_info in extracted_details:
                category = category_info.get('category', 'Unknown')
                category_tools = category_info.get('tools', [])
                
                for tool in category_tools:
                    if tool.get('name') and tool.get('link'):
                        tools.append({
                            'name': tool.get('name', '').strip(),
                            'description': tool.get('description', '').strip(),
                            'link': tool.get('link', '').strip(),
                            'category': category,
                            'source': 'mahseema/awesome-ai-tools'
                        })
    except Exception as e:
        print(f"Error parsing mahseema file: {e}")
    
    return tools

def extract_from_steven2358(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from steven2358/awesome-generative-ai repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            tools_list = nested_data.get('data', {}).get('tools', [])
            
            for tool in tools_list:
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool.get('name', '').strip(),
                        'description': tool.get('description', '').strip(),
                        'link': tool.get('link', '').strip(),
                        'category': tool.get('category', 'Unknown'),
                        'source': 'steven2358/awesome-generative-ai'
                    })
    except Exception as e:
        print(f"Error parsing steven2358 file: {e}")
    
    return tools

def extract_from_ai_tools_inc(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from ai-tools-inc/awesome-ai-tools repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            ai_tools_list = nested_data.get('data', {}).get('ai_tools', [])
            
            for tool in ai_tools_list:
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool.get('name', '').strip(),
                        'description': tool.get('description', '').strip(),
                        'link': tool.get('link', '').strip(),
                        'category': tool.get('category', 'Unknown'),
                        'source': 'ai-tools-inc/awesome-ai-tools'
                    })
    except Exception as e:
        print(f"Error parsing ai-tools-inc file: {e}")
    
    return tools

def extract_from_ghimiresunil(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from ghimiresunil/Top-AI-Tools repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            features_list = nested_data.get('data', {}).get('features', [])
            
            for tool in features_list:
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool.get('name', '').strip(),
                        'description': tool.get('description', '').strip(),
                        'link': tool.get('link', '').strip(),
                        'category': tool.get('category', 'Unknown'),
                        'source': 'ghimiresunil/Top-AI-Tools'
                    })
    except Exception as e:
        print(f"Error parsing ghimiresunil file: {e}")
    
    return tools

def extract_from_re50urces(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from re50urces/Awesome-AI repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            features_list = nested_data.get('data', {}).get('features', [])
            
            for tool in features_list:
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool.get('name', '').strip(),
                        'description': tool.get('description', '').strip(),
                        'link': tool.get('link', '').strip(),
                        'category': tool.get('category', 'Unknown'),
                        'source': 're50urces/Awesome-AI'
                    })
    except Exception as e:
        print(f"Error parsing re50urces file: {e}")
    
    return tools

def extract_from_jamesmurdza(file_path: str) -> List[Dict[str, Any]]:
    """Extract tools from jamesmurdza/awesome-ai-devtools repository."""
    tools = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse the nested raw_content JSON
        raw_content = data.get('raw_content', '')
        if raw_content:
            nested_data = json.loads(raw_content)
            features_list = nested_data.get('data', {}).get('features', [])
            
            for tool in features_list:
                if tool.get('name') and tool.get('link'):
                    tools.append({
                        'name': tool.get('name', '').strip(),
                        'description': tool.get('description', '').strip(),
                        'link': tool.get('link', '').strip(),
                        'category': tool.get('category', 'Unknown'),
                        'source': 'jamesmurdza/awesome-ai-devtools'
                    })
    except Exception as e:
        print(f"Error parsing jamesmurdza file: {e}")
    
    return tools

def validate_tool(tool: Dict[str, Any]) -> bool:
    """Validate that a tool entry is properly formatted."""
    # Check required fields
    required_fields = ['name', 'description', 'link', 'category', 'source']
    for field in required_fields:
        if field not in tool:
            return False
    
    # Check that name and link are not empty
    if not tool['name'].strip() or not tool['link'].strip():
        return False
    
    # Check that link is valid URL
    if not tool['link'].startswith(('http://', 'https://')):
        return False
    
    # Check for malformed JSON in name (common parsing error)
    if tool['name'].strip().startswith(('{', '[')):
        return False
    
    return True

def clean_and_deduplicate(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean and deduplicate tools list."""
    cleaned_tools = []
    seen_keys = set()
    
    for tool in tools:
        # Validate tool
        if not validate_tool(tool):
            continue
        
        # Create unique key for deduplication (name + link)
        unique_key = f"{tool['name'].lower().strip()}|{tool['link'].lower().strip()}"
        
        if unique_key not in seen_keys:
            seen_keys.add(unique_key)
            
            # Clean the tool data
            cleaned_tool = {
                'name': tool['name'].strip(),
                'description': tool['description'].strip(),
                'link': tool['link'].strip(),
                'category': tool['category'].strip() or 'Unknown',
                'source': tool['source'].strip()
            }
            
            cleaned_tools.append(cleaned_tool)
    
    return cleaned_tools

def main():
    """Main function to extract and process all AI tools."""
    print("Starting fixed AI tools extraction...")
    
    extract_dir = '/workspace/extract'
    
    # Define extraction functions for each repository
    extractors = [
        ('mahseema_awesome_ai_tools.json', extract_from_mahseema),
        ('steven2358_awesome_generative_ai.json', extract_from_steven2358),
        ('ai_tools_inc_awesome_ai_tools.json', extract_from_ai_tools_inc),
        ('ghimiresunil_top_ai_tools.json', extract_from_ghimiresunil),
        ('re50urces_awesome_ai.json', extract_from_re50urces),
        ('jamesmurdza_awesome_ai_devtools.json', extract_from_jamesmurdza)
    ]
    
    all_tools = []
    
    # Extract from each repository
    for filename, extractor_func in extractors:
        file_path = os.path.join(extract_dir, filename)
        print(f"Processing {filename}...")
        
        if os.path.exists(file_path):
            try:
                tools = extractor_func(file_path)
                all_tools.extend(tools)
                print(f"  ✓ Extracted {len(tools)} tools from {filename}")
            except Exception as e:
                print(f"  ❌ Error processing {filename}: {e}")
        else:
            print(f"  ❌ File not found: {filename}")
    
    print(f"\nTotal tools before cleaning: {len(all_tools)}")
    
    # Clean and deduplicate
    cleaned_tools = clean_and_deduplicate(all_tools)
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
        
        print(f"✓ Successfully saved {len(cleaned_tools)} tools to {output_file}")
        
        # Validate the output
        print("\nValidating output...")
        
        # Re-read and validate JSON
        with open(output_file, 'r', encoding='utf-8') as f:
            validation_data = json.load(f)
        
        assert validation_data['metadata']['total_tools'] == len(cleaned_tools), "Metadata mismatch"
        assert len(validation_data['tools']) == len(cleaned_tools), "Tools count mismatch"
        
        # Validate random samples
        import random
        sample_tools = random.sample(validation_data['tools'], min(5, len(validation_data['tools'])))
        for i, tool in enumerate(sample_tools):
            assert validate_tool(tool), f"Sample tool {i} failed validation"
        
        print("✓ Output validation passed")
        
        # Print statistics
        if cleaned_tools:
            categories = {}
            sources = {}
            for tool in cleaned_tools:
                category = tool.get('category', 'Unknown')
                source = tool.get('source', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\nSource distribution:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"  {source}: {count} tools")
            
            print(f"\nTop 10 categories:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {category}: {count} tools")
        
        print(f"\nSample tools:")
        for i, tool in enumerate(cleaned_tools[:3]):
            print(f"  {i+1}. {tool['name']}: {tool['description'][:60]}...")
            print(f"     Category: {tool['category']}, Source: {tool['source']}")
            
    except Exception as e:
        print(f"❌ Error saving/validating output: {e}")

if __name__ == "__main__":
    main()
