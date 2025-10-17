#!/usr/bin/env python3
"""
Expanded 2024-2025 AI Tools Dataset Creator
This creates a comprehensive dataset with additional tools to provide a robust directory.
"""

import json
from datetime import datetime
from typing import Dict, List, Any

def get_expanded_2024_2025_tools() -> List[Dict[str, Any]]:
    """Comprehensive list of 2024-2025 AI tools with additional entries"""
    tools = []
    tool_id = 1
    
    # TOP PRIORITY TOOLS (Most Popular/Trending 2024-2025)
    top_priority_tools = [
        {"name": "ChatGPT", "description": "Leading AI assistant for wide range of tasks, file analysis, summarization, and advanced reasoning with GPT-4o capabilities", "link": "https://chatgpt.com", "category": "Artificial Intelligence", "popularity_score": 10.0, "featured": True},
        {"name": "Claude", "description": "Advanced AI assistant by Anthropic optimized for coding, reliable code generation, collaborative communication, and long-form content analysis", "link": "https://claude.ai", "category": "Artificial Intelligence", "popularity_score": 9.8, "featured": True},
        {"name": "Grok", "description": "Uncensored AI assistant integrated with X (Twitter), featuring real-time information access and image generation capabilities", "link": "https://grok.x.ai", "category": "Artificial Intelligence", "popularity_score": 9.5, "featured": True},
        {"name": "Gemini", "description": "Google's multimodal AI with 2M token context window, audio overview feature, and advanced reasoning capabilities across text, image, and code", "link": "https://gemini.google.com", "category": "Artificial Intelligence", "popularity_score": 9.6, "featured": True},
        {"name": "DeepSeek", "description": "Fastest growing AI tool with 88.6% popularity increase in 2024, offering advanced reasoning and coding capabilities with competitive performance", "link": "https://www.deepseek.com", "category": "Artificial Intelligence", "popularity_score": 9.2, "featured": True},
        {"name": "Perplexity AI", "description": "Conversational search engine with 37.7% growth in 2024, combining web search with AI reasoning for accurate, sourced answers", "link": "https://www.perplexity.ai", "category": "Artificial Intelligence", "popularity_score": 8.9, "featured": True},
        {"name": "Microsoft Copilot", "description": "AI-powered productivity tool and conversational chatbot integrated across Microsoft 365 suite with enterprise-grade security", "link": "https://copilot.microsoft.com", "category": "Productivity", "popularity_score": 9.1, "featured": True},
        {"name": "Cursor", "description": "AI-powered IDE for writing code with 56% growth in 2024, featuring intelligent code completion, chat-based programming, and pair programming", "link": "https://cursor.sh", "category": "Developer Tools", "popularity_score": 8.8, "featured": True},
        {"name": "NotebookLM", "description": "Google's AI note-taking with personal knowledge management and 57% growth in 2024, perfect for research and collaborative learning", "link": "https://notebooklm.google.com", "category": "Productivity", "popularity_score": 8.7, "featured": True}
    ]
    
    # VIDEO & CONTENT CREATION TOOLS (Expanded)
    video_content_tools = [
        {"name": "Synthesia", "description": "Professional AI video generator with photorealistic avatars for corporate training, marketing content, and multilingual videos", "link": "https://www.synthesia.io", "category": "Video", "popularity_score": 8.5},
        {"name": "Runway", "description": "Advanced AI video generation and editing platform with Gen-3 model for cinematic video creation and motion graphics", "link": "https://runwayml.com", "category": "Video", "popularity_score": 8.6},
        {"name": "OpusClip", "description": "AI-powered tool to break longer videos into engaging social media clips with automatic highlighting and viral score prediction", "link": "https://www.opus.pro", "category": "Video", "popularity_score": 8.2},
        {"name": "Luma AI", "description": "3D model generation and video creation platform with Dream Machine for realistic video synthesis from text prompts", "link": "https://lumalabs.ai", "category": "Video", "popularity_score": 8.4},
        {"name": "HeyGen", "description": "AI avatar video generation platform for creating spokesperson videos with multilingual support and emotion control", "link": "https://www.heygen.com", "category": "Video", "popularity_score": 8.1},
        {"name": "CapCut", "description": "AI video editing platform with automated editing features, background removal, and social media optimization", "link": "https://www.capcut.com", "category": "Video", "popularity_score": 8.0},
        {"name": "Pictory", "description": "AI video creation platform that transforms text articles and blog posts into engaging video content with voiceovers", "link": "https://pictory.ai", "category": "Video", "popularity_score": 7.9},
        {"name": "InVideo", "description": "Comprehensive AI video generator with 5000+ templates and automated video creation workflows for marketing", "link": "https://invideo.io", "category": "Video", "popularity_score": 7.8},
        {"name": "Descript", "description": "All-in-one AI video editor with transcription, overdub voice cloning, and collaborative editing features", "link": "https://www.descript.com", "category": "Video", "popularity_score": 8.3},
        {"name": "Fliki", "description": "AI video creation platform that converts text to video with realistic AI voices in multiple languages", "link": "https://fliki.ai", "category": "Video", "popularity_score": 7.7},
        {"name": "Steve AI", "description": "AI video maker that creates animated and live-action videos from text scripts with customizable characters", "link": "https://www.steve.ai", "category": "Video", "popularity_score": 7.5},
        {"name": "Wondershare Filmora", "description": "AI-powered video editing software with automatic scene detection, smart cutout, and AI music generation", "link": "https://filmora.wondershare.com", "category": "Video", "popularity_score": 7.6}
    ]
    
    # IMAGE & DESIGN TOOLS (Expanded)
    image_design_tools = [
        {"name": "Midjourney", "description": "Leading AI image generation platform with painterly aesthetic, advanced prompt engineering, and community-driven improvements", "link": "https://www.midjourney.com", "category": "Design", "popularity_score": 9.3, "featured": True},
        {"name": "Leonardo", "description": "Advanced AI image generation platform with fine-tuned models for different artistic styles and commercial use rights", "link": "https://leonardo.ai", "category": "Design", "popularity_score": 8.3},
        {"name": "Canva Magic Studio", "description": "AI-powered design suite with automated design generation, background removal, and smart editing features", "link": "https://www.canva.com/magic-studio", "category": "Design", "popularity_score": 8.4},
        {"name": "Remove.bg", "description": "AI background removal tool with instant processing for professional photo editing and batch processing", "link": "https://www.remove.bg", "category": "Design", "popularity_score": 8.1},
        {"name": "Adobe Firefly", "description": "Adobe's AI image generation and editing suite integrated into Creative Cloud with commercial safety guarantees", "link": "https://firefly.adobe.com", "category": "Design", "popularity_score": 8.5},
        {"name": "Stable Diffusion", "description": "Open-source AI image generation model with community-driven improvements, ControlNet support, and unlimited customizations", "link": "https://stability.ai/stable-diffusion", "category": "Design", "popularity_score": 8.7},
        {"name": "DALL-E 3", "description": "OpenAI's latest image generation model integrated with ChatGPT, offering photorealistic and artistic image creation", "link": "https://openai.com/dall-e-3", "category": "Design", "popularity_score": 8.9},
        {"name": "Figma AI", "description": "AI-powered design assistance integrated into Figma with automated layout suggestions and design system generation", "link": "https://www.figma.com/ai", "category": "Design", "popularity_score": 8.0},
        {"name": "Krea AI", "description": "Real-time AI image generation platform with live canvas editing and instant visual feedback", "link": "https://www.krea.ai", "category": "Design", "popularity_score": 7.8},
        {"name": "Ideogram", "description": "AI image generator specializing in text rendering within images and graphic design elements", "link": "https://ideogram.ai", "category": "Design", "popularity_score": 7.9},
        {"name": "Adobe Express", "description": "AI-powered design platform with quick actions, template customization, and social media optimization", "link": "https://www.adobe.com/express", "category": "Design", "popularity_score": 7.7},
        {"name": "Recraft", "description": "AI design tool for creating brand-consistent graphics, illustrations, and marketing materials with style control", "link": "https://www.recraft.ai", "category": "Design", "popularity_score": 7.6}
    ]
    
    # AUDIO & VOICE TOOLS (Expanded)
    audio_voice_tools = [
        {"name": "ElevenLabs", "description": "Leading AI voice generation and cloning platform with realistic speech synthesis and emotion control for content creation", "link": "https://elevenlabs.io", "category": "Content Creation", "popularity_score": 8.6},
        {"name": "Murf.ai", "description": "Professional AI voice generation platform with clean interface, diverse voice options, and commercial licensing", "link": "https://murf.ai", "category": "Content Creation", "popularity_score": 8.2},
        {"name": "Suno", "description": "AI music generator for creating background music, soundtracks, and complete songs with text prompts and style control", "link": "https://www.suno.ai", "category": "Content Creation", "popularity_score": 8.4},
        {"name": "Udio", "description": "AI music generator designed for musicians with advanced composition, arrangement features, and professional audio quality", "link": "https://www.udio.com", "category": "Content Creation", "popularity_score": 8.1},
        {"name": "Speechify", "description": "AI text-to-speech platform with natural voices, speed control, and integration across devices for accessibility", "link": "https://speechify.com", "category": "Content Creation", "popularity_score": 7.9},
        {"name": "Play.ht", "description": "AI voice generator with ultra-realistic voices, emotion control, and API access for developers and content creators", "link": "https://play.ht", "category": "Content Creation", "popularity_score": 7.8},
        {"name": "Resemble AI", "description": "AI voice cloning platform with real-time voice conversion and custom voice model training capabilities", "link": "https://www.resemble.ai", "category": "Content Creation", "popularity_score": 7.7},
        {"name": "AIVA", "description": "AI music composition platform for creating original soundtracks, theme music, and background scores for media", "link": "https://www.aiva.ai", "category": "Content Creation", "popularity_score": 7.5},
        {"name": "Soundraw", "description": "AI music generator for content creators with royalty-free music creation and customizable track elements", "link": "https://soundraw.io", "category": "Content Creation", "popularity_score": 7.4},
        {"name": "Krisp", "description": "AI-powered noise cancellation and voice enhancement tool for professional meetings and content recording", "link": "https://krisp.ai", "category": "Content Creation", "popularity_score": 7.6}
    ]
    
    # WRITING & PRODUCTIVITY TOOLS (Expanded)
    writing_productivity_tools = [
        {"name": "Grammarly", "description": "Advanced AI writing assistant and grammar checker with tone detection, style suggestions, and plagiarism detection", "link": "https://www.grammarly.com", "category": "Writing", "popularity_score": 8.8, "featured": True},
        {"name": "Jasper.ai", "description": "Comprehensive AI marketing content creation platform for campaigns, blog posts, and brand messaging with brand voice training", "link": "https://www.jasper.ai", "category": "Writing", "popularity_score": 8.3},
        {"name": "Copy.ai", "description": "AI copywriting tool for marketing content, social media posts, email campaigns, and business communications", "link": "https://www.copy.ai", "category": "Writing", "popularity_score": 8.1},
        {"name": "QuillBot", "description": "AI writing enhancement and paraphrasing tool for improving content quality, clarity, and avoiding plagiarism", "link": "https://quillbot.com", "category": "Writing", "popularity_score": 8.0},
        {"name": "Rytr", "description": "AI writing assistant optimized for short-form content creation, copywriting, and social media posts with tone control", "link": "https://rytr.me", "category": "Writing", "popularity_score": 7.9},
        {"name": "Sudowrite", "description": "Creative writing assistant specifically designed for fiction writers, novelists, and storytellers with plot development", "link": "https://www.sudowrite.com", "category": "Writing", "popularity_score": 7.8},
        {"name": "Writesonic", "description": "AI content creation platform for articles, ads, emails, and website copy with SEO optimization features", "link": "https://writesonic.com", "category": "Writing", "popularity_score": 7.7},
        {"name": "Wordtune", "description": "AI writing companion that helps rewrite and improve sentences for clarity, tone, and impact in real-time", "link": "https://www.wordtune.com", "category": "Writing", "popularity_score": 7.6},
        {"name": "Lex", "description": "AI-powered writing tool designed for long-form content with collaborative features and intelligent suggestions", "link": "https://lex.page", "category": "Writing", "popularity_score": 7.4},
        {"name": "Jenni AI", "description": "AI writing assistant for academic and research writing with citation management and plagiarism checking", "link": "https://jenni.ai", "category": "Writing", "popularity_score": 7.5},
        {"name": "ProWritingAid", "description": "AI-powered writing editor with in-depth analysis, style improvement suggestions, and comprehensive writing reports", "link": "https://prowritingaid.com", "category": "Writing", "popularity_score": 7.3},
        {"name": "Hypotenuse AI", "description": "AI content generator for e-commerce, marketing copy, and product descriptions with bulk content creation", "link": "https://www.hypotenuse.ai", "category": "Writing", "popularity_score": 7.2}
    ]
    
    # AUTOMATION & DEVELOPMENT TOOLS (Expanded)
    automation_dev_tools = [
        {"name": "GitHub Copilot", "description": "AI pair programming assistant integrated into development environments for intelligent code completion and generation", "link": "https://github.com/features/copilot", "category": "Developer Tools", "popularity_score": 8.7},
        {"name": "Replit", "description": "AI-powered coding environment with collaborative development, instant deployment, and intelligent code assistance", "link": "https://replit.com", "category": "Developer Tools", "popularity_score": 8.1},
        {"name": "Tabnine", "description": "AI code completion platform that works across IDEs with context-aware suggestions and team learning", "link": "https://www.tabnine.com", "category": "Developer Tools", "popularity_score": 7.8},
        {"name": "CodeT5", "description": "AI code generation and understanding model for multiple programming languages with code summarization", "link": "https://github.com/salesforce/CodeT5", "category": "Developer Tools", "popularity_score": 7.5},
        {"name": "Codeium", "description": "Free AI code completion tool with support for 70+ programming languages and IDE integrations", "link": "https://codeium.com", "category": "Developer Tools", "popularity_score": 7.7},
        {"name": "Lovable", "description": "Build complete software applications by prompting with natural language descriptions and visual requirements", "link": "https://lovable.dev", "category": "Developer Tools", "popularity_score": 7.9},
        {"name": "v0 by Vercel", "description": "AI-powered web development tool that generates React components and complete applications from prompts", "link": "https://v0.dev", "category": "Developer Tools", "popularity_score": 8.0},
        {"name": "CodeWP", "description": "AI code generator specifically for WordPress development with plugin creation and theme customization", "link": "https://codewp.ai", "category": "Developer Tools", "popularity_score": 7.3},
        {"name": "Hugging Face", "description": "Leading AI model platform and community for sharing, training, and deploying machine learning models and datasets", "link": "https://huggingface.co", "category": "Developer Tools", "popularity_score": 8.6},
        {"name": "Google AI Studio", "description": "AI development platform with 80% growth for building and prototyping with Google's Gemini and PaLM models", "link": "https://aistudio.google.com", "category": "Developer Tools", "popularity_score": 8.3},
        {"name": "Groq", "description": "High-speed AI inference platform optimized for real-time AI applications with ultra-low latency responses", "link": "https://groq.com", "category": "Developer Tools", "popularity_score": 8.1},
        {"name": "Anthropic Claude API", "description": "Enterprise API access to Claude AI with enhanced safety, constitutional AI training, and developer tools", "link": "https://www.anthropic.com/api", "category": "Developer Tools", "popularity_score": 8.4}
    ]
    
    # BUSINESS & PRODUCTIVITY TOOLS (Expanded)
    business_productivity_tools = [
        {"name": "Notion AI", "description": "AI-enhanced knowledge management and productivity suite with intelligent content creation and database automation", "link": "https://www.notion.so/product/ai", "category": "Productivity", "popularity_score": 8.4},
        {"name": "Zapier", "description": "Automation platform with AI features for connecting 5000+ apps and automating complex business workflows", "link": "https://zapier.com", "category": "Productivity", "popularity_score": 8.5},
        {"name": "n8n", "description": "Visual workflow automation tool with AI integrations, self-hosted options, and advanced business process automation", "link": "https://n8n.io", "category": "Productivity", "popularity_score": 8.2},
        {"name": "Gamma", "description": "AI presentation builder that creates beautiful slides, documents, and websites from text prompts and outlines", "link": "https://gamma.app", "category": "Productivity", "popularity_score": 8.2},
        {"name": "Fathom", "description": "AI meeting notetaker that automatically records, transcribes, summarizes, and creates action items from meetings", "link": "https://fathom.video", "category": "Productivity", "popularity_score": 7.8},
        {"name": "Reclaim", "description": "AI scheduling assistant that optimizes calendar management, time blocking, and work-life balance automatically", "link": "https://reclaim.ai", "category": "Productivity", "popularity_score": 7.6},
        {"name": "Otter.ai", "description": "AI meeting transcription and note-taking platform with real-time collaboration and automated summaries", "link": "https://otter.ai", "category": "Productivity", "popularity_score": 8.0},
        {"name": "Calendly AI", "description": "AI-powered scheduling platform with smart meeting optimization and automated follow-up management", "link": "https://calendly.com", "category": "Productivity", "popularity_score": 7.5},
        {"name": "Taskade", "description": "AI-powered productivity platform combining task management, mind mapping, and collaborative workspaces with AI automation", "link": "https://www.taskade.com", "category": "Productivity", "popularity_score": 7.4},
        {"name": "Manus", "description": "AI agent platform for automating various business tasks, workflows, and repetitive processes across teams", "link": "https://www.manus.ai", "category": "Productivity", "popularity_score": 7.7},
        {"name": "Monday.com AI", "description": "AI-enhanced project management platform with automated workflows, predictive analytics, and smart task assignment", "link": "https://monday.com", "category": "Productivity", "popularity_score": 7.3},
        {"name": "Clickup AI", "description": "AI-powered project management with automated task creation, smart scheduling, and intelligent progress tracking", "link": "https://clickup.com/ai", "category": "Productivity", "popularity_score": 7.6}
    ]
    
    # MARKETING & SALES TOOLS (Expanded)
    marketing_sales_tools = [
        {"name": "AdCreative", "description": "AI-powered ad creative generation platform for performance marketing campaigns with conversion optimization", "link": "https://www.adcreative.ai", "category": "Marketing", "popularity_score": 8.0},
        {"name": "HubSpot AI", "description": "AI-enhanced CRM and marketing automation platform with lead scoring, content generation, and sales insights", "link": "https://www.hubspot.com/artificial-intelligence", "category": "Marketing", "popularity_score": 7.9},
        {"name": "Persado", "description": "AI-powered marketing language optimization platform that generates high-converting marketing copy and messaging", "link": "https://www.persado.com", "category": "Marketing", "popularity_score": 7.7},
        {"name": "Phrasee", "description": "AI copywriting platform specialized in email subject lines, social media posts, and marketing copy optimization", "link": "https://phrasee.co", "category": "Marketing", "popularity_score": 7.5},
        {"name": "Patterns", "description": "AI-powered ecommerce marketing platform with automated product recommendations and personalization", "link": "https://patterns.app", "category": "Marketing", "popularity_score": 7.4},
        {"name": "Seventh Sense", "description": "AI email delivery optimization platform that uses machine learning to improve open rates and engagement", "link": "https://www.theseventhsense.com", "category": "Marketing", "popularity_score": 7.3},
        {"name": "Brandwatch", "description": "AI-powered social media monitoring and consumer intelligence platform with sentiment analysis and trend detection", "link": "https://www.brandwatch.com", "category": "Marketing", "popularity_score": 7.6},
        {"name": "Albert AI", "description": "Autonomous AI marketing platform that manages and optimizes digital advertising campaigns across channels", "link": "https://albert.ai", "category": "Marketing", "popularity_score": 7.2},
        {"name": "Seamless.AI", "description": "AI-powered sales prospecting platform for finding verified contact information and building targeted lead lists", "link": "https://seamless.ai", "category": "Sales", "popularity_score": 7.8},
        {"name": "Gong", "description": "AI revenue intelligence platform that analyzes sales conversations to improve deal outcomes and team performance", "link": "https://www.gong.io", "category": "Sales", "popularity_score": 8.1},
        {"name": "Outreach", "description": "AI-powered sales engagement platform with automated sequences, conversation intelligence, and pipeline management", "link": "https://www.outreach.io", "category": "Sales", "popularity_score": 7.9},
        {"name": "Chorus", "description": "AI conversation analytics platform for sales teams with call recording, coaching insights, and deal risk analysis", "link": "https://www.chorus.ai", "category": "Sales", "popularity_score": 7.7}
    ]
    
    # CHATBOTS & CUSTOMER SUPPORT (Expanded)
    chatbots_support_tools = [
        {"name": "Character.ai", "description": "AI character chatbot platform for creating and conversing with custom AI personalities for entertainment and education", "link": "https://character.ai", "category": "Chatbots", "popularity_score": 8.0},
        {"name": "Poe", "description": "AI chatbot aggregator by Quora providing access to multiple AI models including Claude, GPT, and others in one platform", "link": "https://poe.com", "category": "Chatbots", "popularity_score": 7.9},
        {"name": "Intercom Fin", "description": "AI-powered customer service chatbot with natural language understanding and seamless handoff to human agents", "link": "https://www.intercom.com/fin", "category": "Customer Support", "popularity_score": 8.1},
        {"name": "Zendesk AI", "description": "AI-enhanced customer support platform with automated ticket routing, sentiment analysis, and response suggestions", "link": "https://www.zendesk.com/ai", "category": "Customer Support", "popularity_score": 7.8},
        {"name": "Ada", "description": "AI chatbot platform for customer service with no-code bot building and automated resolution of common inquiries", "link": "https://www.ada.cx", "category": "Customer Support", "popularity_score": 7.6},
        {"name": "LivePerson", "description": "Conversational AI platform for customer engagement with voice and text capabilities across multiple channels", "link": "https://www.liveperson.com", "category": "Customer Support", "popularity_score": 7.5},
        {"name": "Drift", "description": "AI-powered conversational marketing platform with chatbots for lead qualification and customer engagement", "link": "https://www.drift.com", "category": "Customer Support", "popularity_score": 7.7},
        {"name": "Freshworks Freddy AI", "description": "AI assistant integrated across Freshworks suite for customer service, sales, and marketing automation", "link": "https://www.freshworks.com/freddy-ai", "category": "Customer Support", "popularity_score": 7.4},
        {"name": "Botpress", "description": "Open-source chatbot development platform with AI capabilities and enterprise-grade deployment options", "link": "https://botpress.com", "category": "Chatbots", "popularity_score": 7.3},
        {"name": "Rasa", "description": "Open-source framework for building AI assistants and chatbots with advanced natural language understanding", "link": "https://rasa.com", "category": "Chatbots", "popularity_score": 7.2}
    ]
    
    # ANALYTICS & INSIGHTS TOOLS (Expanded)
    analytics_tools = [
        {"name": "DataRobot", "description": "Enterprise AI platform for automated machine learning, predictive analytics, and business intelligence insights", "link": "https://www.datarobot.com", "category": "Analytics", "popularity_score": 8.2},
        {"name": "H2O.ai", "description": "Open-source machine learning platform with automated ML capabilities and enterprise AI deployment solutions", "link": "https://www.h2o.ai", "category": "Analytics", "popularity_score": 7.8},
        {"name": "Tableau AI", "description": "AI-powered data visualization and business intelligence platform with automated insights and natural language queries", "link": "https://www.tableau.com", "category": "Analytics", "popularity_score": 7.9},
        {"name": "Microsoft Power BI AI", "description": "Business intelligence platform with AI-driven insights, automated data preparation, and natural language Q&A", "link": "https://powerbi.microsoft.com", "category": "Analytics", "popularity_score": 7.7},
        {"name": "Qlik Sense AI", "description": "Self-service analytics platform with AI-powered insights, automated data discovery, and augmented analytics", "link": "https://www.qlik.com/us/products/qlik-sense", "category": "Analytics", "popularity_score": 7.5},
        {"name": "Sisense AI", "description": "AI-driven analytics platform that simplifies complex data analysis with automated insights and ML capabilities", "link": "https://www.sisense.com", "category": "Analytics", "popularity_score": 7.4},
        {"name": "ThoughtSpot", "description": "Search-driven analytics platform with AI-powered insights and natural language data queries for business users", "link": "https://www.thoughtspot.com", "category": "Analytics", "popularity_score": 7.6},
        {"name": "Alteryx", "description": "Self-service data analytics platform with automated machine learning and predictive analytics capabilities", "link": "https://www.alteryx.com", "category": "Analytics", "popularity_score": 7.3}
    ]
    
    # EDUCATION & LEARNING TOOLS (Expanded)
    education_tools = [
        {"name": "Khan Academy Khanmigo", "description": "AI tutoring assistant that provides personalized learning support and guided practice across subjects", "link": "https://www.khanacademy.org/khan-labs", "category": "Education", "popularity_score": 8.3},
        {"name": "Duolingo Max", "description": "AI-powered language learning with personalized lessons, conversation practice, and adaptive learning paths", "link": "https://blog.duolingo.com/duolingo-max", "category": "Education", "popularity_score": 8.1},
        {"name": "Coursera AI", "description": "AI-enhanced online learning platform with personalized course recommendations and adaptive assessment", "link": "https://www.coursera.org", "category": "Education", "popularity_score": 7.8},
        {"name": "Grammarly for Students", "description": "AI writing assistant specifically designed for academic writing with citation support and plagiarism detection", "link": "https://www.grammarly.com/edu", "category": "Education", "popularity_score": 7.9},
        {"name": "Speechify Education", "description": "AI text-to-speech platform designed for students with learning differences and accessibility needs", "link": "https://speechify.com/education", "category": "Education", "popularity_score": 7.7},
        {"name": "Socratic by Google", "description": "AI homework helper that provides step-by-step explanations and learning resources across subjects", "link": "https://socratic.org", "category": "Education", "popularity_score": 7.6},
        {"name": "Quizlet AI", "description": "AI-enhanced study platform with intelligent flashcards, personalized learning modes, and adaptive testing", "link": "https://quizlet.com", "category": "Education", "popularity_score": 7.5},
        {"name": "Gradescope AI", "description": "AI-assisted grading platform for educators with automated feedback and rubric-based assessment", "link": "https://www.gradescope.com", "category": "Education", "popularity_score": 7.4},
        {"name": "Carnegie Learning", "description": "AI-powered adaptive learning platform for mathematics with personalized instruction and real-time feedback", "link": "https://www.carnegielearning.com", "category": "Education", "popularity_score": 7.3},
        {"name": "Century Tech", "description": "AI platform for personalized learning with adaptive content delivery and progress tracking for educators", "link": "https://www.century.tech", "category": "Education", "popularity_score": 7.2}
    ]
    
    # EMERGING & SPECIALIZED TOOLS
    emerging_tools = [
        {"name": "DeepAI", "description": "Comprehensive collection of AI tools for image generation, text processing, and analysis with API access", "link": "https://deepai.org", "category": "Artificial Intelligence", "popularity_score": 7.7},
        {"name": "Replika", "description": "AI companion app for emotional support and conversation with personalized AI personality development", "link": "https://replika.ai", "category": "Chatbots", "popularity_score": 7.4},
        {"name": "MonkeyLearn", "description": "No-code text analysis platform with sentiment analysis, keyword extraction, and custom AI model training", "link": "https://monkeylearn.com", "category": "Analytics", "popularity_score": 7.1},
        {"name": "Lobe", "description": "Microsoft's visual machine learning tool for creating custom AI models without coding experience required", "link": "https://www.lobe.ai", "category": "Developer Tools", "popularity_score": 7.0},
        {"name": "Runway Academy", "description": "Educational platform for learning AI tools and creative applications with hands-on tutorials and projects", "link": "https://academy.runwayml.com", "category": "Education", "popularity_score": 6.9},
        {"name": "AI Dungeon", "description": "AI-powered text adventure game with infinite storylines and creative writing assistance capabilities", "link": "https://play.aidungeon.io", "category": "Content Creation", "popularity_score": 6.8}
    ]
    
    # Combine all tool categories
    all_tool_categories = [
        top_priority_tools, video_content_tools, image_design_tools, audio_voice_tools,
        writing_productivity_tools, automation_dev_tools, business_productivity_tools,
        marketing_sales_tools, chatbots_support_tools, analytics_tools, education_tools, emerging_tools
    ]
    
    # Process each tool and assign IDs
    for category_tools in all_tool_categories:
        for tool in category_tools:
            domain = tool['link'].split('//')[1].split('/')[0]
            tool_entry = {
                "id": tool_id,
                "name": tool["name"],
                "description": tool["description"],
                "link": tool["link"],
                "category": tool["category"],
                "logo_url": f"https://logo.clearbit.com/{domain}",
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

def create_comprehensive_dataset():
    """Create the comprehensive 2024-2025 AI tools dataset"""
    tools = get_expanded_2024_2025_tools()
    
    # Create metadata
    categories = list(set([tool["category"] for tool in tools]))
    
    dataset = {
        "metadata": {
            "title": "AIverse - Comprehensive 2024-2025 AI Tools Collection",
            "description": "An extensive, curated collection of trending AI tools released or significantly updated in 2024-2025",
            "version": "2.0",
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "total_tools": len(tools),
            "categories": sorted(categories),
            "curation_criteria": [
                "Released or significantly updated in 2024-2025",
                "High popularity and user adoption",
                "Active development and community support",
                "Professional-grade functionality",
                "Comprehensive feature set",
                "Strong market presence and user reviews"
            ],
            "source": "Curated from Synthesia, Exploding Topics, Insidr AI, Aixploria, and industry research",
            "featured_tools_count": len([t for t in tools if t.get("featured", False)])
        },
        "tools": tools
    }
    
    return dataset

if __name__ == "__main__":
    # Create the comprehensive dataset
    dataset = create_comprehensive_dataset()
    
    # Save to file
    output_file = "/workspace/aiverse_tools_2024_2025_comprehensive.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Comprehensive 2024-2025 AI Tools dataset created successfully!")
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
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {category}: {count} tools")
    
    print("\n🌟 Top Featured Tools:")
    featured_tools = [t for t in dataset['tools'] if t.get('featured', False)]
    for tool in sorted(featured_tools, key=lambda x: x['popularity_score'], reverse=True):
        print(f"  • {tool['name']} - {tool['popularity_score']}/10.0 ({tool['category']})")
