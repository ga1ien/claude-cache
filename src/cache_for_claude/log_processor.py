"""Process Claude Code log entries and extract meaningful data"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console
from .log_state import LogStateTracker

console = Console()


class LogEntry:
    """Represents a single log entry"""

    def __init__(self, data: Dict[str, Any], source_file: str):
        self.data = data
        self.source_file = source_file
        self.type = data.get('type', 'unknown')
        self.timestamp = data.get('timestamp', datetime.now().isoformat())
        self.content = data.get('content', '')

    @property
    def project_name(self) -> str:
        """Extract project name from source file path"""
        path = Path(self.source_file)
        if path.parent.name == 'projects':
            return 'unknown'
        return path.parent.name

    def is_user_message(self) -> bool:
        return self.type == 'user_message'

    def is_tool_call(self) -> bool:
        return self.type == 'tool_call'

    def is_assistant_message(self) -> bool:
        return self.type == 'assistant_message'


class SessionTracker:
    """Track and organize log entries by session"""

    def __init__(self):
        self.sessions = {}
        self.current_sessions = {}

    def add_entry(self, entry: LogEntry):
        """Add an entry to the appropriate session"""
        project = entry.project_name

        if project not in self.current_sessions:
            self.current_sessions[project] = {
                'entries': [],
                'start_time': entry.timestamp,
                'user_requests': [],
                'tool_calls': [],
                'file_operations': []
            }

        session = self.current_sessions[project]
        session['entries'].append(entry)

        if entry.is_user_message():
            session['user_requests'].append(entry)
        elif entry.is_tool_call():
            session['tool_calls'].append(entry)
            if entry.data.get('tool') in ['Read', 'Edit', 'Write']:
                session['file_operations'].append(entry)

    def get_current_session(self, project: str) -> Optional[Dict]:
        """Get the current session for a project"""
        return self.current_sessions.get(project)

    def finalize_session(self, project: str):
        """Mark a session as complete"""
        if project in self.current_sessions:
            session = self.current_sessions[project]
            session['end_time'] = datetime.now().isoformat()

            if project not in self.sessions:
                self.sessions[project] = []

            self.sessions[project].append(session)
            del self.current_sessions[project]


class LogProcessor:
    """Process Claude Code log files"""

    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
        self.session_tracker = SessionTracker()
        self.state_tracker = LogStateTracker()
        self.processed_lines = {}  # Deprecated, using state_tracker now

    def process_file(self, file_path: str):
        """Process a single JSONL log file with incremental processing"""
        if not Path(file_path).exists():
            return  # Silently skip non-existent files

        # Check if file needs processing
        if not self.state_tracker.should_process_file(file_path):
            return  # File hasn't changed since last processing

        start_position = self.state_tracker.get_position(file_path)
        entries_processed = 0
        current_position = 0

        try:
            with open(file_path, 'r') as f:
                # Skip to last processed position
                if start_position > 0:
                    f.seek(start_position)

                for line in f:

                    line = line.strip()
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                        entry = LogEntry(data, file_path)
                        self.process_entry(entry)
                        entries_processed += 1
                    except json.JSONDecodeError as e:
                        # Silently skip malformed entries to avoid spam
                        pass
                    except Exception as e:
                        # Handle any other parsing errors gracefully
                        if entries_processed == 0:  # Only show error if no entries processed yet
                            console.print(f"[yellow]Warning: Error processing entry: {str(e)[:50]}[/yellow]")

                # Save position after processing
                current_position = f.tell()
                self.state_tracker.update_position(file_path, current_position)

            if entries_processed > 0:
                console.print(f"[green]✓ Processed {entries_processed} new entries from {Path(file_path).name}[/green]")
                # Ensure state is saved after successful processing
                self.state_tracker.save_state()

        except FileNotFoundError:
            console.print(f"[yellow]File not found (may have been deleted): {Path(file_path).name}[/yellow]")
        except PermissionError:
            console.print(f"[yellow]Permission denied: {Path(file_path).name}[/yellow]")
        except Exception as e:
            console.print(f"[red]Unexpected error processing {Path(file_path).name}: {str(e)[:100]}[/red]")
            # Continue processing other files even if one fails

    def process_entry(self, entry: LogEntry):
        """Process a single log entry"""
        self.session_tracker.add_entry(entry)

        if entry.is_user_message():
            self.handle_user_request(entry)
        elif entry.is_tool_call():
            self.handle_tool_call(entry)
        elif entry.is_assistant_message():
            self.handle_assistant_response(entry)

    def handle_user_request(self, entry: LogEntry):
        """Extract and classify user intents"""
        content = entry.content
        request_type = self.classify_request(content)

        request_data = {
            'content': content,
            'type': request_type,
            'timestamp': entry.timestamp,
            'project': entry.project_name,
            'source': entry.source_file
        }

        if self.kb:
            self.kb.store_request(request_data)

    def handle_tool_call(self, entry: LogEntry):
        """Process tool usage patterns"""
        tool_data = {
            'tool': entry.data.get('tool'),
            'args': entry.data.get('args', {}),
            'success': entry.data.get('success', True),
            'timestamp': entry.timestamp,
            'project': entry.project_name
        }

        if self.kb:
            self.kb.store_tool_usage(tool_data)

    def handle_assistant_response(self, entry: LogEntry):
        """Process assistant responses"""
        response_data = {
            'content': entry.content,
            'reasoning': entry.data.get('reasoning', ''),
            'timestamp': entry.timestamp,
            'project': entry.project_name
        }

        if self.kb:
            self.kb.store_response(response_data)

    def classify_request(self, content: str) -> str:
        """Classify the type of user request"""
        content_lower = content.lower()

        if any(word in content_lower for word in ['fix', 'bug', 'error', 'broken', 'issue']):
            return 'debugging'
        elif any(word in content_lower for word in ['add', 'create', 'implement', 'build', 'new feature']):
            return 'feature_development'
        elif any(word in content_lower for word in ['test', 'spec', 'validate', 'check']):
            return 'testing'
        elif any(word in content_lower for word in ['refactor', 'clean', 'optimize', 'improve']):
            return 'refactoring'
        elif any(word in content_lower for word in ['explain', 'how', 'what', 'why', 'understand']):
            return 'explanation'
        elif any(word in content_lower for word in ['document', 'readme', 'comment']):
            return 'documentation'
        else:
            return 'other'

    def get_session_summary(self, project: str) -> Optional[Dict]:
        """Get a summary of the current session"""
        session = self.session_tracker.get_current_session(project)

        if not session:
            return None

        return {
            'project': project,
            'start_time': session['start_time'],
            'total_entries': len(session['entries']),
            'user_requests': len(session['user_requests']),
            'tool_calls': len(session['tool_calls']),
            'files_touched': len(session['file_operations'])
        }