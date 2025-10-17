#!/usr/bin/env python3
"""
Create a curated dataset of 2024-2025 AI tools for AIverse website update.
This script generates a comprehensive JSON dataset with modern AI tools
that were released or significantly updated from 2024-2025.
"""

import json
from datetime import datetime
from typing import Dict, List, Any

def get_category_mapping() -> Dict[str, str]:
    """Map user-provided categories to existing AIverse categories"""
    return {
        "AI Assistants & Chatbots": "Artificial Intelligence",
        "Content Creation & Writing": "Writing", 
        "Image Generation & Editing": "Design",
        "Video Creation & Editing": "Video",
        "Audio & Voice Generation": "Content Creation",
        "Development & Coding": "Developer Tools",
        "Business & Productivity": "Productivity",
        "Marketing & Sales": "Marketing",
        "Design & Graphics": "Design",
        "Automation & Workflows": "Productivity"
    }

def get_2024_2025_ai_tools() -> List[Dict[str, Any]]:
    """Get the curated list of 2024-2025 AI tools based on user requirements"""
    tools = []
    tool_id = 1
    
    # Top Priority Tools (Most Popular/Trending 2024-2025)
    top_priority_tools = [
        {
            "name": "ChatGPT",
            "description": "Leading AI assistant for wide range of tasks, file analysis, summarization, and advanced reasoning with GPT-4 capabilities",
            "link": "https://chatgpt.com",
            "category": "Artificial Intelligence",
            "popularity_score": 10.0,
            "featured": True
        },
        {
            "name": "Claude",
            "description": "Advanced AI assistant optimized for coding, reliable code generation, collaborative communication, and long-form content",
            "link": "https://claude.ai",
            "category": "Artificial Intelligence", 
            "popularity_score": 9.8,
            "featured": True
        },
        {
            "name": "Grok",
            "description": "Uncensored AI assistant integrated with X (Twitter), featuring real-time information and image generation capabilities",
            "link": "https://grok.x.ai",
            "category": "Artificial Intelligence",
            "popularity_score": 9.5,
            "featured": True
        },
        {
            "name": "Gemini",
            "description": "Google's multimodal AI with large context window, audio overview feature, and advanced reasoning capabilities",
            "link": "https://gemini.google.com",
            "category": "Artificial Intelligence",
            "popularity_score": 9.6,
            "featured": True
        },
        {
            "name": "DeepSeek",
            "description": "Fastest growing AI tool with 88.6% popularity increase, offering advanced reasoning and coding capabilities",
            "link": "https://www.deepseek.com",
            "category": "Artificial Intelligence",
            "popularity_score": 9.2,
            "featured": True
        },
        {
            "name": "Perplexity AI",
            "description": "Conversational search engine with 37.7% growth, combining web search with AI reasoning for accurate answers",
            "link": "https://www.perplexity.ai",
            "category": "Artificial Intelligence",
            "popularity_score": 8.9,
            "featured": True
        },
        {
            "name": "Microsoft Copilot",
            "description": "AI-powered productivity tool and conversational chatbot integrated across Microsoft 365 suite",
            "link": "https://copilot.microsoft.com",
            "category": "Productivity",
            "popularity_score": 9.1,
            "featured": True
        },
        {
            "name": "Cursor",
            "description": "AI-powered IDE for writing code with 56% growth, featuring intelligent code completion and pair programming",
            "link": "https://cursor.sh",
            "category": "Developer Tools",
            "popularity_score": 8.8,
            "featured": True
        },
        {
            "name": "NotebookLM",
            "description": "AI note-taking with personal knowledge management and 57% growth, perfect for research and learning",
            "link": "https://notebooklm.google.com",
            "category": "Productivity",
            "popularity_score": 8.7,
            "featured": True
        }
    ]
    
    # Video & Content Creation Tools
    video_content_tools = [
        {
            "name": "Synthesia",
            "description": "Professional AI video generator with realistic avatars for corporate training and marketing content",
            "link": "https://www.synthesia.io",
            "category": "Video",
            "popularity_score": 8.5,
            "featured": False
        },
        {
            "name": "Runway",
            "description": "Advanced AI video generation and editing platform with Gen-3 model for cinematic video creation",
            "link": "https://runwayml.com",
            "category": "Video",
            "popularity_score": 8.6,
            "featured": False
        },
        {
            "name": "OpusClip",
            "description": "AI-powered tool to break longer videos into engaging social media clips with automatic highlighting",
            "link": "https://www.opus.pro",
            "category": "Video",
            "popularity_score": 8.2,
            "featured": False
        },
        {
            "name": "Luma AI",
            "description": "3D model generation and video creation platform with Dream Machine for realistic video synthesis",
            "link": "https://lumalabs.ai",
            "category": "Video",
            "popularity_score": 8.4,
            "featured": False
        },
        {
            "name": "HeyGen",
            "description": "AI avatar video generation platform for creating spokesperson videos with multilingual support",
            "link": "https://www.heygen.com",
            "category": "Video",
            "popularity_score": 8.1,
            "featured": False
        },
        {
            "name": "CapCut",
            "description": "AI video editing platform with automated editing features and social media optimization",
            "link": "https://www.capcut.com",
            "category": "Video",
            "popularity_score": 8.0,
            "featured": False
        },
        {
            "name": "Pictory",
            "description": "AI video creation platform that transforms text and articles into engaging video content",
            "link": "https://pictory.ai",
            "category": "Video",
            "popularity_score": 7.9,
            "featured": False
        },
        {
            "name": "InVideo",
            "description": "Comprehensive AI video generator with templates and automated video creation workflows",
            "link": "https://invideo.io",
            "category": "Video",
            "popularity_score": 7.8,
            "featured": False
        }
    ]
    
    # Image & Design Tools
    image_design_tools = [
        {
            "name": "Midjourney",
            "description": "Leading AI image generation platform with painterly aesthetic and advanced prompt engineering",
            "link": "https://www.midjourney.com",
            "category": "Design",
            "popularity_score": 9.3,
            "featured": True
        },
        {
            "name": "Leonardo",
            "description": "Advanced AI image generation platform with fine-tuned models for different artistic styles",
            "link": "https://leonardo.ai",
            "category": "Design",
            "popularity_score": 8.3,
            "featured": False
        },
        {
            "name": "Canva Magic Studio",
            "description": "AI-powered design suite with automated design generation and smart editing features",
            "link": "https://www.canva.com/magic-studio",
            "category": "Design",
            "popularity_score": 8.4,
            "featured": False
        },
        {
            "name": "Remove.bg",
            "description": "AI background removal tool with instant processing for professional photo editing",
            "link": "https://www.remove.bg",
            "category": "Design",
            "popularity_score": 8.1,
            "featured": False
        },
        {
            "name": "Adobe Firefly",
            "description": "Adobe's AI image generation and editing suite integrated into Creative Cloud applications",
            "link": "https://firefly.adobe.com",
            "category": "Design",
            "popularity_score": 8.5,
            "featured": False
        },
        {
            "name": "Stable Diffusion",
            "description": "Open-source AI image generation model with community-driven improvements and customizations",
            "link": "https://stability.ai/stable-diffusion",
            "category": "Design",
            "popularity_score": 8.7,
            "featured": False
        }
    ]
    
    # Audio & Voice Tools
    audio_voice_tools = [
        {
            "name": "ElevenLabs",
            "description": "Advanced AI voice generation and cloning platform with realistic speech synthesis",
            "link": "https://elevenlabs.io",
            "category": "Content Creation",
            "popularity_score": 8.6,
            "featured": False
        },
        {
            "name": "Murf.ai",
            "description": "Professional AI voice generation platform with clean interface and diverse voice options",
            "link": "https://murf.ai",
            "category": "Content Creation",
            "popularity_score": 8.2,
            "featured": False
        },
        {
            "name": "Suno",
            "description": "AI music generator for creating background music and soundtracks with text prompts",
            "link": "https://www.suno.ai",
            "category": "Content Creation",
            "popularity_score": 8.4,
            "featured": False
        },
        {
            "name": "Udio",
            "description": "AI music generator designed for musicians with advanced composition and arrangement features",
            "link": "https://www.udio.com",
            "category": "Content Creation",
            "popularity_score": 8.1,
            "featured": False
        }
    ]
    
    # Writing & Productivity Tools
    writing_productivity_tools = [
        {
            "name": "Rytr",
            "description": "AI writing assistant optimized for short-form content creation and copywriting",
            "link": "https://rytr.me",
            "category": "Writing",
            "popularity_score": 7.9,
            "featured": False
        },
        {
            "name": "Jasper.ai",
            "description": "Comprehensive AI marketing content creation platform for campaigns and brand messaging",
            "link": "https://www.jasper.ai",
            "category": "Writing",
            "popularity_score": 8.3,
            "featured": False
        },
        {
            "name": "QuillBot",
            "description": "AI writing enhancement and paraphrasing tool for improving content quality and clarity",
            "link": "https://quillbot.com",
            "category": "Writing",
            "popularity_score": 8.0,
            "featured": False
        },
        {
            "name": "Grammarly",
            "description": "Advanced AI writing assistant and grammar checker with tone and style suggestions",
            "link": "https://www.grammarly.com",
            "category": "Writing",
            "popularity_score": 8.8,
            "featured": True
        },
        {
            "name": "Copy.ai",
            "description": "AI copywriting tool for marketing content, social media posts, and business communications",
            "link": "https://www.copy.ai",
            "category": "Writing",
            "popularity_score": 8.1,
            "featured": False
        },
        {
            "name": "Sudowrite",
            "description": "Creative writing assistant specifically designed for fiction writers and storytellers",
            "link": "https://www.sudowrite.com",
            "category": "Writing",
            "popularity_score": 7.8,
            "featured": False
        }
    ]
    
    # Automation & Development Tools
    automation_dev_tools = [
        {
            "name": "n8n",
            "description": "Visual workflow automation tool with AI integrations for business process automation",
            "link": "https://n8n.io",
            "category": "Productivity",
            "popularity_score": 8.2,
            "featured": False
        },
        {
            "name": "Zapier",
            "description": "Automation platform with AI features for connecting apps and automating workflows",
            "link": "https://zapier.com",
            "category": "Productivity",
            "popularity_score": 8.5,
            "featured": False
        },
        {
            "name": "Replit",
            "description": "AI-powered coding environment with collaborative development and instant deployment",
            "link": "https://replit.com",
            "category": "Developer Tools",
            "popularity_score": 8.1,
            "featured": False
        },
        {
            "name": "Lovable",
            "description": "Build complete software applications by prompting with natural language descriptions",
            "link": "https://lovable.dev",
            "category": "Developer Tools",
            "popularity_score": 7.9,
            "featured": False
        },
        {
            "name": "Manus",
            "description": "AI agent platform for automating various business tasks and workflows",
            "link": "https://www.manus.ai",
            "category": "Productivity",
            "popularity_score": 7.7,
            "featured": False
        },
        {
            "name": "GitHub Copilot",
            "description": "AI pair programming assistant integrated into development environments for code completion",
            "link": "https://github.com/features/copilot",
            "category": "Developer Tools",
            "popularity_score": 8.7,
            "featured": False
        }
    ]
    
    # Business & Marketing Tools
    business_marketing_tools = [
        {
            "name": "AdCreative",
            "description": "AI-powered ad creative generation platform for performance marketing campaigns",
            "link": "https://www.adcreative.ai",
            "category": "Marketing",
            "popularity_score": 8.0,
            "featured": False
        },
        {
            "name": "HubSpot AI Email Writer",
            "description": "AI email campaign creation tool integrated into HubSpot's marketing automation platform",
            "link": "https://www.hubspot.com/artificial-intelligence",
            "category": "Marketing",
            "popularity_score": 7.9,
            "featured": False
        },
        {
            "name": "Gamma",
            "description": "AI presentation builder that creates beautiful slides from text prompts and outlines",
            "link": "https://gamma.app",
            "category": "Productivity",
            "popularity_score": 8.2,
            "featured": False
        },
        {
            "name": "Notion AI",
            "description": "AI-enhanced knowledge management and productivity suite with intelligent content creation",
            "link": "https://www.notion.so/product/ai",
            "category": "Productivity",
            "popularity_score": 8.4,
            "featured": False
        },
        {
            "name": "Fathom",
            "description": "AI meeting notetaker that automatically records, transcribes, and summarizes meetings",
            "link": "https://fathom.video",
            "category": "Productivity",
            "popularity_score": 7.8,
            "featured": False
        },
        {
            "name": "Reclaim",
            "description": "AI scheduling assistant that optimizes calendar management and time blocking",
            "link": "https://reclaim.ai",
            "category": "Productivity",
            "popularity_score": 7.6,
            "featured": False
        }
    ]
    
    # Emerging & Specialized Tools
    emerging_specialized_tools = [
        {
            "name": "Character.ai",
            "description": "AI character chatbot platform for creating and conversing with custom AI personalities",
            "link": "https://character.ai",
            "category": "Chatbots",
            "popularity_score": 8.0,
            "featured": False
        },
        {
            "name": "Poe",
            "description": "AI chatbot aggregator by Quora providing access to multiple AI models in one platform",
            "link": "https://poe.com",
            "category": "Chatbots",
            "popularity_score": 7.9,
            "featured": False
        },
        {
            "name": "DeepAI",
            "description": "Comprehensive collection of AI tools for image generation, text processing, and analysis",
            "link": "https://deepai.org",
            "category": "Artificial Intelligence",
            "popularity_score": 7.7,
            "featured": False
        },
        {
            "name": "Hugging Face",
            "description": "Leading AI model platform and community for sharing, training, and deploying machine learning models",
            "link": "https://huggingface.co",
            "category": "Developer Tools",
            "popularity_score": 8.6,
            "featured": False
        },
        {
            "name": "Google AI Studio",
            "description": "AI development platform with 80% growth for building and prototyping with Google's AI models",
            "link": "https://aistudio.google.com",
            "category": "Developer Tools",
            "popularity_score": 8.3,
            "featured": False
        },
        {
            "name": "Groq",
            "description": "High-speed AI inference platform optimized for real-time AI applications and responses",
            "link": "https://groq.com",
            "category": "Developer Tools",
            "popularity_score": 8.1,
            "featured": False
        }
    ]
    
    # Combine all tool categories
    all_tool_categories = [
        top_priority_tools,
        video_content_tools,
        image_design_tools,
        audio_voice_tools,
        writing_productivity_tools,
        automation_dev_tools,
        business_marketing_tools,
        emerging_specialized_tools
    ]
    
    # Process each tool and assign IDs
    for category_tools in all_tool_categories:
        for tool in category_tools:
            tool_entry = {
                "id": tool_id,
                "name": tool["name"],
                "description": tool["description"],
                "link": tool["link"],
                "category": tool["category"],
                "logo_url": f"https://logo.clearbit.com/{tool['link'].split('//')[1].split('/')[0]}",
                "screenshot_url": f"https://image.thum.io/get/fullpage/{tool['link']}",
                "featured": tool.get("featured", False),
                "popularity_score": tool["popularity_score"],
                "source": "2024_2025_curated_collection",
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": datetime.now().isoformat() + "Z"
            }
            tools.append(tool_entry)
            tool_id += 1
    
    return tools

def create_dataset():
    """Create the complete 2024-2025 AI tools dataset"""
    tools = get_2024_2025_ai_tools()
    
    # Create metadata
    categories = list(set([tool["category"] for tool in tools]))
    
    dataset = {
        "metadata": {
            "title": "AIverse - 2024-2025 AI Tools Collection",
            "description": "A curated collection of trending AI tools released or significantly updated in 2024-2025",
            "version": "2.0",
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "total_tools": len(tools),
            "categories": sorted(categories),
            "curation_criteria": [
                "Released or significantly updated in 2024-2025",
                "High popularity and user adoption",
                "Active development and community",
                "Professional-grade functionality",
                "Comprehensive feature set"
            ],
            "source": "Curated from Synthesia, Exploding Topics, Insidr AI, and Aixploria research",
            "featured_tools_count": len([t for t in tools if t.get("featured", False)])
        },
        "tools": tools
    }
    
    return dataset

if __name__ == "__main__":
    # Create the dataset
    dataset = create_dataset()
    
    # Save to file
    output_file = "/workspace/aiverse_tools_2024_2025.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 2024-2025 AI Tools dataset created successfully!")
    print(f"📊 Total tools: {dataset['metadata']['total_tools']}")
    print(f"🎯 Featured tools: {dataset['metadata']['featured_tools_count']}")
    print(f"📂 Categories: {len(dataset['metadata']['categories'])}")
    print(f"💾 Saved to: {output_file}")
    
    # Display category breakdown
    print("\n📋 Category Distribution:")
    category_counts = {}
    for tool in dataset['tools']:
        cat = tool['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for category, count in sorted(category_counts.items()):
        print(f"  • {category}: {count} tools")
    
    print("\n🌟 Featured Tools:")
    featured_tools = [t for t in dataset['tools'] if t.get('featured', False)]
    for tool in sorted(featured_tools, key=lambda x: x['popularity_score'], reverse=True):
        print(f"  • {tool['name']} - {tool['popularity_score']}/10.0")
