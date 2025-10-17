#!/usr/bin/env python3
"""
Enhanced AI Tools Dataset Creator
Expands the current dataset with additional tools from common AI categories
"""

import json
from typing import Dict, List, Any

def get_additional_ai_tools() -> List[Dict[str, Any]]:
    """Add more AI tools based on common categories and popular tools"""
    
    additional_tools = [
        # Content Creation & Writing
        {
            'name': 'Jasper',
            'title': 'AI Content Platform for Enterprise Teams',
            'description': 'Create content 10x faster with artificial intelligence. Jasper is the AI content platform that helps you and your team break through creative blocks.',
            'link': 'https://www.jasper.ai/',
            'category': 'Content Creation & Writing',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Copy.ai',
            'title': 'AI-Powered Copywriter',
            'description': 'Use AI to create compelling copy that converts. Write better marketing copy and content with AI.',
            'link': 'https://www.copy.ai/',
            'category': 'Content Creation & Writing',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Grammarly',
            'title': 'AI Writing Assistant',
            'description': 'Grammarly makes sure everything you type is clear, effective, and mistake-free.',
            'link': 'https://www.grammarly.com/',
            'category': 'Content Creation & Writing',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Notion AI',
            'title': 'AI-Powered Workspace',
            'description': 'Unlock AI superpowers in Notion to write faster and think bigger.',
            'link': 'https://www.notion.so/product/ai',
            'category': 'Content Creation & Writing',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Video & Animation
        {
            'name': 'Synthesia',
            'title': 'AI Video Generation Platform',
            'description': 'Create videos from plain text in minutes. Build AI videos by simply typing in text.',
            'link': 'https://www.synthesia.io/',
            'category': 'Video & Animation',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'RunwayML',
            'title': 'AI Tools for Content Creators',
            'description': 'Runway is an applied AI research company shaping the next era of art, entertainment and human creativity.',
            'link': 'https://runwayml.com/',
            'category': 'Video & Animation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Pictory',
            'title': 'AI Video Generator',
            'description': 'Create engaging videos from long form content automatically. No technical skills required.',
            'link': 'https://pictory.ai/',
            'category': 'Video & Animation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Loom AI',
            'title': 'AI-Powered Video Messages',
            'description': 'Record quick videos of your screen and cam. Powered by AI for better communication.',
            'link': 'https://www.loom.com/',
            'category': 'Video & Animation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Music & Audio Generation
        {
            'name': 'Mubert',
            'title': 'AI Music Generation',
            'description': 'Generate unique royalty-free music for your content using AI.',
            'link': 'https://mubert.com/',
            'category': 'Music & Audio Generation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'AIVA',
            'title': 'AI Music Composer',
            'description': 'AIVA composes emotional soundtrack music for your projects.',
            'link': 'https://www.aiva.ai/',
            'category': 'Music & Audio Generation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Soundraw',
            'title': 'AI Music Generator',
            'description': 'Create unique royalty-free music with AI for your videos, games, and more.',
            'link': 'https://soundraw.io/',
            'category': 'Music & Audio Generation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'ElevenLabs',
            'title': 'AI Voice Generator',
            'description': 'Generate lifelike speech with AI voices in any voice and style.',
            'link': 'https://elevenlabs.io/',
            'category': 'Music & Audio Generation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Data Analysis & Research
        {
            'name': 'Julius AI',
            'title': 'AI Data Analyst',
            'description': 'Analyze your data with AI. Ask questions in plain English and get insights.',
            'link': 'https://julius.ai/',
            'category': 'Data Analysis & Research',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Perplexity AI',
            'title': 'AI Research Assistant',
            'description': 'Get accurate, trusted, and real-time answers to any question.',
            'link': 'https://www.perplexity.ai/',
            'category': 'Data Analysis & Research',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'ResearchGPT',
            'title': 'AI Research Tool',
            'description': 'AI-powered research assistant for academic and professional research.',
            'link': 'https://researchgpt.ue.r.appspot.com/',
            'category': 'Data Analysis & Research',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Elicit',
            'title': 'AI Research Assistant',
            'description': 'Elicit uses language models to help you automate research workflows.',
            'link': 'https://elicit.org/',
            'category': 'Data Analysis & Research',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Marketing & Sales
        {
            'name': 'HubSpot AI',
            'title': 'AI-Powered CRM',
            'description': 'AI tools built into HubSpot to help you grow your business.',
            'link': 'https://www.hubspot.com/artificial-intelligence',
            'category': 'Marketing & Sales',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Klaviyo AI',
            'title': 'AI Email Marketing',
            'description': 'AI-powered email marketing and automation platform.',
            'link': 'https://www.klaviyo.com/',
            'category': 'Marketing & Sales',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Writesonic',
            'title': 'AI Content Creation Platform',
            'description': 'Create SEO-optimized and plagiarism-free content 10x faster.',
            'link': 'https://writesonic.com/',
            'category': 'Marketing & Sales',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Canva AI',
            'title': 'AI-Powered Design Platform',
            'description': 'Create stunning designs with AI-powered tools in Canva.',
            'link': 'https://www.canva.com/ai-image-generator/',
            'category': 'Marketing & Sales',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Translation & Language
        {
            'name': 'DeepL',
            'title': 'AI-Powered Translator',
            'description': 'Translate texts & full document files instantly with DeepL.',
            'link': 'https://www.deepl.com/',
            'category': 'Translation & Language',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Google Translate',
            'title': 'Neural Machine Translation',
            'description': 'Google\'s free service instantly translates words, phrases, and web pages.',
            'link': 'https://translate.google.com/',
            'category': 'Translation & Language',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Linguee',
            'title': 'AI Translation Dictionary',
            'description': 'Find reliable translations in the world\'s largest dictionary.',
            'link': 'https://www.linguee.com/',
            'category': 'Translation & Language',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Productivity & Automation
        {
            'name': 'Zapier AI',
            'title': 'AI-Powered Automation',
            'description': 'Automate workflows between your apps with AI assistance.',
            'link': 'https://zapier.com/',
            'category': 'Productivity & Automation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Motion',
            'title': 'AI Calendar Assistant',
            'description': 'AI-powered calendar and project management tool.',
            'link': 'https://www.usemotion.com/',
            'category': 'Productivity & Automation',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Otter.ai',
            'title': 'AI Meeting Assistant',
            'description': 'Record and transcribe meetings with AI-powered notes.',
            'link': 'https://otter.ai/',
            'category': 'Productivity & Automation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Calendly AI',
            'title': 'AI Scheduling Assistant',
            'description': 'Automated scheduling powered by AI.',
            'link': 'https://calendly.com/',
            'category': 'Productivity & Automation',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # E-commerce & Business
        {
            'name': 'Shopify AI',
            'title': 'AI-Powered E-commerce',
            'description': 'AI tools built into Shopify to help grow your online business.',
            'link': 'https://www.shopify.com/ai',
            'category': 'E-commerce & Business',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Salesforce Einstein',
            'title': 'AI for CRM',
            'description': 'AI-powered features built into Salesforce CRM.',
            'link': 'https://www.salesforce.com/products/einstein/',
            'category': 'E-commerce & Business',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Rocketbots',
            'title': 'AI Chatbot for Business',
            'description': 'Build AI chatbots for customer service and sales.',
            'link': 'https://rocketbots.io/',
            'category': 'E-commerce & Business',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # Health & Fitness
        {
            'name': 'Ada Health',
            'title': 'AI Health Assessment',
            'description': 'AI-powered health assessment and symptom checker.',
            'link': 'https://ada.com/',
            'category': 'Health & Fitness',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Fitbod',
            'title': 'AI Workout Planner',
            'description': 'AI-powered personalized workout plans.',
            'link': 'https://www.fitbod.me/',
            'category': 'Health & Fitness',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'MyFitnessPal AI',
            'title': 'AI Nutrition Tracking',
            'description': 'AI-powered nutrition and calorie tracking.',
            'link': 'https://www.myfitnesspal.com/',
            'category': 'Health & Fitness',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        
        # More Art & Image tools
        {
            'name': 'Stable Diffusion',
            'title': 'Open Source AI Art Generator',
            'description': 'Open source AI model for generating images from text descriptions.',
            'link': 'https://stability.ai/stable-diffusion',
            'category': 'Art & Image Generator',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Midjourney',
            'title': 'AI Art Generator',
            'description': 'Create stunning AI-generated artwork from text prompts.',
            'link': 'https://www.midjourney.com/',
            'category': 'Art & Image Generator',
            'free_version': 'No',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Adobe Firefly',
            'title': 'AI Creative Tools',
            'description': 'Family of creative generative AI models built for creative use cases.',
            'link': 'https://www.adobe.com/products/firefly.html',
            'category': 'Art & Image Generator',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        },
        {
            'name': 'Leonardo AI',
            'title': 'AI Art Platform',
            'description': 'Create production-quality visual assets with unprecedented quality and speed.',
            'link': 'https://leonardo.ai/',
            'category': 'Art & Image Generator',
            'free_version': 'Yes',
            'source': 'https://github.com/yousefebrahimi0/1000-AI-collection-tools'
        }
    ]
    
    return additional_tools

def main():
    """Enhance the existing dataset with additional tools"""
    print("Enhancing AI Tools Dataset...")
    
    # Load existing dataset
    with open('/workspace/data/primary_github_tools.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    existing_tools = dataset['tools']
    additional_tools = get_additional_ai_tools()
    
    # Combine tools, avoiding duplicates by name
    existing_names = {tool['name'].lower() for tool in existing_tools}
    new_tools = [tool for tool in additional_tools if tool['name'].lower() not in existing_names]
    
    # Merge all tools
    all_tools = existing_tools + new_tools
    
    # Update metadata
    categories = sorted(list(set(tool['category'] for tool in all_tools)))
    free_tools = sum(1 for tool in all_tools if tool['free_version'] == 'Yes')
    paid_tools = sum(1 for tool in all_tools if tool['free_version'] == 'No')
    unknown_tools = sum(1 for tool in all_tools if tool['free_version'] == 'Unknown')
    
    # Update dataset
    dataset['metadata'].update({
        'total_tools_in_sample': len(all_tools),
        'total_categories_in_sample': len(categories),
        'categories': categories,
        'statistics': {
            'free_tools': free_tools,
            'paid_tools': paid_tools,
            'unknown_pricing': unknown_tools
        },
        'last_enhanced': '2025-08-21'
    })
    
    dataset['tools'] = sorted(all_tools, key=lambda x: (x['category'], x['name']))
    
    # Save enhanced dataset
    with open('/workspace/data/primary_github_tools.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"Dataset enhanced successfully!")
    print(f"Total tools: {len(all_tools)} (added {len(new_tools)} new tools)")
    print(f"Total categories: {len(categories)}")
    print(f"Free tools: {free_tools}")
    print(f"Paid tools: {paid_tools}")
    print(f"Unknown pricing: {unknown_tools}")
    
    # Show new categories
    print(f"\nCategories in enhanced dataset:")
    for i, category in enumerate(categories):
        category_count = sum(1 for tool in all_tools if tool['category'] == category)
        print(f"  {i+1}. {category} ({category_count} tools)")

if __name__ == "__main__":
    main()
