#!/usr/bin/env python3
"""
Enhanced AI tools parser with improved category extraction.
"""

import json
import os
import re
from typing import List, Dict, Any

def extract_tools_with_categories(content: str, source: str) -> List[Dict[str, Any]]:
    """Enhanced regex extraction with better category detection."""
    tools = []
    
    # Pattern to extract category and tools sections
    category_section_patterns = [
        r'"category":\s*"([^"]+)"[^}]*?"tools":\s*\[(.*?)\]',
        r'"category":\s*"([^"]+)"[^{]*?\{[^}]*?"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"'
    ]
    
    # First try to extract category sections
    for pattern in category_section_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            if len(match) >= 2:
                category = match[0].strip()
                if len(match) == 2:
                    # Tools array format
                    tools_content = match[1]
                    # Extract individual tools from the array
                    tool_matches = re.findall(r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"', tools_content, re.DOTALL)
                    for tool_match in tool_matches:
                        if len(tool_match) >= 3 and tool_match[2].startswith('http'):
                            tools.append({
                                'name': tool_match[0].strip(),
                                'description': tool_match[1].strip(),
                                'link': tool_match[2].strip(),
                                'category': category,
                                'source': source
                            })
                else:
                    # Direct tool format
                    if len(match) >= 4 and match[3].startswith('http'):
                        tools.append({
                            'name': match[1].strip(),
                            'description': match[2].strip(),
                            'link': match[3].strip(),
                            'category': category,
                            'source': source
                        })
    
    # If no category-specific tools found, try general patterns
    if not tools:
        general_patterns = [
            r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"[^}]*?"category":\s*"([^"]*?)"',
            r'"name":\s*"([^"]+)"[^}]*?"description":\s*"([^"]*?)"[^}]*?"link":\s*"([^"]*?)"'
        ]
        
        for pattern in general_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                if len(match) >= 3:
                    name = match[0].strip()
                    description = match[1].strip()
                    link = match[2].strip()
                    category = match[3].strip() if len(match) > 3 else infer_category_from_description(name, description)
                    
                    if name and link and link.startswith('http'):
                        tools.append({
                            'name': name,
                            'description': description,
                            'link': link,
                            'category': category or 'Unknown',
                            'source': source
                        })
    
    return tools

def infer_category_from_description(name: str, description: str) -> str:
    """Infer category from tool name and description."""
    text = (name + " " + description).lower()
    
    # Category mapping based on keywords
    category_keywords = {
        'Writing Tools': ['writing', 'content', 'copy', 'text', 'blog', 'article', 'copywriting', 'grammar'],
        'Developer Tools': ['code', 'coding', 'developer', 'programming', 'api', 'github', 'ide', 'debug'],
        'AI Assistants': ['assistant', 'chat', 'chatbot', 'ai chat', 'conversation'],
        'Image & Design': ['image', 'design', 'visual', 'photo', 'picture', 'graphic', 'logo'],
        'Video Tools': ['video', 'clips', 'editing', 'streaming', 'youtube'],
        'Audio Tools': ['audio', 'voice', 'sound', 'music', 'podcast'],
        'Productivity': ['productivity', 'workflow', 'automation', 'organize', 'notes'],
        'Search Engines': ['search', 'engine', 'find', 'discovery'],
        'Marketing Tools': ['marketing', 'seo', 'social media', 'advertising', 'analytics'],
        'Business Tools': ['business', 'sales', 'crm', 'finance', 'analytics']
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return 'Unknown'

def extract_from_file_enhanced(file_path: str, source: str) -> List[Dict[str, Any]]:
    """Enhanced extraction with multiple strategies."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        raw_content = data.get('raw_content', '')
        if not raw_content:
            return tools
        
        # Strategy 1: Try structured JSON parsing
        try:
            nested_data = json.loads(raw_content)
            tools.extend(extract_from_structured_json(nested_data, source))
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Try partial JSON repair and parsing
        if not tools:
            try:
                repaired_json = repair_truncated_json(raw_content)
                nested_data = json.loads(repaired_json)
                tools.extend(extract_from_structured_json(nested_data, source))
            except:
                pass
        
        # Strategy 3: Regex extraction with category detection
        if not tools:
            tools.extend(extract_tools_with_categories(raw_content, source))
        
        # Strategy 4: Simple regex as fallback
        if not tools:
            simple_pattern = r'"([^"]+)"[^"]*"([^"]*)"[^"]*"(https?://[^"]+)"'
            matches = re.findall(simple_pattern, raw_content)
            for match in matches:
                if len(match) >= 3:
                    tools.append({
                        'name': match[0].strip(),
                        'description': match[1].strip(),
                        'link': match[2].strip(),
                        'category': infer_category_from_description(match[0], match[1]),
                        'source': source
                    })
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return tools

def repair_truncated_json(json_str: str) -> str:
    """Attempt to repair truncated JSON by finding the last complete structure."""
    json_str = json_str.strip()
    
    # Find the last complete brace pair
    brace_count = 0
    bracket_count = 0
    last_valid_pos = -1
    
    for i, char in enumerate(json_str):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        
        # Check if we have balanced braces and brackets
        if brace_count == 0 and bracket_count >= 0:
            last_valid_pos = i
    
    if last_valid_pos > 0:
        json_str = json_str[:last_valid_pos + 1]
        
        # Add closing brackets if needed
        while bracket_count > 0:
            json_str += ']'
            bracket_count -= 1
    
    return json_str

def extract_from_structured_json(data: Dict[str, Any], source: str) -> List[Dict[str, Any]]:
    """Extract from properly structured JSON with category preservation."""
    tools = []
    
    if 'data' not in data:
        return tools
    
    data_section = data['data']
    
    # Handle mahseema structure (categories with tools)
    if 'extracted_information_details' in data_section:
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
    
    # Handle direct tools list with categories
    elif 'tools' in data_section:
        for tool in data_section['tools']:
            if tool.get('name') and tool.get('link'):
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': tool.get('category', 'Unknown'),
                    'source': source
                })
    
    # Handle ai_tools structure
    elif 'ai_tools' in data_section:
        for tool in data_section['ai_tools']:
            if tool.get('name') and tool.get('link'):
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': tool.get('category', 'Unknown'),
                    'source': source
                })
    
    # Handle features structure
    elif 'features' in data_section:
        for tool in data_section['features']:
            if tool.get('name') and tool.get('link'):
                category = tool.get('category')
                if not category:
                    category = infer_category_from_description(tool.get('name', ''), tool.get('description', ''))
                
                tools.append({
                    'name': tool['name'],
                    'description': tool.get('description', ''),
                    'link': tool['link'],
                    'category': category,
                    'source': source
                })
    
    return tools

def clean_and_validate_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enhanced cleaning and validation."""
    cleaned_tools = []
    seen_combinations = set()
    
    for tool in tools:
        # Clean fields
        name = str(tool.get('name', '')).strip()
        description = str(tool.get('description', '')).strip()
        link = str(tool.get('link', '')).strip()
        category = str(tool.get('category', 'Unknown')).strip()
        source = str(tool.get('source', '')).strip()
        
        # Remove markdown formatting
        name = re.sub(r'\*+', '', name).strip()
        description = re.sub(r'\*+', '', description).strip()
        
        # Clean up review links and artifacts
        if description.startswith('[reviews'):
            description = description.split(']')[-1].strip().lstrip('-').strip()
        
        # Skip if invalid
        if not name or not link or not link.startswith(('http://', 'https://')):
            continue
        
        # Skip if name looks like JSON or is too long
        if name.startswith(('{', '[', '"')) or len(name) > 150:
            continue
        
        # Create unique identifier
        unique_id = f"{name.lower().strip()}|{link.lower().strip()}"
        
        if unique_id not in seen_combinations:
            seen_combinations.add(unique_id)
            
            # If category is still Unknown, try to infer it
            if category == 'Unknown':
                category = infer_category_from_description(name, description)
            
            cleaned_tools.append({
                'name': name,
                'description': description,
                'link': link,
                'category': category,
                'source': source
            })
    
    return cleaned_tools

def main():
    """Enhanced main extraction function."""
    print("Starting enhanced AI tools extraction with category detection...")
    
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
            tools = extract_from_file_enhanced(file_path, source)
            all_tools.extend(tools)
            print(f"  ✓ Extracted {len(tools)} tools")
        else:
            print(f"  ❌ File not found")
    
    print(f"\nTotal tools before cleaning: {len(all_tools)}")
    
    # Clean and validate
    cleaned_tools = clean_and_validate_tools(all_tools)
    print(f"Tools after cleaning and validation: {len(cleaned_tools)}")
    
    # Create final output
    final_data = {
        'metadata': {
            'total_tools': len(cleaned_tools),
            'extraction_date': '2025-08-21',
            'extraction_method': 'enhanced_category_detection',
            'sources': [repo[1] for repo in repositories]
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
        
        # Validation and statistics
        print("\nValidation and Statistics:")
        
        categories = {}
        sources = {}
        
        for tool in cleaned_tools:
            category = tool.get('category', 'Unknown')
            source = tool.get('source', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        print(f"Total tools: {len(cleaned_tools)}")
        print(f"Categories: {len(categories)}")
        print(f"Sources: {len(sources)}")
        
        print(f"\nSource distribution:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count} tools")
        
        print(f"\nTop categories:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  {category}: {count} tools")
        
        print(f"\nSample tools by category:")
        samples_shown = set()
        for category in sorted(categories.keys()):
            if category != 'Unknown' and len(samples_shown) < 5:
                for tool in cleaned_tools:
                    if tool['category'] == category and category not in samples_shown:
                        print(f"  [{category}] {tool['name']}: {tool['description'][:60]}...")
                        samples_shown.add(category)
                        break
        
        # Final validation check
        print(f"\nFinal validation:")
        
        # Re-read and validate JSON structure
        with open(output_file, 'r', encoding='utf-8') as f:
            validation_data = json.load(f)
        
        validation_errors = 0
        for tool in validation_data['tools']:
            if not all(k in tool for k in ['name', 'description', 'link', 'category', 'source']):
                validation_errors += 1
            elif not tool['link'].startswith(('http://', 'https://')):
                validation_errors += 1
        
        if validation_errors == 0:
            print("✓ All tools passed final validation")
        else:
            print(f"❌ {validation_errors} tools have validation issues")
        
    except Exception as e:
        print(f"❌ Error in processing: {e}")

if __name__ == "__main__":
    main()
