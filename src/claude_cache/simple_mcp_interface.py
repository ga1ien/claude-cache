#!/usr/bin/env python3
"""
Simplified MCP Interface for Claude Cache
Focus: Clean, intuitive tool interfaces that just work
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional

# Configure logging to stderr only (stdout corrupts MCP)
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

# Suppress noisy libraries
import warnings
warnings.filterwarnings("ignore")

# Import with minimal overhead
import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    from mcp.server.fastmcp import FastMCP
    # Import Claude Cache silently
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from claude_cache.knowledge_base import KnowledgeBase
    from claude_cache.behavioral_detector import PatternQuality

# Initialize server
mcp = FastMCP("cache")

# Initialize knowledge base in silent mode
kb = KnowledgeBase(silent=True)

@mcp.tool()
async def query(what: str, project: Optional[str] = None) -> str:
    """
    Search your patterns - simple as that.

    Examples:
        query("authentication")
        query("how did I fix that JWT issue")
        query("database connection", project="myapp")
    """
    try:
        # Simple search - no complex parameters
        if project:
            patterns = kb.find_similar_patterns(what, project, threshold=0.2)
        else:
            # Search across all projects
            patterns = kb.find_similar_patterns(what, "default", threshold=0.2)

        if not patterns:
            return f"No patterns found for '{what}'. Save successful solutions with the 'learn' tool!"

        # Simple, clean output
        output = []
        for i, p in enumerate(patterns[:5], 1):
            quality = p.get('quality', 'unknown')
            icon = "🏆" if quality == 'gold' else "✅" if quality == 'silver' else "📝"

            output.append(f"{icon} {p.get('request', 'Pattern')} ({p.get('similarity', 0):.0%} match)")
            output.append(f"   → {p.get('approach', 'Solution')[:100]}")

        return "\n".join(output)

    except Exception as e:
        return f"Search failed: {str(e)}"

@mcp.tool()
async def learn(solution: str, context: Optional[str] = "", tags: Optional[str] = "") -> str:
    """
    Save something that worked. Claude Cache learns from your successes.

    Examples:
        learn("Fixed auth by adding JWT refresh token logic")
        learn("useEffect cleanup prevented memory leak", context="React hooks")
        learn("Async/await in map doesn't work", tags="javascript,gotcha")
    """
    try:
        # Auto-detect project from context
        project = _detect_current_project()

        # Determine quality based on context
        quality = PatternQuality.SILVER  # Default to silver (good solution)
        if "perfect" in solution.lower() or "elegant" in solution.lower():
            quality = PatternQuality.GOLD
        elif "eventually" in solution.lower() or "finally" in solution.lower():
            quality = PatternQuality.BRONZE

        # Store the pattern
        pattern_data = {
            'user_request': context or "General solution",
            'approach': solution,
            'solution_steps': [solution],
            'tags': tags.split(',') if tags else [],
            'pattern_quality': quality.value
        }

        kb.store_success_pattern(pattern_data, project, success_score=0.8)

        icon = "🏆" if quality == PatternQuality.GOLD else "✅"
        return f"{icon} Saved to {project}! This pattern will help you next time."

    except Exception as e:
        return f"Failed to save: {str(e)}"

@mcp.tool()
async def suggest(context: Optional[str] = "") -> str:
    """
    Get smart suggestions based on what you're working on.

    Examples:
        suggest()  # General suggestions
        suggest("working on API endpoints")
        suggest("debugging React component")
    """
    try:
        project = _detect_current_project()

        # Get recent patterns for context
        patterns = kb.get_project_patterns(project, limit=3)

        if not patterns:
            return "💡 No patterns yet. Start saving successful solutions with 'learn'!"

        output = ["💡 Based on your recent work:"]

        for p in patterns:
            approach = p.get('approach', '')[:80]
            output.append(f"• {approach}")

        if context:
            # Try to find relevant patterns
            similar = kb.find_similar_patterns(context, project, threshold=0.3)
            if similar:
                output.append(f"\n📌 Relevant to '{context}':")
                output.append(f"• {similar[0].get('approach', '')[:80]}")

        return "\n".join(output)

    except Exception as e:
        return f"Suggestion failed: {str(e)}"

@mcp.tool()
async def stats() -> str:
    """
    Quick stats about your knowledge base.
    """
    try:
        import sqlite3
        conn = sqlite3.connect(kb.db_path)
        cursor = conn.cursor()

        # Get pattern counts
        cursor.execute("SELECT COUNT(*) FROM success_patterns")
        total_patterns = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM success_patterns WHERE pattern_quality = 'gold'")
        gold_patterns = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT project_name) FROM success_patterns")
        projects = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM anti_patterns")
        anti_patterns = cursor.fetchone()[0]

        conn.close()

        return f"""📊 Claude Cache Stats:
• {total_patterns} total patterns ({gold_patterns} gold 🏆)
• {anti_patterns} anti-patterns (things to avoid)
• {projects} projects tracked
• Knowledge base: {Path(kb.db_path).name}"""

    except Exception as e:
        return f"Stats failed: {str(e)}"

@mcp.tool()
async def browse(url: str, project: Optional[str] = None) -> str:
    """
    Index documentation or code from a URL/path.

    Examples:
        browse("https://docs.python.org/3/tutorial/")
        browse("/path/to/project/README.md")
    """
    try:
        project = project or _detect_current_project()

        # Simple validation
        if not url:
            return "Please provide a URL or file path to index"

        # Store as documentation
        kb.store_documentation(url, project, "external", url)

        return f"📚 Indexed {url} for project {project}"

    except Exception as e:
        return f"Browse failed: {str(e)}"

def _detect_current_project() -> str:
    """Simple project detection from current directory"""
    try:
        cwd = Path.cwd()
        # Use directory name as project
        project = cwd.name

        # Skip common non-project directories
        if project in ['src', 'lib', 'test', 'tests']:
            project = cwd.parent.name

        return project.lower()
    except:
        return "default"

def main():
    """Run the MCP server"""
    try:
        mcp.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()