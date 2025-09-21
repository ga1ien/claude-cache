"""Monitor Claude Code log files for changes"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from rich.console import Console

console = Console()


class LogFileHandler(FileSystemEventHandler):
    """Handle file system events for Claude Code logs"""

    def __init__(self, processor_callback: Callable[[str], None]):
        self.processor_callback = processor_callback
        self.processed_files = set()
        self.file_positions = {}

    def on_modified(self, event: FileModifiedEvent):
        """Handle file modification events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix == '.jsonl':
            self._process_file_update(str(file_path))

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix == '.jsonl':
            console.print(f"[green]New log file detected: {file_path.name}[/green]")
            self._process_file_update(str(file_path))

    def _process_file_update(self, file_path: str):
        """Process updates to a file"""
        try:
            current_position = self.file_positions.get(file_path, 0)

            with open(file_path, 'r') as f:
                f.seek(current_position)
                new_content = f.read()

                if new_content:
                    self.processor_callback(file_path)
                    self.file_positions[file_path] = f.tell()

        except Exception as e:
            console.print(f"[red]Error processing {file_path}: {e}[/red]")


class LogWatcher:
    """Watch and monitor Claude Code log files"""

    def __init__(self, log_processor):
        self.log_processor = log_processor
        self.observer = None
        self.claude_projects_dir = Path.home() / '.claude' / 'projects'

    def start(self):
        """Start monitoring log files"""
        if not self.claude_projects_dir.exists():
            console.print(f"[yellow]Creating Claude projects directory: {self.claude_projects_dir}[/yellow]")
            self.claude_projects_dir.mkdir(parents=True, exist_ok=True)

        handler = LogFileHandler(self.log_processor.process_file)

        self.observer = Observer()
        self.observer.schedule(
            handler,
            str(self.claude_projects_dir),
            recursive=True
        )

        self.observer.start()
        console.print(f"[green]✓ Monitoring Claude Code logs in {self.claude_projects_dir}[/green]")

        return self.observer

    def stop(self):
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            console.print("[yellow]Log monitoring stopped[/yellow]")

    def process_existing_logs(self):
        """Process all existing log files"""
        if not self.claude_projects_dir.exists():
            console.print(f"[yellow]No Claude projects directory found at {self.claude_projects_dir}[/yellow]")
            return

        log_files = list(self.claude_projects_dir.glob('**/*.jsonl'))

        if not log_files:
            console.print("[yellow]No existing log files found[/yellow]")
            return

        console.print(f"[blue]Processing {len(log_files)} existing log files...[/blue]")

        for log_file in log_files:
            project_name = log_file.parent.name
            console.print(f"  Processing: {project_name}/{log_file.name}")
            self.log_processor.process_file(str(log_file))

        console.print("[green]✓ Finished processing existing logs[/green]")