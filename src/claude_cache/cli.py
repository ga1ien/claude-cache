"""Command-line interface for Claude Cache"""

import click
import sys
from pathlib import Path
from rich.console import Console
from datetime import datetime

from . import __version__
from .agent import CacheAgent
from .daemon import CacheDaemon

console = Console()

ASCII_ART = """                              claude
 ██████╗ █████╗  ██████╗██╗  ██╗███████╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝
██║     ███████║██║     ███████║█████╗
██║     ██╔══██║██║     ██╔══██║██╔══╝
╚██████╗██║  ██║╚██████╗██║  ██║███████╗
 ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝"""


@click.group()
@click.version_option(version=__version__, prog_name="cache")
def cli():
    """Claude Cache - Give your AI coding assistant perfect recall

    Quick Start: cache run  (starts background learning + terminal interface)
    For Claude Code: cache-mcp  (run separately for MCP integration)
    """
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
@click.option('--foreground', '-f', is_flag=True, help='Run in foreground instead of background')
@click.option('--with-mcp', is_flag=True, help='Also start MCP server (usually not needed)')
@click.option('--db', type=click.Path(), help='Custom database path')
def run(foreground, with_mcp, db):
    """Start Claude Cache: background learning + vector search + terminal interface"""
    import subprocess
    import time

    console.print(f"[bold cyan]{ASCII_ART}[/bold cyan]")
    console.print(f"[bold]Starting Claude Cache v{__version__} - Terminal & Learning System[/bold]\n")

    processes = []

    try:
        # Start background learning agent directly (no daemon)
        console.print("🔄 [cyan]Starting background learning system...[/cyan]")
        agent = CacheAgent(db)

        if foreground:
            # Start agent in foreground
            console.print("✅ [green]Background learning active[/green]")
            console.print("\n[dim]Running in foreground mode. Press Ctrl+C to stop.[/dim]")
            agent.start(watch=True)
        else:
            # Start agent as background subprocess
            import subprocess
            import sys

            # Start the agent using cache start command in background
            subprocess.Popen([
                sys.executable, '-c',
                f'from claude_cache.agent import CacheAgent; '
                f'agent = CacheAgent("{db}" if "{db}" != "None" else None); '
                f'agent.start(watch=True)'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            console.print("✅ [green]Background learning started[/green]")
            time.sleep(1)  # Give agent time to start

        # Start MCP server only if explicitly requested
        if with_mcp:
            console.print("🔗 [cyan]Starting MCP server for Claude Code integration...[/cyan]")
            if foreground:
                console.print("⚠️  [yellow]Cannot run MCP server in foreground mode[/yellow]")
                console.print("    Run 'cache-mcp' separately for Claude Code integration")
            else:
                # Start MCP server as subprocess
                mcp_process = subprocess.Popen(
                    ['cache-mcp'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                processes.append(('cache-mcp', mcp_process))
                console.print("✅ [green]MCP server started[/green]")

        if not foreground:
            console.print("\n🎉 [bold green]Claude Cache is now running![/bold green]")
            console.print("\n[bold]What's running:[/bold]")
            console.print("  • 🧠 Background learning agent (monitors Claude Code every 30s)")
            console.print("  • 🔍 Vector search and pattern intelligence")
            console.print("  • 💻 Full terminal interface available")

            console.print("\n[bold]Try these terminal commands:[/bold]")
            console.print("  • [cyan]cache query \"authentication patterns\"[/cyan]")
            console.print("  • [cyan]cache stats[/cyan]")
            console.print("  • [cyan]cache suggest --context \"working on API\"[/cyan]")
            console.print("  • [cyan]cache learn \"solution here\" --tags auth,api[/cyan]")

            if not with_mcp:
                console.print("\n[bold]For Claude Code integration:[/bold]")
                console.print("  • Run [cyan]cache-mcp[/cyan] separately")
                console.print("  • Or use [cyan]cache run --with-mcp[/cyan]")

            console.print("\n[bold]Stop with:[/bold]")
            console.print("  • [cyan]pkill -f 'CacheAgent'[/cyan]")
            if with_mcp:
                console.print("  • [cyan]pkill cache-mcp[/cyan]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping Claude Cache...[/yellow]")
        for name, process in processes:
            try:
                process.terminate()
                console.print(f"✅ Stopped {name}")
            except:
                pass
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error starting Claude Cache: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--db', type=click.Path(), help='Custom database path')
def background(db):
    """Start Claude Cache in background using simple subprocess (no daemon)"""
    import subprocess
    import sys

    console.print(f"[bold cyan]{ASCII_ART}[/bold cyan]")
    console.print(f"[bold]Starting Claude Cache v{__version__} in Background[/bold]\n")

    console.print("🔄 [cyan]Starting background process...[/cyan]")

    # Use nohup approach for background execution
    cmd = [
        'nohup', 'cache', 'start', '--watch'
    ]

    if db:
        cmd.extend(['--db', db])

    try:
        # Start in background, redirect output to log file
        subprocess.Popen(
            cmd + ['>', '/tmp/claude-cache.log', '2>&1', '&'],
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        console.print("✅ [green]Background process started![/green]")
        console.print("\n[bold]Claude Cache is now running in background![/bold]")
        console.print("\n[bold]What's running:[/bold]")
        console.print("  • 🧠 Background learning (monitors Claude Code)")
        console.print("  • 🔍 Vector search and pattern intelligence")
        console.print("  • 💻 Terminal commands available")

        console.print("\n[bold]Try these commands:[/bold]")
        console.print("  • [cyan]cache query \"patterns\"[/cyan]")
        console.print("  • [cyan]cache stats[/cyan]")
        console.print("  • [cyan]cache suggest[/cyan]")

        console.print("\n[bold]Stop with:[/bold]")
        console.print("  • [cyan]pkill -f 'cache start'[/cyan]")
        console.print("\n[bold]View logs:[/bold]")
        console.print("  • [cyan]tail -f /tmp/claude-cache.log[/cyan]")

    except Exception as e:
        console.print(f"[red]Error starting background process: {e}[/red]")
        sys.exit(1)


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
@click.argument('solution')
@click.option('--context', '-c', help='Additional context about the solution')
@click.option('--tags', '-t', help='Comma-separated tags for categorization')
@click.option('--project', '-p', help='Project name (defaults to current directory)')
@click.option('--db', type=click.Path(), help='Custom database path')
def learn(solution, context, tags, project, db):
    """Save a successful solution to your knowledge base"""
    try:
        agent = CacheAgent(db)

        # Use current directory as project if not specified
        if not project:
            project = Path.cwd().name

        pattern = {
            'request_type': 'manual_save',
            'user_request': context or '',
            'approach': solution,
            'solution_steps': [solution],
            'tags': tags.split(',') if tags else [],
            'timestamp': datetime.now().isoformat()
        }

        agent.kb.store_success_pattern(pattern, project)

        console.print(f"✅ [green]Pattern saved successfully![/green]")
        console.print(f"🏷️  Tags: {tags or 'none'}")
        console.print(f"📁 Project: {project}")

    except Exception as e:
        console.print(f"[red]Error saving pattern: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('url')
@click.option('--project', '-p', help='Project name (defaults to current directory)')
@click.option('--db', type=click.Path(), help='Custom database path')
def browse(url, project, db):
    """Index documentation from URL or file path"""
    try:
        from .doc_scanner import DocumentationScanner
        import json

        agent = CacheAgent(db)
        scanner = DocumentationScanner(agent.kb)

        # Use current directory as project if not specified
        if not project:
            project = Path.cwd().name

        console.print(f"[cyan]Indexing documentation: {url}[/cyan]")

        # Determine if URL or file path
        if url.startswith(('http://', 'https://', 'file://')):
            # Web documentation
            scraped = scanner.scrape_documentation(url)
            if not scraped:
                console.print(f"[red]❌ Failed to fetch documentation from {url}[/red]")
                sys.exit(1)

            extracted = scanner.extract_lessons(scraped['content'])
            doc_type = 'web'
        else:
            # Local file/directory
            path = Path(url).expanduser().resolve()
            if not path.exists():
                console.print(f"[red]❌ Path not found: {url}[/red]")
                sys.exit(1)

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
                    console.print(f"[red]❌ No documentation found in directory: {url}[/red]")
                    sys.exit(1)

            extracted = scanner.extract_lessons(content)

        # Store in knowledge base
        agent.kb.store_documentation(
            project_name=project,
            file_path=url,
            doc_type=doc_type,
            content=json.dumps(extracted),
            extracted_at=datetime.now().isoformat()
        )

        console.print("✅ [green]Documentation indexed successfully![/green]")
        console.print(f"📊 Extracted Content:")
        console.print(f"  • Lessons: {len(extracted.get('lessons', []))}")
        console.print(f"  • Warnings: {len(extracted.get('warnings', []))}")
        console.print(f"  • Best Practices: {len(extracted.get('best_practices', []))}")
        console.print(f"📁 Project: {project}")

    except Exception as e:
        console.print(f"[red]Error indexing documentation: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--context', '-c', help='Current work context for relevant suggestions')
@click.option('--project', '-p', help='Project name (defaults to current directory)')
@click.option('--db', type=click.Path(), help='Custom database path')
def suggest(context, project, db):
    """Get proactive recommendations based on current context"""
    try:
        agent = CacheAgent(db)

        # Use current directory as project if not specified
        if not project:
            project = Path.cwd().name

        # Get project patterns
        patterns = agent.kb.get_project_patterns(project, limit=3)

        # Search for context-relevant patterns if context provided
        relevant = []
        if context:
            try:
                if hasattr(agent.kb, 'vector_search') and agent.kb.vector_search:
                    relevant = agent.kb.vector_search.search_patterns(context, limit=3)
                else:
                    # Fallback to basic pattern search
                    all_patterns = agent.kb.search_patterns(context, limit=3)
                    relevant = [{'content': p.get('approach', ''), 'similarity': 0.5} for p in all_patterns]
            except Exception:
                # Silent fallback if vector search fails
                pass

        console.print("💡 [bold]Suggestions for your current work:[/bold]\n")

        if patterns:
            console.print(f"[bold]Recent patterns from {project}:[/bold]")
            for i, p in enumerate(patterns, 1):
                approach = p.get('approach', 'No description')[:100]
                console.print(f"{i}. {approach}...")
            console.print()

        if relevant:
            console.print("[bold]Context-relevant patterns:[/bold]")
            for i, r in enumerate(relevant, 1):
                content = r.get('content', '')[:100]
                similarity = r.get('similarity', 0)
                console.print(f"{i}. {content}...")
                console.print(f"   Relevance: {similarity:.2%}")
            console.print()

        if not patterns and not relevant:
            console.print("[yellow]No suggestions available yet.[/yellow]")
            console.print("Save patterns with [cyan]cache learn[/cyan] to build your knowledge base!")

    except Exception as e:
        console.print(f"[red]Error getting suggestions: {e}[/red]")
        sys.exit(1)


@cli.command()
def info():
    """Show information about Claude Cache"""
    console.print(f"[bold cyan]{ASCII_ART}[/bold cyan]")
    console.print(f"[bold cyan]Claude Cache v{__version__}[/bold cyan]")
    console.print("[bold]Give your AI coding assistant perfect recall[/bold]\n")

    console.print("[bold]Overview:[/bold]")
    console.print("Claude Cache automatically learns from every successful solution and provides")
    console.print("instant access to your accumulated knowledge directly within Claude Code.\n")

    console.print("[bold]Features:[/bold]")
    console.print("• 🔄 Never solve the same problem twice")
    console.print("• 🔍 Semantic search with AI understanding")
    console.print("• ⚡ Zero context switching in Claude Code")
    console.print("• 🏗️ Cross-project pattern recognition")
    console.print("• 📚 Documentation indexing and search\n")

    console.print("[bold]Claude Code Integration:[/bold]")
    console.print("Add to your .claude.json:")
    console.print('[cyan]{"mcpServers": {"cache": {"type": "stdio", "command": "cache-mcp"}}}[/cyan]\n')

    console.print("[bold]CLI Quick Start:[/bold]")
    console.print("1. [cyan]cache learn[/cyan] \"Fixed CORS issue with middleware\" --tags cors,api")
    console.print("2. [cyan]cache query[/cyan] \"authentication problems\"")
    console.print("3. [cyan]cache suggest[/cyan] --context \"working on API endpoints\"")
    console.print("4. [cyan]cache browse[/cyan] https://docs.example.com")
    console.print("5. [cyan]cache stats[/cyan] to see your knowledge base\n")

    console.print("[bold]Storage:[/bold]")
    console.print("All data stored locally in ~/.claude/knowledge/ - completely private\n")

    console.print("[bold]Documentation:[/bold]")
    console.print("https://github.com/ga1ien/claude-cache")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()