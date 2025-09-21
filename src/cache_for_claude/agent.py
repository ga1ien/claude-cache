"""Main agent that coordinates all components"""

import time
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text

from .log_watcher import LogWatcher
from .log_processor import LogProcessor
from .enhanced_detector import EnhancedSuccessDetector
from .knowledge_base import KnowledgeBase
from .context_injector import ContextInjector
from .realtime_updater import RealtimeContextUpdater, HotReloadWatcher

console = Console()


class CacheAgent:
    """Main agent that caches successful patterns from Claude Code"""

    def __init__(self, db_path: Optional[str] = None):
        self.kb = KnowledgeBase(db_path)
        self.processor = LogProcessor(self.kb)
        self.detector = EnhancedSuccessDetector()  # Using enhanced detector for better stack awareness
        self.injector = ContextInjector(self.kb)
        self.watcher = LogWatcher(self.processor)
        self.realtime_updater = RealtimeContextUpdater(self.kb, self.injector)
        self.config_watcher = HotReloadWatcher()

        self.processor.detector = self.detector

    def start(self, watch: bool = True):
        """Start the agent"""
        # Display beautiful ASCII banner
        self._show_banner()

        console.print(Panel.fit(
            "[bold cyan]Claude Cache[/bold cyan]\n"
            "[italic]Building memory from your AI coding sessions[/italic]",
            padding=(1, 2),
            border_style="cyan"
        ))

        console.print("[blue]Processing existing logs...[/blue]")
        self.process_existing_logs()

        if watch:
            console.print("[blue]Starting real-time monitoring...[/blue]")
            self.start_monitoring()

    def process_existing_logs(self):
        """Process all existing log files with progress tracking"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:

                # Process existing logs
                task = progress.add_task("[cyan]Processing existing logs...", total=100)
                self.watcher.process_existing_logs()
                progress.update(task, advance=30)

                projects = self.get_projects()
                if projects:
                    per_project = 70 // len(projects)

                    for project in projects:
                        progress.update(task, description=f"[cyan]Analyzing {project}...")
                        self.analyze_project_sessions(project)
                        progress.update(task, advance=per_project//3)

                        self.injector.generate_all_commands(project)
                        progress.update(task, advance=per_project//3)

                        self.injector.export_commands_to_claude_md(project)
                        progress.update(task, advance=per_project//3)

                progress.update(task, completed=100, description="[green]✓ Processing complete!")

            self.show_statistics()
        except Exception as e:
            import traceback
            console.print(f"[red]Error during log processing: {e}[/red]")
            console.print(f"[dim]Traceback:\n{traceback.format_exc()}[/dim]")
            raise

    def start_monitoring(self):
        """Start real-time log monitoring with context updates"""
        # Start real-time context updates
        self.realtime_updater.start()

        # Start config hot-reload
        self.config_watcher.start()

        # Start log monitoring
        observer = self.watcher.start()

        try:
            with Live(self.generate_status_table(), refresh_per_second=1) as live:
                while True:
                    time.sleep(1)
                    live.update(self.generate_status_table())

        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping monitoring...[/yellow]")
            self.realtime_updater.stop()
            self.config_watcher.stop()
            self.watcher.stop()

    def analyze_project_sessions(self, project_name: str):
        """Analyze sessions for a project and extract patterns"""
        sessions = self.processor.session_tracker.sessions.get(project_name, [])

        patterns_found = 0
        for session in sessions:
            result = self.detector.analyze_session_success(session['entries'])

            if result['success']:
                pattern = result['pattern']
                self.kb.store_success_pattern(pattern, project_name, result['score'])
                patterns_found += 1

                self.detect_and_store_conventions(session, project_name)

        if patterns_found > 0:
            console.print(f"[green]✓ Found {patterns_found} successful patterns in {project_name}[/green]")

    def detect_and_store_conventions(self, session: dict, project_name: str):
        """Detect and store project conventions from sessions"""
        file_operations = session.get('file_operations', [])

        for op in file_operations:
            # Handle both object and dict formats
            if hasattr(op, 'data'):
                data = op.data
            else:
                data = op if isinstance(op, dict) else {}

            if data.get('tool') == 'Edit':
                args = data.get('args', {})
                old_str = args.get('old_string', '')
                new_str = args.get('new_string', '')

                if 'import' in old_str or 'import' in new_str:
                    self.kb.store_convention(
                        project_name,
                        'import_pattern',
                        new_str[:100] if new_str else old_str[:100],
                        'Import convention'
                    )

    def get_projects(self):
        """Get list of all projects"""
        projects_dir = Path.home() / '.claude' / 'projects'
        if not projects_dir.exists():
            return []

        return [d.name for d in projects_dir.iterdir() if d.is_dir()]

    def show_statistics(self):
        """Display enhanced knowledge base statistics"""
        stats = self.kb.get_statistics()

        # Create a beautiful statistics display
        table = Table(
            title="✨ Claude Cache Statistics ✨",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            title_style="bold cyan"
        )
        table.add_column("Metric", style="cyan", width=25)
        table.add_column("Value", style="green", width=15)
        table.add_column("Trend", style="yellow", width=20)

        patterns = stats.get('total_patterns', 0)
        projects = stats.get('projects', 0)
        requests = stats.get('total_requests', 0)

        # Calculate trends and insights
        patterns_per_project = patterns / projects if projects > 0 else 0
        success_rate = (patterns / requests * 100) if requests > 0 else 0

        table.add_row(
            "🧠 Total Patterns",
            str(patterns),
            self._get_trend_indicator(patterns)
        )
        table.add_row(
            "📁 Projects",
            str(projects),
            f"~{patterns_per_project:.1f} patterns each"
        )
        table.add_row(
            "💬 Total Requests",
            str(requests),
            f"{success_rate:.1f}% success rate"
        )

        # Add insights section
        if patterns > 0:
            table.add_section()
            table.add_row(
                "🎯 Most Active",
                self._get_most_active_project() or "N/A",
                "Keep it up! 🚀"
            )
            table.add_row(
                "⭐ Best Success Rate",
                f"{success_rate:.1f}%",
                self._get_performance_emoji(success_rate)
            )

        console.print(table)

        # Add motivational message based on stats
        if patterns == 0:
            console.print("\n[yellow]💡 Start using Claude Code to build your knowledge base![/yellow]")
        elif patterns < 10:
            console.print("\n[cyan]🌱 Your knowledge garden is growing![/cyan]")
        elif patterns < 50:
            console.print("\n[green]🌳 Great progress! Your cache is building nicely![/green]")
        else:
            console.print("\n[bold green]🏆 Excellent! You have a rich knowledge base![/bold green]")

    def _get_trend_indicator(self, value: int) -> str:
        """Get trend indicator based on value"""
        if value == 0:
            return "📊 Getting started"
        elif value < 10:
            return "📈 Building up"
        elif value < 50:
            return "⚡ Accelerating"
        else:
            return "🚀 Thriving!"

    def _get_performance_emoji(self, percentage: float) -> str:
        """Get performance emoji based on percentage"""
        if percentage >= 90:
            return "🌟 Outstanding!"
        elif percentage >= 70:
            return "✨ Excellent!"
        elif percentage >= 50:
            return "👍 Good!"
        else:
            return "📈 Improving"

    def _get_most_active_project(self) -> Optional[str]:
        """Get the most active project name"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.kb.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT project_name, COUNT(*) as count
                FROM success_patterns
                GROUP BY project_name
                ORDER BY count DESC
                LIMIT 1
            """)
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None

    def generate_status_table(self):
        """Generate a status table for live display"""
        stats = self.kb.get_statistics()

        table = Table(title="Claude Cache - Live Status", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Patterns", str(stats.get('total_patterns', 0)))
        table.add_row("Projects", str(stats.get('projects', 0)))
        table.add_row("Requests", str(stats.get('total_requests', 0)))
        table.add_row("Status", "[green]● Monitoring[/green]")

        return table

    def query_patterns(self, query: str, project: Optional[str] = None):
        """Query patterns from the knowledge base"""
        if project:
            patterns = self.kb.find_similar_patterns(query, project)
        else:
            all_patterns = []
            for proj in self.get_projects():
                all_patterns.extend(self.kb.find_similar_patterns(query, proj))

            patterns = sorted(all_patterns, key=lambda x: x['similarity'], reverse=True)[:10]

        if not patterns:
            console.print("[yellow]No patterns found[/yellow]")
            return

        for i, pattern in enumerate(patterns, 1):
            console.print(Panel(
                f"[bold]Pattern {i}[/bold]\n"
                f"Request: {pattern['request'][:100]}\n"
                f"Approach: {pattern['approach']}\n"
                f"Similarity: {pattern['similarity']:.1%}\n"
                f"Success: {pattern['success_score']:.1%}",
                expand=False
            ))

    def export_knowledge(self, output_file: str, project: Optional[str] = None):
        """Export knowledge base to file"""
        import json

        data = self.kb.export_patterns(project)

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        console.print(f"[green]✓ Exported to {output_file}[/green]")

    def import_knowledge(self, input_file: str):
        """Import knowledge from file"""
        import json

        with open(input_file, 'r') as f:
            data = json.load(f)

        self.kb.import_patterns(data)

    def rebuild_index(self):
        """Rebuild the entire knowledge base from scratch"""
        console.print("[yellow]Rebuilding knowledge base...[/yellow]")

        import sqlite3
        conn = sqlite3.connect(self.kb.db_path)
        cursor = conn.cursor()

        tables = ['success_patterns', 'project_conventions', 'user_requests', 'tool_usage', 'responses']
        for table in tables:
            cursor.execute(f'DELETE FROM {table}')

        conn.commit()
        conn.close()

        self.process_existing_logs()
        console.print("[green]✓ Knowledge base rebuilt[/green]")

    def _show_banner(self):
        """Display ASCII art banner"""
        banner = """
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║              claude                       ║
    ║                                           ║
    ║    ___    _    ____ _   _ _____           ║
    ║   / __\\  / \\  / ___| | | | ____|          ║
    ║  | |    / _ \\ | |   | |_| |  _|           ║
    ║  | |__ / ___ \\| |___|  _  | |___          ║
    ║   \\___/_/   \\_\\\\____|_| |_|_____|         ║
    ║                                           ║
    ║                v0.1.0                     ║
    ╚═══════════════════════════════════════════╝
        """

        console.print(Text(banner, style="bold cyan"))