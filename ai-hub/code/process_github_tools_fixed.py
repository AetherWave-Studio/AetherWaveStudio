#!/usr/bin/env python3
"""
Fixed script to process and combine AI tools data from multiple GitHub repositories.
"""

import json
import re
from typing import List, Dict, Any

def parse_e2b_data(file_path: str) -> List[Dict[str, Any]]:
    """Parse the e2b-dev/awesome-ai-agents data with error handling."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # The file contains raw JSON, let's parse it directly
        data = json.loads(content)
        raw_content = data.get('raw_content', '')
        
        if not raw_content:
            print("No raw_content found in e2b data")
            return tools
        
        # Parse the nested JSON
        try:
            json_data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            print(f"Error parsing nested JSON in e2b data: {e}")
            # Try to fix common JSON issues
            raw_content_fixed = raw_content.replace('\\n', ' ').replace('\\"', '"')
            try:
                json_data = json.loads(raw_content_fixed)
            except json.JSONDecodeError:
                print("Could not fix JSON parsing, extracting manually...")
                return extract_e2b_tools_manually(raw_content)
        
        ai_agents = json_data.get('data', {}).get('ai_agents', [])
        
        for agent in ai_agents:
            tool = {
                'name': agent.get('tool_name', ''),
                'url': agent.get('tool_url', ''),
                'categories': agent.get('category', []),
                'description': agent.get('description', '').replace('\\n', '\n'),
                'additional_links': agent.get('links', []),
                'source_repository': 'e2b-dev/awesome-ai-agents'
            }
            
            if tool['name']:  # Only add if tool has a name
                tools.append(tool)
                
    except Exception as e:
        print(f"Error parsing e2b data: {e}")
        
    return tools

def extract_e2b_tools_manually(raw_content: str) -> List[Dict[str, Any]]:
    """Manually extract tools from e2b data using regex patterns."""
    tools = []
    
    try:
        # Find tool entries using regex patterns
        tool_pattern = r'"tool_name":\s*"([^"]+)"[^}]*?"tool_url":\s*"([^"]+)"[^}]*?"category":\s*(\[[^\]]+\])[^}]*?"description":\s*"([^"]+(?:\\.[^"]*)*)"'
        
        matches = re.findall(tool_pattern, raw_content)
        
        for match in matches:
            name, url, categories_str, description = match
            
            # Parse categories
            try:
                categories = json.loads(categories_str.replace("'", '"'))
            except:
                categories = []
            
            tool = {
                'name': name,
                'url': url,
                'categories': categories,
                'description': description.replace('\\n', '\n').replace('\\"', '"'),
                'additional_links': [],
                'source_repository': 'e2b-dev/awesome-ai-agents'
            }
            
            tools.append(tool)
    except Exception as e:
        print(f"Error in manual extraction: {e}")
    
    return tools

def parse_partharay_data(file_path: str) -> List[Dict[str, Any]]:
    """Parse the ParthaPRay/Curated-List-of-Generative-AI-Tools data."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the JSON content
        data = json.loads(content)
        raw_content = data.get('raw_content', '')
        
        if not raw_content:
            print("No raw_content found in ParthaPRay data")
            return tools
        
        # Parse the nested JSON
        try:
            json_data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            print(f"Error parsing nested JSON in ParthaPRay data: {e}")
            return extract_partharay_tools_manually(raw_content)
        
        extracted_info = json_data.get('data', {}).get('extracted_information', '')
        
        # Parse the extracted information to identify tools
        tool_entries = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\\n- \*\*|\\n\\n|\Z)', extracted_info, re.DOTALL)
        
        for tool_name, description in tool_entries:
            tool = {
                'name': tool_name.strip(),
                'url': '',  # URL not provided in this format
                'categories': ['Generative AI'],  # Default category
                'description': description.strip().replace('\\n', '\n'),
                'additional_links': [],
                'source_repository': 'ParthaPRay/Curated-List-of-Generative-AI-Tools'
            }
            
            # Attempt to categorize based on description keywords
            desc_lower = description.lower()
            categories = ['Generative AI']
            
            if any(keyword in desc_lower for keyword in ['code', 'coding', 'programming', 'developer']):
                categories.append('Coding')
            if any(keyword in desc_lower for keyword in ['llm', 'language model']):
                categories.append('Language Models')
            if any(keyword in desc_lower for keyword in ['agent', 'autonomous']):
                categories.append('AI Agents')
            if any(keyword in desc_lower for keyword in ['framework', 'platform']):
                categories.append('Framework')
            if any(keyword in desc_lower for keyword in ['video', 'image', 'visual']):
                categories.append('Multimedia')
            if any(keyword in desc_lower for keyword in ['data', 'analysis', 'analytics']):
                categories.append('Data Analysis')
                
            tool['categories'] = categories
            
            if tool['name']:  # Only add if tool has a name
                tools.append(tool)
                
    except Exception as e:
        print(f"Error parsing ParthaPRay data: {e}")
        
    return tools

def extract_partharay_tools_manually(raw_content: str) -> List[Dict[str, Any]]:
    """Manually extract tools from ParthaPRay data."""
    tools = []
    
    try:
        # Look for the extracted_information field
        info_match = re.search(r'"extracted_information":\s*"([^"]+(?:\\.[^"]*)*)"', raw_content)
        if info_match:
            extracted_info = info_match.group(1)
            
            # Parse tool entries
            tool_entries = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\\n- \*\*|\\n\\n|\Z)', extracted_info, re.DOTALL)
            
            for tool_name, description in tool_entries:
                tool = {
                    'name': tool_name.strip(),
                    'url': '',
                    'categories': ['Generative AI'],
                    'description': description.strip().replace('\\n', '\n'),
                    'additional_links': [],
                    'source_repository': 'ParthaPRay/Curated-List-of-Generative-AI-Tools'
                }
                
                # Categorize based on description
                desc_lower = description.lower()
                categories = ['Generative AI']
                
                if any(keyword in desc_lower for keyword in ['code', 'coding', 'programming']):
                    categories.append('Coding')
                if any(keyword in desc_lower for keyword in ['agent', 'autonomous']):
                    categories.append('AI Agents')
                if any(keyword in desc_lower for keyword in ['framework', 'platform']):
                    categories.append('Framework')
                
                tool['categories'] = categories
                
                if tool['name']:
                    tools.append(tool)
    except Exception as e:
        print(f"Error in manual ParthaPRay extraction: {e}")
    
    return tools

def combine_and_deduplicate_tools(tools_lists: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Combine tool lists and remove duplicates based on name similarity."""
    all_tools = []
    seen_names = set()
    
    for tools_list in tools_lists:
        for tool in tools_list:
            name_lower = tool['name'].lower().strip()
            
            # Simple deduplication - exact name matches
            if name_lower not in seen_names:
                seen_names.add(name_lower)
                all_tools.append(tool)
    
    return all_tools

def main():
    """Main function to process and combine all tool data."""
    print("Processing GitHub AI tools data...")
    
    # Parse data from both repositories
    e2b_tools = parse_e2b_data('/workspace/extract/e2b_awesome_ai_agents.json')
    partharay_tools = parse_partharay_data('/workspace/extract/partharay_generative_ai_tools.json')
    
    print(f"Extracted {len(e2b_tools)} tools from e2b-dev repository")
    print(f"Extracted {len(partharay_tools)} tools from ParthaPRay repository")
    
    # If no tools were extracted, try reading raw files directly
    if len(e2b_tools) == 0 and len(partharay_tools) == 0:
        print("Trying alternative parsing methods...")
        
        # Try reading the files as simple text and extract patterns
        try:
            with open('/workspace/extract/e2b_awesome_ai_agents.json', 'r') as f:
                e2b_content = f.read()
            
            with open('/workspace/extract/partharay_generative_ai_tools.json', 'r') as f:
                partharay_content = f.read()
            
            # Extract tool names from both files using simple patterns
            e2b_names = re.findall(r'"tool_name":\s*"([^"]+)"', e2b_content)
            partharay_names = re.findall(r'\*\*(.*?)\*\*:', partharay_content)
            
            print(f"Found {len(e2b_names)} tool names in e2b data")
            print(f"Found {len(partharay_names)} tool names in ParthaPRay data")
            
            # Create basic tool objects
            for name in e2b_names:
                if name:
                    e2b_tools.append({
                        'name': name,
                        'url': '',
                        'categories': ['AI Tools'],
                        'description': '',
                        'additional_links': [],
                        'source_repository': 'e2b-dev/awesome-ai-agents'
                    })
            
            for name in partharay_names:
                if name:
                    partharay_tools.append({
                        'name': name.strip(),
                        'url': '',
                        'categories': ['Generative AI'],
                        'description': '',
                        'additional_links': [],
                        'source_repository': 'ParthaPRay/Curated-List-of-Generative-AI-Tools'
                    })
                    
        except Exception as e:
            print(f"Error in alternative parsing: {e}")
    
    # Combine and deduplicate
    all_tools = combine_and_deduplicate_tools([e2b_tools, partharay_tools])
    
    print(f"Total unique tools after deduplication: {len(all_tools)}")
    
    # Sort tools alphabetically by name
    all_tools.sort(key=lambda x: x['name'].lower())
    
    # Create summary statistics
    total_tools = len(all_tools)
    
    # Count categories
    category_counts = {}
    for tool in all_tools:
        for category in tool['categories']:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    # Count source repositories
    source_counts = {}
    for tool in all_tools:
        source = tool['source_repository']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # Create the final data structure
    result = {
        'metadata': {
            'title': 'AI Tools from GitHub Repositories',
            'description': 'Comprehensive collection of AI tools extracted from awesome-ai-tools, curated-list-of-generative-ai-tools, and awesome-ai-agents repositories',
            'extraction_date': '2025-08-21',
            'total_tools': total_tools,
            'source_repositories': list(source_counts.keys()),
            'source_counts': source_counts,
            'category_distribution': category_counts,
            'note': 'Data extracted from GitHub repositories focusing on AI agents and generative AI tools'
        },
        'tools': all_tools
    }
    
    # Save to JSON file
    output_file = '/workspace/data/remaining_github_tools.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {total_tools} AI tools to {output_file}")
    print(f"Categories found: {list(category_counts.keys())}")
    
    # Show sample tools
    if all_tools:
        print("\nSample tools extracted:")
        for i, tool in enumerate(all_tools[:5]):
            print(f"{i+1}. {tool['name']} - {tool['categories']}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()