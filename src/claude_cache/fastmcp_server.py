#!/usr/bin/env python3
"""
FastMCP Server for Claude Cache
Clean implementation using FastMCP pattern for reliable MCP connection
"""

import sys
import os
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Suppress all stdout output to prevent JSON-RPC pollution
import contextlib
import io

# Configure logging to stderr only
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Import with output suppression
with contextlib.redirect_stdout(io.StringIO()):
    from mcp.server.fastmcp import FastMCP
    # Import Claude Cache components with silent mode
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    try:
        from claude_cache.knowledge_base import KnowledgeBase
        from claude_cache.agent import CacheAgent
        from claude_cache.doc_scanner import DocumentationScanner
    except ImportError:
        from .knowledge_base import KnowledgeBase
        from .agent import CacheAgent
        from .doc_scanner import DocumentationScanner

# Initialize FastMCP server
mcp = FastMCP("cache")

# Initialize Claude Cache components in silent mode
kb = KnowledgeBase(silent=True)
agent = CacheAgent(kb=kb)

@mcp.tool()
async def query(query: str, limit: int = 5, project: str = None) -> str:
    """
    Search your coding patterns and documentation using intelligent contextual search.
    Automatically prioritizes patterns most relevant to your current project and context.

    Args:
        query: What to search for (e.g., 'authentication', 'database optimization')
        limit: Maximum number of results to return (default: 5)
        project: Project name for context-aware results (auto-detected if not provided)

    Returns:
        Contextually ranked search results with relevance scores and applicability
    """
    try:
        results = []

        # Try to detect current project context if not provided
        if not project:
            project = "default"  # Could be enhanced with actual project detection

        # Get contextual patterns using cross-project intelligence
        try:
            cross_intel = agent.processor.cross_project_intelligence
            if cross_intel:
                # Build current context for better ranking
                current_context = {
                    'current_task': query,
                    'recent_successful_patterns': []  # Could be populated from recent history
                }

                # Get contextually relevant patterns
                contextual_patterns = cross_intel.get_contextual_patterns(
                    project, current_context, limit=limit
                )

                # Convert to results format with enhanced metadata
                for pattern in contextual_patterns:
                    scope = pattern.get('scope', 'unknown')
                    confidence = pattern.get('confidence', 'medium')

                    result = {
                        'content': pattern.get('approach', pattern.get('description', '')),
                        'type': 'contextual_pattern',
                        'scope': scope,
                        'confidence': confidence,
                        'similarity': 0.8 if confidence == 'high' else 0.6,
                        'project_specific': scope == 'project_specific'
                    }
                    results.append(result)
        except Exception:
            # Fallback to traditional search if contextual search fails
            pass

        # Fallback or supplement with traditional search
        if not results or len(results) < limit:
            remaining_limit = limit - len(results)

            if kb.vector_search:
                patterns = kb.vector_search.search_patterns(query, limit=remaining_limit)
                for pattern in patterns:
                    results.append({
                        'content': pattern.get('content', ''),
                        'type': 'pattern',
                        'similarity': pattern.get('similarity', 0.5),
                        'scope': 'traditional_search'
                    })
            else:
                patterns = kb.search_patterns(query, limit=remaining_limit)
                for pattern in patterns:
                    results.append({
                        'content': pattern.get('approach', ''),
                        'type': 'pattern',
                        'similarity': 0.5,
                        'scope': 'traditional_search'
                    })

        # Search documentation
        docs = kb.search_documentation(query, limit=limit)
        results.extend([{
            'content': d.get('content', ''),
            'type': 'documentation',
            'similarity': d.get('similarity', 0.5)
        } for d in docs])

        # Sort by similarity and limit
        results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        results = results[:limit]

        if not results:
            return f"No results found for '{query}'"

        # Sort results by similarity/relevance
        results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        results = results[:limit]

        output = f"🔍 Found {len(results)} contextual results for '{query}':\n\n"

        for i, result in enumerate(results, 1):
            content_type = result.get('type', 'unknown')
            scope = result.get('scope', 'unknown')
            confidence = result.get('confidence', 'medium')

            # Choose appropriate icon and context info
            if content_type == 'documentation':
                icon = "📚"
                context_info = "Documentation"
            elif content_type == 'contextual_pattern':
                if scope == 'project_specific':
                    icon = "🎯"
                    context_info = f"Project-specific ({confidence} confidence)"
                elif scope == 'universal':
                    icon = "🌍"
                    context_info = f"Universal pattern ({confidence} confidence)"
                else:
                    icon = "🔄"
                    context_info = f"Transferable ({confidence} confidence)"
            else:
                icon = "🧠"
                context_info = "General pattern"

            content = result.get('content', '')[:200]
            score = result.get('similarity', 0)

            output += f"{i}. {icon} {content}...\n"
            output += f"   Relevance: {score:.3f} | {context_info}\n\n"

        return output

    except Exception as e:
        return f"❌ Error searching: {str(e)}"

@mcp.tool()
async def learn(
    solution: str,
    context: str = "",
    tags: str = "",
    project_name: str = "default"
) -> str:
    """
    Save a successful coding solution or pattern to your knowledge base.
    Use this when something works well and you want to remember it.

    Args:
        solution: The successful code or approach that worked
        context: Additional context about when/why this solution is useful
        tags: Comma-separated tags for categorization (e.g., 'auth,jwt,security')
        project_name: Project this solution belongs to (default: 'default')

    Returns:
        Confirmation message with pattern ID
    """
    try:
        pattern = {
            'request_type': 'manual_save',
            'user_request': context,
            'approach': solution,
            'solution_steps': [solution],
            'tags': tags.split(',') if tags else [],
            'timestamp': datetime.now().isoformat()
        }

        kb.store_success_pattern(pattern, project_name)

        # Update vector index if available
        if kb.vector_search:
            kb.vector_search.update_index()

        return f"✅ Pattern saved successfully!\n🏷️ Tags: {tags or 'none'}\n📁 Project: {project_name}"

    except Exception as e:
        return f"❌ Error saving pattern: {str(e)}"

@mcp.tool()
async def suggest(context: str = "", project_name: str = "default") -> str:
    """
    Get intelligent, proactive recommendations based on current context.
    Uses advanced pattern analysis to suggest the most relevant solutions.

    Args:
        context: Current code or problem description (optional)
        project_name: Current project name (default: 'default')

    Returns:
        Contextually intelligent suggestions with applicability analysis
    """
    try:
        output = "💡 **Intelligent suggestions for your current work:**\n\n"

        # Use cross-project intelligence for better suggestions
        try:
            cross_intel = agent.processor.cross_project_intelligence
            if cross_intel:
                # Build rich context
                current_context = {
                    'current_task': context,
                    'recent_successful_patterns': []  # Could be populated from recent history
                }

                # Get contextually ranked patterns
                contextual_patterns = cross_intel.get_contextual_patterns(
                    project_name, current_context, limit=5
                )

                if contextual_patterns:
                    # Group by scope for better presentation
                    project_specific = [p for p in contextual_patterns if p.get('scope') == 'project_specific']
                    universal = [p for p in contextual_patterns if p.get('scope') == 'universal']
                    transferable = [p for p in contextual_patterns if p.get('scope') in ['transferable', 'context_dependent']]

                    if project_specific:
                        output += f"**🎯 {project_name}-specific patterns:**\n"
                        for i, p in enumerate(project_specific[:3], 1):
                            confidence = p.get('confidence', 'medium')
                            output += f"{i}. {p.get('approach', p.get('description', ''))[:100]}...\n"
                            output += f"   Confidence: {confidence}\n"
                        output += "\n"

                    if universal:
                        output += "**🌍 Universal patterns that apply here:**\n"
                        for i, p in enumerate(universal[:2], 1):
                            confidence = p.get('confidence', 'medium')
                            success_rate = p.get('success_rate', 0)
                            output += f"{i}. {p.get('approach', p.get('description', ''))[:100]}...\n"
                            output += f"   Success rate: {success_rate:.1%} | Confidence: {confidence}\n"
                        output += "\n"

                    if transferable:
                        output += "**🔄 Patterns from similar contexts:**\n"
                        for i, p in enumerate(transferable[:2], 1):
                            confidence = p.get('confidence', 'medium')
                            output += f"{i}. {p.get('approach', p.get('description', ''))[:100]}...\n"
                            output += f"   Transferability: {confidence}\n"

                    return output

        except Exception:
            # Fallback to traditional suggestions
            pass

        # Fallback to original suggestion logic
        patterns = kb.get_project_patterns(project_name, limit=3)

        # Search for context-relevant patterns if context provided
        if context:
            relevant = kb.vector_search.search_patterns(context, limit=3) if kb.vector_search else []
        else:
            relevant = []

        if patterns:
            output += f"**Recent patterns from {project_name}:**\n"
            for i, p in enumerate(patterns, 1):
                output += f"{i}. {p.get('approach', 'No description')[:100]}...\n"
            output += "\n"

        if relevant:
            output += "**Context-relevant patterns:**\n"
            for i, r in enumerate(relevant, 1):
                output += f"{i}. {r.get('content', '')[:100]}...\n"
                output += f"   Relevance: {r.get('similarity', 0):.2%}\n"

        if not patterns and not relevant:
            output += "No suggestions available yet. Save patterns with `/mcp__cache__learn` to build your knowledge base!"

        return output

    except Exception as e:
        return f"❌ Error getting suggestions: {str(e)}"

@mcp.tool()
async def stats() -> str:
    """
    View your Claude Cache knowledge base statistics.
    Shows pattern count, search capabilities, and indexed items.

    Returns:
        Formatted statistics about your knowledge base
    """
    try:
        stats = kb.get_statistics()

        output = "📊 **Claude Cache Statistics**\n\n"
        output += f"**Knowledge Base:**\n"
        output += f"- Total Patterns: {stats.get('total_patterns', 0)}\n"
        output += f"- Projects: {stats.get('projects', 0)}\n"
        output += f"- Documentation: {stats.get('documentation_count', 0)} items\n\n"

        if kb.vector_search:
            caps = kb.vector_search.get_capabilities()
            output += f"**Search Capabilities:**\n"
            output += f"- Mode: {caps['mode']} {'✨' if caps['mode'] == 'semantic' else '⚡'}\n"
            output += f"- Indexed Items: {caps['pattern_count']}\n"

            if caps['mode'] == 'semantic':
                output += "- Features: Context-aware, meaning-based search\n"
            else:
                output += "- Features: Fast keyword matching with TF-IDF\n"

        # Get recent activity
        recent = kb.get_project_patterns(limit=3)
        if recent:
            output += f"\n**Recent Activity:**\n"
            for r in recent:
                timestamp = r.get('timestamp', 'unknown')
                output += f"- {r.get('request_type', 'unknown')} ({timestamp[:10]})\n"

        return output

    except Exception as e:
        return f"❌ Error getting statistics: {str(e)}"

@mcp.tool()
async def browse(url: str, project_name: str = "default") -> str:
    """
    Index and learn from documentation or code repositories.
    Automatically extracts patterns and best practices.

    Args:
        url: URL or file path to documentation/code to index
        project_name: Project to associate the documentation with (default: 'default')

    Returns:
        Summary of extracted patterns and indexed content
    """
    try:
        scanner = DocumentationScanner(kb)

        # Determine if URL or file path
        if url.startswith(('http://', 'https://', 'file://')):
            # Web documentation
            scraped = scanner.scrape_documentation(url)
            if not scraped:
                return f"❌ Failed to fetch documentation from {url}"

            extracted = scanner.extract_lessons(scraped['content'])
            doc_type = 'web'
        else:
            # Local file/directory
            path = Path(url).expanduser().resolve()
            if not path.exists():
                return f"❌ Path not found: {url}"

            if path.is_file():
                content = path.read_text()
                doc_type = 'file'
            else:
                # Directory - read README or main docs
                readme = path / 'README.md'
                if readme.exists():
                    content = readme.read_text()
                    doc_type = 'readme'
                else:
                    return f"❌ No documentation found in directory: {url}"

            extracted = scanner.extract_lessons(content)

        # Store in knowledge base
        kb.store_documentation(
            project_name=project_name,
            file_path=url,
            doc_type=doc_type,
            content=json.dumps(extracted),
            extracted_at=datetime.now().isoformat()
        )

        # Build response
        output = "✅ **Documentation Indexed Successfully!**\n\n"
        output += f"📊 **Extracted Content:**\n"
        output += f"- Lessons: {len(extracted.get('lessons', []))}\n"
        output += f"- Warnings: {len(extracted.get('warnings', []))}\n"
        output += f"- Best Practices: {len(extracted.get('best_practices', []))}\n\n"

        if kb.vector_search:
            output += "🔍 **Auto-indexed for vector search** - Now searchable with `/mcp__cache__query`!\n\n"

        output += "🎯 **Next Steps:**\n"
        output += "- Try: `/mcp__cache__query` with topics from this documentation\n"
        output += "- Use: `/mcp__cache__stats` to see updated knowledge base\n"

        return output

    except Exception as e:
        return f"❌ Error browsing {url}: {str(e)}"

# Main entry point
def main():
    """Entry point for cache-mcp command"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()