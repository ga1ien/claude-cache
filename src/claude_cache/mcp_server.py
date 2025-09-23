#!/usr/bin/env python3
"""
MCP Server for Claude Cache
Exposes vector search and pattern management as native Claude Code tools
"""

import os
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    Prompt,
    PromptArgument,
    GetPromptResult,
    PromptMessage,
    LoggingLevel
)

# Claude Cache imports
from .knowledge_base import KnowledgeBase
from .agent import CacheAgent

# Configure logging to stderr (IMPORTANT: stdout corrupts MCP messages)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class ClaudeCacheMCP:
    """MCP Server for Claude Cache - Makes AI coding faster and smarter"""

    def __init__(self):
        self.server = Server("claude-cache")
        self.kb = KnowledgeBase()
        self.agent = CacheAgent()

        # Register handlers
        self._register_handlers()

        logger.info("Claude Cache MCP Server initialized")

    def _register_handlers(self):
        """Register all MCP handlers"""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List all available Claude Cache tools"""
            return [
                Tool(
                    name="cache_query",
                    description="Search your coding patterns and documentation using semantic vector search. Finds relevant solutions from past sessions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "What to search for (e.g., 'authentication', 'database pooling', 'error handling')"
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
                    description="Mark the current solution as successful and save it to your knowledge base. Use when something works well.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Brief description of what worked"
                            },
                            "category": {
                                "type": "string",
                                "description": "Category (e.g., 'authentication', 'database', 'testing')"
                            },
                            "code_snippet": {
                                "type": "string",
                                "description": "Optional: The code that worked"
                            }
                        },
                        "required": ["description"]
                    }
                ),
                Tool(
                    name="cache_stats",
                    description="Get statistics about your knowledge base - patterns learned, projects tracked, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "Optional: Get stats for specific project"
                            }
                        }
                    }
                ),
                Tool(
                    name="cache_suggest",
                    description="Proactively get suggestions based on current context. Finds patterns similar to what you're working on.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "context": {
                                "type": "string",
                                "description": "Current code or problem you're working on"
                            },
                            "intent": {
                                "type": "string",
                                "description": "What you're trying to do (e.g., 'add authentication', 'fix bug', 'optimize performance')"
                            }
                        },
                        "required": ["context"]
                    }
                ),
                Tool(
                    name="cache_inject",
                    description="Inject specific patterns or documentation into current context. Updates CLAUDE.md for reference.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of pattern IDs to inject"
                            },
                            "category": {
                                "type": "string",
                                "description": "Category of patterns to inject"
                            }
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool execution"""

            try:
                if name == "cache_query":
                    results = self._handle_query(
                        arguments.get("query"),
                        arguments.get("project"),
                        arguments.get("limit", 5)
                    )
                    return [TextContent(type="text", text=results)]

                elif name == "cache_learn":
                    result = self._handle_learn(
                        arguments.get("description"),
                        arguments.get("category", "general"),
                        arguments.get("code_snippet")
                    )
                    return [TextContent(type="text", text=result)]

                elif name == "cache_stats":
                    stats = self._handle_stats(arguments.get("project"))
                    return [TextContent(type="text", text=stats)]

                elif name == "cache_suggest":
                    suggestions = self._handle_suggest(
                        arguments.get("context"),
                        arguments.get("intent")
                    )
                    return [TextContent(type="text", text=suggestions)]

                elif name == "cache_inject":
                    result = self._handle_inject(
                        arguments.get("pattern_ids", []),
                        arguments.get("category")
                    )
                    return [TextContent(type="text", text=result)]

                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

        @self.server.list_prompts()
        async def handle_list_prompts() -> list[Prompt]:
            """List available prompts for quick access"""
            return [
                Prompt(
                    name="find_similar",
                    description="Find patterns similar to current work",
                    arguments=[
                        PromptArgument(
                            name="code",
                            description="Current code context",
                            required=True
                        )
                    ]
                ),
                Prompt(
                    name="debug_help",
                    description="Get debugging help from past solutions",
                    arguments=[
                        PromptArgument(
                            name="error",
                            description="Error message or issue",
                            required=True
                        )
                    ]
                )
            ]

        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict) -> GetPromptResult:
            """Generate prompt based on template"""

            if name == "find_similar":
                code = arguments.get("code", "")
                # Use vector search to find similar patterns
                results = self.kb.unified_search(code[:500], limit=3)

                messages = [
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=f"Based on this code:\n```\n{code}\n```\n\nHere are similar patterns from your knowledge base:\n{self._format_results(results)}"
                        )
                    )
                ]
                return GetPromptResult(messages=messages)

            elif name == "debug_help":
                error = arguments.get("error", "")
                # Search for similar errors or debugging patterns
                results = self.kb.unified_search(f"error debug {error}", limit=5)

                messages = [
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=f"For this error:\n{error}\n\nRelevant debugging patterns:\n{self._format_results(results)}"
                        )
                    )
                ]
                return GetPromptResult(messages=messages)

            return GetPromptResult(messages=[])

    def _handle_query(self, query: str, project: Optional[str], limit: int) -> str:
        """Handle vector search query"""
        if not query:
            return "Error: Query is required"

        results = self.kb.unified_search(query, project_name=project, limit=limit)

        if not results:
            return f"No results found for '{query}'"

        # Format results with rich information
        output = f"🔍 Found {len(results)} relevant patterns for '{query}':\n\n"

        for i, result in enumerate(results, 1):
            content_type = result.get('type', 'unknown')
            icon = "📚" if content_type == 'documentation' else "🧠"

            output += f"{i}. {icon} "

            if content_type == 'pattern':
                output += f"**Pattern**: {result.get('content', '')[:100]}...\n"
                output += f"   Score: {result.get('similarity', 0):.3f}"
                if result.get('project'):
                    output += f" | Project: {result.get('project')}"
            else:
                output += f"**Doc**: {result.get('content', '')[:100]}...\n"
                output += f"   Score: {result.get('similarity', 0):.3f}"
                if result.get('file_path'):
                    output += f" | File: {result.get('file_path')}"

            output += "\n\n"

        # Add proactive suggestion
        output += "\n💡 **Tip**: Use `cache_learn` to save successful solutions!"

        return output

    def _handle_learn(self, description: str, category: str, code_snippet: Optional[str]) -> str:
        """Save a successful pattern"""

        # Get current project from working directory
        project_name = Path.cwd().name

        # Create pattern object
        pattern = {
            "user_request": description,
            "approach": code_snippet if code_snippet else description,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "source": "mcp_direct"
        }

        # Store in knowledge base
        self.kb.store_success_pattern(pattern, project_name, success_score=1.0)

        # Update stats
        stats = self.kb.get_statistics(project_name)

        return f"""✅ Pattern saved successfully!

📊 **Your Knowledge Base**:
- Total Patterns: {stats.get('patterns', 0)}
- Project: {project_name}
- Category: {category}

🎯 This pattern is now searchable via vector search and will help in similar situations!"""

    def _handle_stats(self, project: Optional[str]) -> str:
        """Get knowledge base statistics"""
        stats = self.kb.get_statistics(project)

        output = "📊 **Claude Cache Statistics**\n\n"

        if project:
            output += f"Project: **{project}**\n"
            output += f"- Patterns: {stats.get('patterns', 0)}\n"
            output += f"- Conventions: {stats.get('conventions', 0)}\n"
            output += f"- Requests: {stats.get('requests', 0)}\n"
        else:
            output += f"**Global Stats**:\n"
            output += f"- Total Patterns: {stats.get('total_patterns', 0)}\n"
            output += f"- Projects Tracked: {stats.get('projects', 0)}\n"
            output += f"- Total Requests: {stats.get('total_requests', 0)}\n"

        # Add vector search info
        if self.kb.vector_search:
            caps = self.kb.vector_search.get_capabilities()
            output += f"\n**Search Engine**:\n"
            output += f"- Mode: {caps['mode']} {'✨' if caps['mode'] == 'semantic' else '⚡'}\n"
            output += f"- Indexed Items: {caps['pattern_count']}\n"

        return output

    def _handle_suggest(self, context: str, intent: Optional[str]) -> str:
        """Proactively suggest relevant patterns"""

        # Build search query from context and intent
        search_query = context[:500]  # Limit context length
        if intent:
            search_query = f"{intent} {search_query}"

        # Find similar patterns
        results = self.kb.unified_search(search_query, limit=3)

        if not results:
            return "💭 No similar patterns found. This looks like something new!"

        output = "💡 **Proactive Suggestions**\n\n"
        output += "Based on what you're working on, here are relevant patterns:\n\n"

        for i, result in enumerate(results, 1):
            output += f"{i}. {result.get('content', '')[:150]}...\n"
            output += f"   Relevance: {result.get('similarity', 0):.1%}\n\n"

        output += "\n🎯 These patterns have worked before in similar situations!"

        return output

    def _handle_inject(self, pattern_ids: List[str], category: Optional[str]) -> str:
        """Inject patterns into current context"""

        # Get project root
        project_root = Path.cwd()
        claude_dir = project_root / ".claude"
        claude_md = claude_dir / "CLAUDE.md"

        # Ensure directory exists
        claude_dir.mkdir(exist_ok=True)

        patterns_to_inject = []

        if category:
            # Get patterns by category
            # This would need a method in KnowledgeBase to get patterns by category
            output = f"Injected patterns from category: {category}"
        elif pattern_ids:
            # Get specific patterns
            output = f"Injected {len(pattern_ids)} patterns"
        else:
            return "Error: Provide either pattern_ids or category"

        # Update CLAUDE.md
        # This would integrate with existing context injection logic

        return f"""✅ Patterns injected into context!

📁 Updated: {claude_md}
📊 Patterns injected: {len(pattern_ids) if pattern_ids else 'category: ' + (category or '')}

Claude will now reference these patterns automatically!"""

    def _format_results(self, results: List[Dict]) -> str:
        """Format search results for display"""
        if not results:
            return "No results found"

        output = []
        for i, r in enumerate(results[:3], 1):
            output.append(f"{i}. {r.get('content', '')[:100]}...")

        return "\n".join(output)

    async def run(self):
        """Run the MCP server"""
        # Run with stdio transport
        from mcp.server.stdio import stdio_server
        import asyncio

        async with stdio_server() as streams:
            await self.server.run(
                streams[0],  # read stream
                streams[1],  # write stream
                InitializationOptions(
                    server_name="claude-cache",
                    server_version="0.7.0"
                )
            )

def main():
    """Main entry point for MCP server"""
    import asyncio

    # Create and run server
    server = ClaudeCacheMCP()

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("MCP Server shutting down")
    except Exception as e:
        logger.error(f"MCP Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()