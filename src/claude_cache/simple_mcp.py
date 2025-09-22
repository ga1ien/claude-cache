#!/usr/bin/env python3
"""
Simple MCP Server for Claude Cache
Based on official MCP Python SDK examples
"""

import asyncio
import sys
import logging
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
except ImportError:
    # Handle direct execution
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from claude_cache.knowledge_base import KnowledgeBase
    from claude_cache.agent import CacheAgent

app = Server("claude-cache")

# Initialize Claude Cache
kb = KnowledgeBase()
agent = CacheAgent()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="cache_query",
            description="Search your coding patterns and documentation using semantic vector search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for (e.g., 'authentication', 'database')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="cache_stats",
            description="Get statistics about your knowledge base",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "cache_query":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 5)

            if not query:
                return [TextContent(type="text", text="Error: Query is required")]

            results = kb.unified_search(query, limit=limit)

            if not results:
                return [TextContent(type="text", text=f"No results found for '{query}'")]

            output = f"🔍 Found {len(results)} results for '{query}':\n\n"

            for i, result in enumerate(results, 1):
                content_type = result.get('type', 'unknown')
                icon = "📚" if content_type == 'documentation' else "🧠"
                content = result.get('content', '')[:100]
                score = result.get('similarity', 0)

                output += f"{i}. {icon} {content}...\n"
                output += f"   Score: {score:.3f}\n\n"

            return [TextContent(type="text", text=output)]

        elif name == "cache_stats":
            stats = kb.get_statistics()

            output = "📊 **Claude Cache Statistics**\n\n"
            output += f"- Total Patterns: {stats.get('total_patterns', 0)}\n"
            output += f"- Projects: {stats.get('projects', 0)}\n"

            if kb.vector_search:
                caps = kb.vector_search.get_capabilities()
                output += f"- Search Mode: {caps['mode']} {'✨' if caps['mode'] == 'semantic' else '⚡'}\n"
                output += f"- Indexed Items: {caps['pattern_count']}\n"

            return [TextContent(type="text", text=output)]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Main entry point"""
    logger.info("Starting Claude Cache MCP Server...")

    try:
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1])
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())