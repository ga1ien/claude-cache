#!/usr/bin/env python3
"""
Complete MCP Server for Claude Cache
All features available as native Claude Code tools
"""

import asyncio
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Import Claude Cache components
try:
    from .knowledge_base import KnowledgeBase
    from .agent import CacheAgent
    from .doc_scanner import DocumentationScanner
except ImportError:
    # Handle direct execution
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from claude_cache.knowledge_base import KnowledgeBase
    from claude_cache.agent import CacheAgent
    from claude_cache.doc_scanner import DocumentationScanner

app = Server("claude-cache")

# Initialize Claude Cache (silent mode for MCP)
kb = KnowledgeBase(silent=True)
agent = CacheAgent(kb=kb)

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Claude Cache tools"""
    return [
        Tool(
            name="cache_query",
            description="🔍 Search your coding patterns and documentation using semantic vector search. Finds relevant solutions from past sessions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for (e.g., 'authentication JWT', 'database pooling', 'error handling')"
                    },
                    "project": {
                        "type": "string",
                        "description": "Optional: Specific project name to search within"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="cache_learn",
            description="💾 Save successful solution as a pattern. Use when something works well to build your knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Brief description of what worked (e.g., 'JWT refresh token implementation')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category for organization (e.g., 'authentication', 'database', 'testing')",
                        "default": "general"
                    },
                    "code_snippet": {
                        "type": "string",
                        "description": "Optional: The working code or configuration"
                    },
                    "approach": {
                        "type": "string",
                        "description": "Optional: Detailed explanation of the approach"
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="cache_suggest",
            description="💡 Get proactive suggestions based on your current work. Finds patterns similar to what you're doing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Current code or problem context you're working on"
                    },
                    "intent": {
                        "type": "string",
                        "description": "What you're trying to accomplish (e.g., 'add caching', 'fix performance', 'implement auth')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum suggestions to return (default: 3)",
                        "default": 3
                    }
                },
                "required": ["context"]
            }
        ),
        Tool(
            name="cache_stats",
            description="📊 Get statistics about your knowledge base - patterns learned, projects tracked, search capabilities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Optional: Get stats for specific project only"
                    },
                    "detailed": {
                        "type": "boolean",
                        "description": "Show detailed breakdown by category (default: false)",
                        "default": false
                    }
                }
            }
        ),
        Tool(
            name="cache_browse",
            description="🌐 Ingest documentation from a URL and add to your knowledge base. Automatically indexes content for search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to scrape and index (e.g., 'https://docs.example.com/api')"
                    },
                    "project": {
                        "type": "string",
                        "description": "Project name to associate with this documentation"
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "Type of documentation (e.g., 'api', 'tutorial', 'reference')",
                        "default": "documentation"
                    }
                },
                "required": ["url"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution with comprehensive error handling"""

    try:
        if name == "cache_query":
            return await handle_query(arguments)
        elif name == "cache_learn":
            return await handle_learn(arguments)
        elif name == "cache_suggest":
            return await handle_suggest(arguments)
        elif name == "cache_stats":
            return await handle_stats(arguments)
        elif name == "cache_browse":
            return await handle_browse(arguments)
        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"❌ Error in {name}: {str(e)}")]

async def handle_query(args: dict) -> list[TextContent]:
    """Handle vector search queries"""
    query = args.get("query", "").strip()
    project = args.get("project")
    limit = args.get("limit", 5)

    if not query:
        return [TextContent(type="text", text="❌ Error: Query is required")]

    # Perform unified search
    results = kb.unified_search(query, project_name=project, limit=limit)

    if not results:
        return [TextContent(type="text", text=f"🔍 No results found for '{query}'\n\n💡 Try:\n- Broader search terms\n- Different keywords\n- Use cache_learn to add more patterns")]

    # Format results with rich information
    output = f"🔍 **Found {len(results)} results for '{query}'**\n\n"

    for i, result in enumerate(results, 1):
        content_type = result.get('type', 'unknown')
        similarity = result.get('similarity', 0)
        content = result.get('content', '')
        project_name = result.get('project', 'Unknown')

        # Choose icon based on type
        if content_type == 'documentation':
            icon = "📚"
            type_label = "Documentation"
        elif content_type == 'pattern':
            icon = "🧠"
            type_label = "Pattern"
        else:
            icon = "📄"
            type_label = "Content"

        # Format content preview
        preview = content[:120] + "..." if len(content) > 120 else content

        output += f"**{i}. {icon} {type_label}** (Score: {similarity:.3f})\n"
        output += f"📁 Project: {project_name}\n"
        output += f"📝 {preview}\n\n"

    # Add helpful footer
    output += "💡 **Tips**:\n"
    output += "- Use `cache_learn` to save successful solutions\n"
    output += "- Try `cache_suggest` for proactive recommendations\n"
    output += "- Check `cache_stats` to see your knowledge base growth"

    return [TextContent(type="text", text=output)]

async def handle_learn(args: dict) -> list[TextContent]:
    """Save successful patterns to knowledge base"""
    description = args.get("description", "").strip()
    category = args.get("category", "general")
    code_snippet = args.get("code_snippet", "")
    approach = args.get("approach", "")

    if not description:
        return [TextContent(type="text", text="❌ Error: Description is required")]

    # Get current project from working directory
    project_name = Path.cwd().name

    # Build comprehensive pattern object
    pattern = {
        "user_request": description,
        "approach": approach or code_snippet or description,
        "category": category,
        "timestamp": datetime.now().isoformat(),
        "source": "mcp_learn_tool",
        "files_involved": [],
        "solution_steps": [description],
        "key_operations": [],
        "tags": [category]
    }

    # Add code snippet if provided
    if code_snippet:
        pattern["code_example"] = code_snippet
        pattern["solution_steps"].append(f"Code: {code_snippet[:100]}...")

    # Store in knowledge base
    kb.store_success_pattern(pattern, project_name, success_score=1.0)

    # Get updated stats
    stats = kb.get_statistics(project_name)

    output = f"✅ **Pattern Saved Successfully!**\n\n"
    output += f"📝 **Description**: {description}\n"
    output += f"📂 **Category**: {category}\n"
    output += f"📁 **Project**: {project_name}\n"
    output += f"⏰ **Saved**: {datetime.now().strftime('%H:%M:%S')}\n\n"

    output += f"📊 **Your Knowledge Base**:\n"
    output += f"- Patterns in this project: {stats.get('patterns', 0)}\n"

    if kb.vector_search:
        caps = kb.vector_search.get_capabilities()
        output += f"- Search mode: {caps['mode']} {'✨' if caps['mode'] == 'semantic' else '⚡'}\n"

    output += f"\n🎯 This pattern is now searchable and will help in similar situations!"

    return [TextContent(type="text", text=output)]

async def handle_suggest(args: dict) -> list[TextContent]:
    """Provide proactive suggestions based on context"""
    context = args.get("context", "").strip()
    intent = args.get("intent", "")
    limit = args.get("limit", 3)

    if not context:
        return [TextContent(type="text", text="❌ Error: Context is required")]

    # Build search query from context and intent
    search_query = context[:500]  # Limit context length for search
    if intent:
        search_query = f"{intent} {search_query}"

    # Find similar patterns
    results = kb.unified_search(search_query, limit=limit)

    if not results:
        output = "💭 **No Similar Patterns Found**\n\n"
        output += "This looks like something new! Consider:\n"
        output += "- Breaking the problem into smaller parts\n"
        output += "- Searching for individual components\n"
        output += "- Using `cache_learn` to save your solution when you find it"
        return [TextContent(type="text", text=output)]

    output = "💡 **Proactive Suggestions**\n\n"
    output += f"Based on your context: *{context[:100]}{'...' if len(context) > 100 else ''}*\n\n"

    if intent:
        output += f"🎯 Intent: {intent}\n\n"

    output += "**Relevant patterns from your knowledge base**:\n\n"

    for i, result in enumerate(results, 1):
        similarity = result.get('similarity', 0)
        content = result.get('content', '')
        content_type = result.get('type', 'unknown')

        icon = "🧠" if content_type == 'pattern' else "📚"
        relevance_pct = similarity * 100

        # Format content preview
        preview = content[:100] + "..." if len(content) > 100 else content

        output += f"**{i}. {icon} {preview}**\n"
        output += f"   📊 Relevance: {relevance_pct:.1f}%\n\n"

    output += "🎯 **These patterns have worked before in similar situations!**\n"
    output += "Use `cache_query` to explore these patterns in more detail."

    return [TextContent(type="text", text=output)]

async def handle_stats(args: dict) -> list[TextContent]:
    """Get comprehensive knowledge base statistics"""
    project = args.get("project")
    detailed = args.get("detailed", False)

    stats = kb.get_statistics(project)

    output = "📊 **Claude Cache Statistics**\n\n"

    if project:
        output += f"🗂️ **Project: {project}**\n"
        output += f"- Patterns: {stats.get('patterns', 0)}\n"
        output += f"- Conventions: {stats.get('conventions', 0)}\n"
        output += f"- Requests: {stats.get('requests', 0)}\n\n"
    else:
        output += f"🌍 **Global Knowledge Base**\n"
        output += f"- Total Patterns: {stats.get('total_patterns', 0)}\n"
        output += f"- Projects Tracked: {stats.get('projects', 0)}\n"
        output += f"- Total Requests: {stats.get('total_requests', 0)}\n\n"

    # Vector search capabilities
    if kb.vector_search:
        caps = kb.vector_search.get_capabilities()
        output += f"🔍 **Search Engine**\n"
        if caps['mode'] == 'semantic':
            output += f"- Mode: Semantic Search ✨ (Enhanced)\n"
            output += f"- Model: {caps['model']}\n"
            output += f"- Understanding: Context + meaning\n"
        else:
            output += f"- Mode: TF-IDF Search ⚡ (Fast)\n"
            output += f"- Type: Keyword matching\n"
            output += f"- Upgrade: Install sentence-transformers for semantic search\n"

        output += f"- Indexed Items: {caps['pattern_count']}\n\n"

    # Current project context
    current_project = Path.cwd().name
    output += f"📁 **Current Project**: {current_project}\n"

    # Quick tips based on stats
    total_patterns = stats.get('total_patterns', 0) or stats.get('patterns', 0)
    if total_patterns == 0:
        output += "\n💡 **Getting Started**:\n"
        output += "- Use `cache_learn` to save successful solutions\n"
        output += "- Use `cache_browse` to index documentation\n"
        output += "- Try `cache_query` to search existing knowledge\n"
    elif total_patterns < 10:
        output += "\n🌱 **Building Knowledge**:\n"
        output += "- Great start! Keep using `cache_learn` for successful patterns\n"
        output += "- Consider browsing relevant documentation\n"
    else:
        output += "\n🚀 **Knowledge Base Active**:\n"
        output += "- Use `cache_suggest` for proactive recommendations\n"
        output += "- Try specific searches with `cache_query`\n"

    return [TextContent(type="text", text=output)]

async def handle_browse(args: dict) -> list[TextContent]:
    """Browse and index documentation from URL"""
    url = args.get("url", "").strip()
    project = args.get("project") or Path.cwd().name
    doc_type = args.get("doc_type", "documentation")

    if not url:
        return [TextContent(type="text", text="❌ Error: URL is required")]

    if not url.startswith(('http://', 'https://')):
        return [TextContent(type="text", text="❌ Error: URL must start with http:// or https://")]

    try:
        output = f"🌐 **Browsing Documentation**\n\n"
        output += f"📄 URL: {url}\n"
        output += f"📁 Project: {project}\n"
        output += f"📋 Type: {doc_type}\n\n"
        output += "⏳ Fetching and processing content...\n\n"

        # Create documentation scanner
        scanner = DocumentationScanner(kb)

        # Scan and process the URL
        scraped_content = scanner.scan_url(url)

        if not scraped_content or not scraped_content.get('content'):
            return [TextContent(type="text", text=f"❌ Could not extract content from {url}")]

        # Extract lessons and patterns from content
        extracted = scanner.extract_lessons(scraped_content['content'])

        # Store in knowledge base
        kb.store_documentation(
            project_name=project,
            file_path=url,
            doc_type=doc_type,
            content=json.dumps(extracted),
            extracted_at=datetime.now().isoformat()
        )

        # Build success message
        result_output = "✅ **Documentation Indexed Successfully!**\n\n"
        result_output += f"📊 **Extracted Content**:\n"
        result_output += f"- Lessons: {len(extracted.get('lessons', []))}\n"
        result_output += f"- Warnings: {len(extracted.get('warnings', []))}\n"
        result_output += f"- Best Practices: {len(extracted.get('best_practices', []))}\n\n"

        if kb.vector_search:
            result_output += "🔍 **Auto-indexed for vector search** - Now searchable with `cache_query`!\n\n"

        result_output += "🎯 **Next Steps**:\n"
        result_output += f"- Try: `cache_query` with topics from this documentation\n"
        result_output += f"- Use: `cache_stats` to see updated knowledge base\n"

        return [TextContent(type="text", text=result_output)]

    except Exception as e:
        logger.error(f"Error browsing {url}: {e}")
        return [TextContent(type="text", text=f"❌ Error browsing {url}: {str(e)}")]

async def main():
    """Main entry point for complete MCP server"""
    logger.info("Starting Claude Cache Complete MCP Server...")

    try:
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1])
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())