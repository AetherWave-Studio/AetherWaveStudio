#!/usr/bin/env python3
"""
Comprehensive Markdown Parser for GitHub AI Tools Repository
Parses the complete README.md file to extract all 1000+ AI tools
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any

def parse_markdown_tables(content: str) -> List[Dict[str, Any]]:
    """Parse markdown content to extract all AI tools from tables"""
    tools = []
    lines = content.split('\n')
    
    current_category = None
    in_table = False
    header_processed = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Check for category headers (### Category Name)
        if line.startswith('### '):
            current_category = line[4:].strip()
            in_table = False
            header_processed = False
            continue
        
        # Check for table headers
        if '| Name |' in line and '| Title |' in line:
            in_table = True
            header_processed = False
            continue
        
        # Skip table separator line
        if in_table and not header_processed and '|---|' in line:
            header_processed = True
            continue
        
        # Process table rows
        if in_table and header_processed and line.startswith('|') and line.endswith('|'):
            tool = parse_table_row(line, current_category)
            if tool:
                tools.append(tool)
    
    return tools

def parse_table_row(line: str, category: str) -> Dict[str, Any]:
    """Parse a single table row to extract tool information"""
    # Split by | and clean up
    parts = [part.strip() for part in line.split('|')[1:-1]]  # Remove empty first and last parts
    
    if len(parts) < 4:
        return None
    
    name_part = parts[0].strip()
    title = parts[1].strip()
    description = parts[2].strip()
    free_version_part = parts[3].strip()
    
    # Extract name and link from markdown link format [Name](URL)
    name_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', name_part)
    if name_match:
        name = name_match.group(1).strip()
        link = name_match.group(2).strip()
    else:
        # Fallback if not in link format
        name = name_part
        link = ""
    
    # Convert emoji to text for free version
    free_version = convert_emoji_to_text(free_version_part)
    
    # Clean description
    if description == "." or description == "":
        description = "No description available"
    
    return {
        "name": name,
        "title": title,
        "description": description,
        "link": clean_url(link),
        "category": category or "Uncategorized",
        "free_version": free_version,
        "source": "https://github.com/yousefebrahimi0/1000-AI-collection-tools"
    }

def convert_emoji_to_text(emoji_text: str) -> str:
    """Convert emoji indicators to text"""
    emoji_text = emoji_text.strip()
    
    if ':white_check_mark:' in emoji_text or '✅' in emoji_text:
        return "Yes"
    elif ':x:' in emoji_text or '❌' in emoji_text:
        return "No"
    elif ':grey_question:' in emoji_text or '❔' in emoji_text:
        return "Unknown"
    else:
        return "Unknown"

def clean_url(url: str) -> str:
    """Clean and normalize URLs"""
    if not url:
        return ""
    
    # Remove any extra spaces
    url = url.strip()
    
    # Ensure URLs have proper protocol
    if url.startswith('http://') or url.startswith('https://'):
        return url
    elif url.startswith('//'):
        return f"https:{url}"
    else:
        return f"https://{url}"

def create_comprehensive_dataset():
    """Create the comprehensive AI tools dataset from markdown"""
    print("📖 Reading original README.md file...")
    
    try:
        with open('/workspace/download/original_readme.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    print("🔍 Parsing markdown tables...")
    tools_list = parse_markdown_tables(content)
    
    print(f"✅ Successfully parsed {len(tools_list)} tools!")
    
    # Create comprehensive dataset structure
    dataset = {
        "metadata": {
            "source_repository": "https://github.com/yousefebrahimi0/1000-AI-collection-tools",
            "description": "Complete collection of 1000+ AI tools extracted from the GitHub repository README.md",
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "extraction_method": "comprehensive_markdown_parsing",
            "total_tools": len(tools_list),
            "data_format": "Complete extraction with structured parsing of markdown tables",
            "original_file_size": "176KB",
            "original_file_lines": 1204
        },
        "tools": tools_list
    }
    
    # Generate category statistics
    category_stats = {}
    free_version_stats = {"Yes": 0, "No": 0, "Unknown": 0}
    
    for tool in tools_list:
        category = tool["category"]
        category_stats[category] = category_stats.get(category, 0) + 1
        
        free_version = tool["free_version"]
        if free_version in free_version_stats:
            free_version_stats[free_version] += 1
    
    dataset["metadata"]["categories"] = list(category_stats.keys())
    dataset["metadata"]["category_distribution"] = category_stats
    dataset["metadata"]["total_categories"] = len(category_stats)
    dataset["metadata"]["free_version_distribution"] = free_version_stats
    
    # Save the dataset
    output_file = '/workspace/data/primary_github_tools.json'
    print(f"💾 Saving comprehensive dataset to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 SUCCESS! Comprehensive AI Tools Dataset Created!")
    print(f"📊 Total tools: {len(tools_list)}")
    print(f"📂 Total categories: {len(category_stats)}")
    print(f"🆓 Free tools: {free_version_stats['Yes']}")
    print(f"💰 Paid tools: {free_version_stats['No']}")
    print(f"❓ Unknown pricing: {free_version_stats['Unknown']}")
    print(f"🔗 Source: https://github.com/yousefebrahimi0/1000-AI-collection-tools")
    
    # Display top categories
    print(f"\n📈 Top 15 categories by tool count:")
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    for i, (category, count) in enumerate(sorted_categories[:15], 1):
        print(f"   {i:2d}. {category}: {count} tools")
    
    # Show some sample tools
    print(f"\n🔍 Sample tools:")
    for i, tool in enumerate(tools_list[:5], 1):
        print(f"   {i}. {tool['name']} - {tool['category']}")
        print(f"      {tool['description'][:80]}...")
        print(f"      {tool['link']}")
        print()
    
    return dataset

if __name__ == "__main__":
    create_comprehensive_dataset()
