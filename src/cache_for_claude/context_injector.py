"""Inject context and generate slash commands for Claude Code"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown

console = Console()


class ContextInjector:
    """Generate context and slash commands from knowledge base"""

    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.commands_dir = Path('.claude/commands')

    def generate_context_for_request(self, user_request: str, project_name: str) -> Optional[str]:
        """Generate context for a specific request"""
        similar_patterns = self.kb.find_similar_patterns(user_request, project_name)

        if not similar_patterns:
            console.print("[yellow]No similar patterns found[/yellow]")
            return None

        context = self.build_context_prompt(similar_patterns, project_name)

        self.save_as_slash_command(context, 'project-context', project_name)

        return context

    def build_context_prompt(self, patterns: List[Dict], project_name: str) -> str:
        """Build a comprehensive context prompt"""
        context_lines = [
            f"# Project Context: {project_name}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Relevant Successful Patterns",
            ""
        ]

        for i, pattern in enumerate(patterns, 1):
            similarity = pattern['similarity']
            context_lines.extend([
                f"### Pattern {i} (Similarity: {similarity:.1%})",
                "",
                f"**Previous Request:**",
                f"> {pattern['request']}",
                "",
                f"**Approach:** {pattern['approach']}",
                ""
            ])

            if pattern['solution_steps']:
                context_lines.append("**Solution Steps:**")
                for step in pattern['solution_steps'][:3]:
                    context_lines.append(f"- {step.get('action', 'Step')}")
                context_lines.append("")

            if pattern['files_involved']:
                context_lines.append("**Files Involved:**")
                for file in pattern['files_involved'][:5]:
                    context_lines.append(f"- `{Path(file).name}`")
                context_lines.append("")

            if pattern['key_operations']:
                context_lines.append("**Key Operations:**")
                for op in pattern['key_operations'][:3]:
                    tool = op.get('tool', 'Unknown')
                    if op.get('file'):
                        context_lines.append(f"- {tool}: `{Path(op['file']).name}`")
                    else:
                        context_lines.append(f"- {tool}")
                context_lines.append("")

        context_lines.extend([
            "## Recommendations",
            "",
            "Based on previous successful sessions:",
            "1. Consider using the same approach that worked before",
            "2. Check the files that were previously involved",
            "3. Follow similar solution steps adapted to current context",
            ""
        ])

        return '\n'.join(context_lines)

    def save_as_slash_command(self, content: str, command_name: str, project_name: str):
        """Save content as a Claude Code slash command"""
        self.commands_dir.mkdir(parents=True, exist_ok=True)

        command_file = self.commands_dir / f"{command_name}.md"

        header = f"""# {command_name.replace('-', ' ').title()}

Load relevant context for: $ARGUMENTS

---

"""

        with open(command_file, 'w') as f:
            f.write(header + content)

        console.print(f"[green]✓ Saved command: /{command_name}[/green]")

    def generate_all_commands(self, project_name: str):
        """Generate all useful slash commands for a project"""
        stats = self.kb.get_statistics(project_name)

        if stats.get('patterns', 0) == 0:
            console.print("[yellow]No patterns found for project[/yellow]")
            return

        self._generate_best_practices_command(project_name)
        self._generate_conventions_command(project_name)
        self._generate_quick_reference_command(project_name)
        self._generate_debug_helper_command(project_name)

        console.print(f"[green]✓ Generated all commands for {project_name}[/green]")

    def _generate_best_practices_command(self, project_name: str):
        """Generate best practices command"""
        conn = self.kb.db_path
        import sqlite3
        conn = sqlite3.connect(self.kb.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT approach, COUNT(*) as count, AVG(success_score) as avg_score
            FROM success_patterns
            WHERE project_name = ?
            GROUP BY approach
            ORDER BY avg_score DESC, count DESC
            LIMIT 10
        ''', (project_name,))

        approaches = cursor.fetchall()
        conn.close()

        if not approaches:
            return

        content_lines = [
            f"# Best Practices for {project_name}",
            "",
            "## Most Successful Approaches",
            ""
        ]

        for approach, count, score in approaches:
            content_lines.append(f"- **{approach}**: Used {count} times (Success: {score:.1%})")

        content_lines.extend([
            "",
            "## Usage Tips",
            "",
            "1. Start with exploration if unfamiliar with the codebase",
            "2. Test changes incrementally",
            "3. Review similar successful patterns before starting",
            ""
        ])

        self.save_as_slash_command('\n'.join(content_lines), 'best-practices', project_name)

    def _generate_conventions_command(self, project_name: str):
        """Generate project conventions command"""
        conventions = self.kb.get_project_conventions(project_name)

        if not conventions:
            return

        content_lines = [
            f"# Project Conventions for {project_name}",
            "",
            "## Detected Patterns",
            ""
        ]

        by_type = {}
        for conv in conventions:
            conv_type = conv['type']
            if conv_type not in by_type:
                by_type[conv_type] = []
            by_type[conv_type].append(conv)

        for conv_type, items in by_type.items():
            content_lines.append(f"### {conv_type.replace('_', ' ').title()}")
            content_lines.append("")

            for item in items[:5]:
                content_lines.append(f"- {item['pattern']}")
                if item['description']:
                    content_lines.append(f"  {item['description']}")

            content_lines.append("")

        self.save_as_slash_command('\n'.join(content_lines), 'conventions', project_name)

    def _generate_quick_reference_command(self, project_name: str):
        """Generate quick reference command"""
        import sqlite3
        conn = sqlite3.connect(self.kb.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT files_involved
            FROM success_patterns
            WHERE project_name = ?
        ''', (project_name,))

        all_files = []
        for row in cursor.fetchall():
            if row[0]:
                files = json.loads(row[0])
                all_files.extend(files)

        from collections import Counter
        file_counts = Counter(all_files)
        common_files = file_counts.most_common(10)

        cursor.execute('''
            SELECT tool, COUNT(*) as count
            FROM tool_usage
            WHERE project_name = ? AND success = 1
            GROUP BY tool
            ORDER BY count DESC
            LIMIT 10
        ''', (project_name,))

        common_tools = cursor.fetchall()
        conn.close()

        content_lines = [
            f"# Quick Reference for {project_name}",
            "",
            "## Most Modified Files",
            ""
        ]

        for file_path, count in common_files:
            file_name = Path(file_path).name
            content_lines.append(f"- `{file_name}` ({count} times)")

        content_lines.extend([
            "",
            "## Most Used Tools",
            ""
        ])

        for tool, count in common_tools:
            content_lines.append(f"- **{tool}**: {count} uses")

        self.save_as_slash_command('\n'.join(content_lines), 'quick-ref', project_name)

    def _generate_debug_helper_command(self, project_name: str):
        """Generate debugging helper command"""
        import sqlite3
        conn = sqlite3.connect(self.kb.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT user_request, solution_steps
            FROM success_patterns
            WHERE project_name = ? AND request_type = 'debugging'
            ORDER BY success_score DESC
            LIMIT 5
        ''', (project_name,))

        debug_patterns = cursor.fetchall()
        conn.close()

        if not debug_patterns:
            return

        content_lines = [
            f"# Debug Helper for {project_name}",
            "",
            "## Previous Debugging Solutions",
            ""
        ]

        for i, (request, steps_json) in enumerate(debug_patterns, 1):
            content_lines.extend([
                f"### Debug Case {i}",
                "",
                f"**Issue:** {request[:100]}",
                ""
            ])

            if steps_json:
                steps = json.loads(steps_json)
                if steps:
                    content_lines.append("**Solution:**")
                    for step in steps[:3]:
                        content_lines.append(f"- {step.get('action', 'Step')}")
                    content_lines.append("")

        content_lines.extend([
            "## Debug Checklist",
            "",
            "1. Check error messages and stack traces",
            "2. Review recent changes to affected files",
            "3. Verify dependencies and imports",
            "4. Test with minimal reproduction case",
            "5. Check similar patterns above",
            ""
        ])

        self.save_as_slash_command('\n'.join(content_lines), 'debug-helper', project_name)

    def export_commands_to_claude_md(self, project_name: str):
        """Export patterns to a CLAUDE.md file"""
        claude_md_path = Path('.claude') / 'CLAUDE.md'
        claude_md_path.parent.mkdir(exist_ok=True)

        stats = self.kb.get_statistics(project_name)
        patterns = self.kb.find_similar_patterns('', project_name)[:10]

        content_lines = [
            f"# Claude Code Knowledge Base for {project_name}",
            "",
            f"*Auto-generated from {stats.get('patterns', 0)} successful patterns*",
            "",
            "## Project Overview",
            "",
            f"- Total Patterns: {stats.get('patterns', 0)}",
            f"- Conventions: {stats.get('conventions', 0)}",
            f"- Analyzed Requests: {stats.get('requests', 0)}",
            "",
            "## Key Success Patterns",
            ""
        ]

        for i, pattern in enumerate(patterns[:5], 1):
            content_lines.extend([
                f"### Pattern {i}",
                f"- **Request:** {pattern['request'][:100]}",
                f"- **Approach:** {pattern['approach']}",
                f"- **Success Score:** {pattern['success_score']:.1%}",
                ""
            ])

        content_lines.extend([
            "## Usage",
            "",
            "This knowledge base is automatically maintained by Claude Cache.",
            "Use slash commands to access specific patterns:",
            "",
            "- `/project-context [task]` - Get relevant patterns for a task",
            "- `/best-practices` - Show successful approaches",
            "- `/conventions` - Show project conventions",
            "- `/quick-ref` - Quick reference for files and tools",
            "- `/debug-helper` - Debugging assistance",
            ""
        ])

        with open(claude_md_path, 'w') as f:
            f.write('\n'.join(content_lines))

        console.print(f"[green]✓ Exported to {claude_md_path}[/green]")