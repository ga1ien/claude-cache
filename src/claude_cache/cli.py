"""Command-line interface for Claude Cache"""

import click
import sys
from pathlib import Path
from rich.console import Console

from . import __version__
from .agent import CacheAgent
from .daemon import CacheDaemon

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="cache")
def cli():
    """Claude Cache - Memory for your AI coding assistant"""
    pass


@cli.command()
@click.option('--watch/--no-watch', default=True, help='Enable real-time monitoring')
@click.option('--daemon', is_flag=True, help='Run as background daemon')
@click.option('--db', type=click.Path(), help='Custom database path')
def start(watch, daemon, db):
    """Start processing Claude Code logs"""
    if daemon:
        # Run as daemon
        d = CacheDaemon()
        d.start()
    else:
        # Run in foreground
        try:
            agent = CacheAgent(db)
            agent.start(watch=watch)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)


@cli.command()
@click.option('--db', type=click.Path(), help='Custom database path')
def process(db):
    """Process existing logs without monitoring"""
    try:
        agent = CacheAgent(db)
        agent.process_existing_logs()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--project', '-p', help='Filter by project name')
@click.option('--db', type=click.Path(), help='Custom database path')
def query(query, project, db):
    """Query patterns from the knowledge base"""
    try:
        agent = CacheAgent(db)
        agent.query_patterns(query, project)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--project', '-p', help='Generate for specific project')
@click.option('--db', type=click.Path(), help='Custom database path')
def generate(project, db):
    """Generate slash commands for Claude Code"""
    try:
        agent = CacheAgent(db)

        if project:
            projects = [project]
        else:
            projects = agent.get_projects()

        if not projects:
            console.print("[yellow]No projects found[/yellow]")
            return

        for proj in projects:
            console.print(f"[blue]Generating commands for {proj}...[/blue]")
            agent.injector.generate_all_commands(proj)
            agent.injector.export_commands_to_claude_md(proj)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--project', '-p', help='Filter by project')
@click.option('--db', type=click.Path(), help='Custom database path')
def stats(project, db):
    """Show knowledge base statistics"""
    try:
        agent = CacheAgent(db)

        if project:
            stats = agent.kb.get_statistics(project)
            console.print(f"\n[bold]Statistics for {project}[/bold]")
        else:
            stats = agent.kb.get_statistics()
            console.print("\n[bold]Overall Statistics[/bold]")

        for key, value in stats.items():
            console.print(f"  {key.replace('_', ' ').title()}: [green]{value}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('output_file', type=click.Path())
@click.option('--project', '-p', help='Export specific project')
@click.option('--db', type=click.Path(), help='Custom database path')
def export(output_file, project, db):
    """Export knowledge base to JSON file"""
    try:
        agent = CacheAgent(db)
        agent.export_knowledge(output_file, project)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command(name='import')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--db', type=click.Path(), help='Custom database path')
def import_kb(input_file, db):
    """Import patterns from JSON file"""
    try:
        agent = CacheAgent(db)
        agent.import_knowledge(input_file)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--confirm', is_flag=True, help='Confirm rebuild without prompt')
@click.option('--db', type=click.Path(), help='Custom database path')
def rebuild(confirm, db):
    """Rebuild knowledge base from scratch"""
    try:
        if not confirm:
            if not click.confirm('This will delete all existing patterns. Continue?'):
                console.print("[yellow]Cancelled[/yellow]")
                return

        agent = CacheAgent(db)
        agent.rebuild_index()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('request')
@click.option('--project', '-p', required=True, help='Project name')
@click.option('--db', type=click.Path(), help='Custom database path')
def context(request, project, db):
    """Generate context for a specific request"""
    try:
        agent = CacheAgent(db)
        context = agent.injector.generate_context_for_request(request, project)

        if context:
            console.print(context)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('action', default='status', type=click.Choice(['start', 'stop', 'restart', 'status']))
def daemon(action):
    """Manage Claude Cache daemon process"""
    d = CacheDaemon()

    if action == 'start':
        d.start()
    elif action == 'stop':
        d.stop()
    elif action == 'restart':
        d.restart()
    elif action == 'status':
        d.status()


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True), default='.')
@click.option('--project', '-p', help='Project name (defaults to directory name)')
@click.option('--db', type=click.Path(), help='Custom database path')
def scan_docs(repo_path, project, db):
    """Scan repository for documentation and lessons learned"""
    try:
        from .doc_scanner import DocumentationScanner

        agent = CacheAgent(db)
        scanner = DocumentationScanner(agent.kb)

        # Use current directory if not specified
        repo_path = Path(repo_path).resolve()

        console.print(f"[cyan]Scanning repository: {repo_path}[/cyan]")
        docs = scanner.scan_repository(str(repo_path), project)

        console.print(f"\n[green]✓ Successfully scanned {len(docs)} documents[/green]")

        # Show summary of what was found
        if docs:
            lessons_count = sum(len(d.lessons_learned) for d in docs)
            warnings_count = sum(len(d.warnings) for d in docs)
            practices_count = sum(len(d.best_practices) for d in docs)

            console.print("\n[bold]Summary:[/bold]")
            console.print(f"  • Lessons learned: {lessons_count}")
            console.print(f"  • Warnings/gotchas: {warnings_count}")
            console.print(f"  • Best practices: {practices_count}")
            console.print(f"  • Code examples: {sum(len(d.code_examples) for d in docs)}")

            console.print("\n[dim]Documentation has been added to your knowledge base.[/dim]")
            console.print("[dim]It will be included in future context generation.[/dim]")

    except Exception as e:
        console.print(f"[red]Error scanning documentation: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--query', '-q', help='Search for specific content')
@click.option('--project', '-p', help='Filter by project name')
@click.option('--type', '-t', help='Filter by document type (lessons, architecture, guide, etc.)')
@click.option('--db', type=click.Path(), help='Custom database path')
def search_docs(query, project, type, db):
    """Search through indexed documentation"""
    try:
        from .doc_scanner import DocumentationScanner
        import json

        agent = CacheAgent(db)
        scanner = DocumentationScanner(agent.kb)

        results = scanner.kb.search_documentation(query, project)

        if not results:
            console.print("[yellow]No documentation found matching your search[/yellow]")
            return

        console.print(f"\n[bold]Found {len(results)} documents:[/bold]\n")

        for result in results[:5]:  # Show top 5
            doc_data = json.loads(result['content'])

            console.print(f"[cyan]{result['file_path']}[/cyan] ({result['doc_type']})")

            if doc_data.get('lessons_learned'):
                console.print("  [bold]Lessons:[/bold]")
                for lesson in doc_data['lessons_learned'][:3]:
                    console.print(f"    • {lesson[:80]}...")

            if doc_data.get('warnings'):
                console.print("  [bold]Warnings:[/bold]")
                for warning in doc_data['warnings'][:2]:
                    console.print(f"    ⚠️  {warning[:80]}...")

            console.print()

    except Exception as e:
        console.print(f"[red]Error searching documentation: {e}[/red]")
        sys.exit(1)


@cli.command()
def info():
    """Show information about Claude Cache"""
    console.print(f"""
[bold cyan]Claude Cache v{__version__}[/bold cyan]

[bold]Overview:[/bold]
Claude Cache builds memory from your Claude Code interactions,
creating a personalized knowledge base of successful patterns.

[bold]Features:[/bold]
• Real-time log monitoring
• Success pattern detection
• Context generation for similar tasks
• Slash command generation for Claude Code
• Project convention tracking
• Export/import for team sharing

[bold]Quick Start:[/bold]
1. Run [cyan]cache start[/cyan] to begin monitoring
2. Use Claude Code as normal
3. Access patterns with slash commands in .claude/commands/

[bold]Log Location:[/bold]
~/.claude/projects/

[bold]Database Location:[/bold]
~/.claude/knowledge/cache.db

[bold]Documentation:[/bold]
https://github.com/yourusername/claude-cache
""")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()