"""Detect successful patterns in Claude Code sessions"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from .intent_detector import IntentDetector
from .execution_monitor import ExecutionMonitor

console = Console()


class SuccessDetector:
    """Analyze sessions to identify successful patterns"""

    def __init__(self):
        self.success_indicators = {
            'test_keywords': ['passed', 'success', 'ok', '✓', 'green', 'passing', 'successful'],
            'failure_keywords': ['failed', 'error', 'exception', 'traceback', 'red', 'failing'],
            'completion_keywords': ['done', 'completed', 'finished', 'works', 'working', 'fixed', 'resolved'],
            'user_satisfaction': ['thanks', 'perfect', 'great', 'awesome', 'exactly', 'good',
                                 'nice', 'excellent', 'that worked', "that's it", 'yes',
                                 'correct', 'right', 'thank you', 'ty', 'appreciated']
        }

        # Initialize semantic intent detector
        self.intent_detector = IntentDetector()

        # Initialize execution monitor
        self.execution_monitor = ExecutionMonitor()

    def analyze_session_success(self, session_entries: List[Dict]) -> Dict:
        """Determine if a session was successful and extract patterns"""
        if not session_entries:
            return {'success': False, 'score': 0, 'pattern': None}

        # Analyze execution signals
        execution_success = self.analyze_execution_signals(session_entries)

        indicators = {
            'tests_passed': self.check_test_success(session_entries),
            'no_errors': self.check_for_errors(session_entries),
            'files_modified': self.count_successful_edits(session_entries),
            'user_satisfied': self.detect_user_satisfaction(session_entries),
            'task_completed': self.check_task_completion(session_entries),
            'execution_success': execution_success
        }

        score = self.calculate_success_score(indicators)

        if score > 0.5:  # Lowered threshold to capture more patterns
            pattern = self.extract_success_pattern(session_entries)
            return {
                'success': True,
                'score': score,
                'pattern': pattern,
                'indicators': indicators
            }

        return {
            'success': False,
            'score': score,
            'pattern': None,
            'indicators': indicators
        }

    def check_test_success(self, entries: List[Dict]) -> bool:
        """Check if tests passed in the session using execution monitoring"""
        # Check execution signals from bash commands
        for entry in entries:
            if entry.get('type') == 'tool_call' and entry.get('tool') == 'Bash':
                command = entry.get('args', {}).get('command', '')
                output = entry.get('output', '')

                if output:
                    signals = self.execution_monitor.analyze_output(output, command)
                    for signal in signals:
                        if signal.signal_type == 'test_pass' and signal.confidence > 0.7:
                            return True

        # Fallback to keyword detection
        for entry in entries:
            content = str(entry.get('content', '')).lower()

            if any(keyword in content for keyword in self.success_indicators['test_keywords']):
                if 'test' in content or 'spec' in content:
                    return True

        return False

    def check_for_errors(self, entries: List[Dict]) -> bool:
        """Check if there were no errors in the session"""
        error_count = 0
        success_count = 0

        for entry in entries:
            content = str(entry.get('content', '')).lower()

            for keyword in self.success_indicators['failure_keywords']:
                if keyword in content:
                    error_count += 1

            for keyword in self.success_indicators['test_keywords']:
                if keyword in content:
                    success_count += 1

        return success_count > error_count

    def count_successful_edits(self, entries: List[Dict]) -> int:
        """Count number of successful file modifications"""
        successful_edits = 0

        for entry in entries:
            if entry.get('type') == 'tool_call':
                tool = entry.get('tool', '')
                success = entry.get('success', True)

                if tool in ['Edit', 'Write', 'MultiEdit'] and success:
                    successful_edits += 1

        return successful_edits

    def detect_user_satisfaction(self, entries: List[Dict]) -> bool:
        """Detect if the user was satisfied with the result using semantic analysis"""
        # Analyze the conversation flow for semantic intent
        conversation = []
        for entry in entries:
            if entry.get('type') in ['user_message', 'assistant_message']:
                conversation.append({
                    'role': 'user' if entry.get('type') == 'user_message' else 'assistant',
                    'content': entry.get('content', '')
                })

        # Use semantic analysis
        if conversation:
            analysis = self.intent_detector.analyze_conversation_flow(conversation)
            return analysis.get('overall_intent') == 'positive' and analysis.get('confidence', 0) > 0.6

        # Fallback to keyword matching
        for entry in reversed(entries):
            if entry.get('type') == 'user_message':
                content = str(entry.get('content', '')).lower()

                for keyword in self.success_indicators['user_satisfaction']:
                    if keyword in content:
                        return True

        return False

    def check_task_completion(self, entries: List[Dict]) -> bool:
        """Check if the task was marked as completed"""
        for entry in entries:
            content = str(entry.get('content', '')).lower()

            for keyword in self.success_indicators['completion_keywords']:
                if keyword in content:
                    return True

        return False

    def calculate_success_score(self, indicators: Dict[str, Any]) -> float:
        """Calculate overall success score"""
        weights = {
            'tests_passed': 0.25,
            'no_errors': 0.2,
            'files_modified': 0.1,
            'user_satisfied': 0.2,
            'task_completed': 0.1,
            'execution_success': 0.15
        }

        score = 0
        for key, value in indicators.items():
            if key in weights:
                if isinstance(value, bool):
                    score += weights[key] if value else 0
                elif isinstance(value, int):
                    score += weights[key] * min(value / 5, 1)
                elif isinstance(value, float):
                    score += weights[key] * value

        return score

    def extract_success_pattern(self, entries: List[Dict]) -> Dict:
        """Extract the successful pattern from a session"""
        pattern = {
            'user_request': self.get_initial_request(entries),
            'approach': self.extract_approach(entries),
            'files_involved': self.get_files_touched(entries),
            'solution_steps': self.extract_solution_steps(entries),
            'key_operations': self.extract_key_operations(entries),
            'timestamp': datetime.now().isoformat()
        }

        return pattern

    def get_initial_request(self, entries: List[Dict]) -> str:
        """Get the initial user request from the session"""
        for entry in entries:
            if entry.get('type') == 'user_message':
                return entry.get('content', '')

        return ''

    def extract_approach(self, entries: List[Dict]) -> str:
        """Extract the general approach taken"""
        tool_sequence = []

        for entry in entries:
            if entry.get('type') == 'tool_call':
                tool = entry.get('tool', '')
                if tool:
                    tool_sequence.append(tool)

        approach_patterns = {
            'exploration_first': ['Grep', 'Read', 'Read'],
            'direct_edit': ['Edit', 'Edit'],
            'test_driven': ['Read', 'Edit', 'Bash'],
            'research_based': ['WebSearch', 'Read', 'Edit']
        }

        for approach, pattern in approach_patterns.items():
            if self._matches_pattern(tool_sequence, pattern):
                return approach

        return 'mixed_approach'

    def _matches_pattern(self, sequence: List[str], pattern: List[str]) -> bool:
        """Check if a tool sequence matches a pattern"""
        if len(sequence) < len(pattern):
            return False

        for i in range(len(sequence) - len(pattern) + 1):
            if sequence[i:i + len(pattern)] == pattern:
                return True

        return False

    def get_files_touched(self, entries: List[Dict]) -> List[str]:
        """Get list of files that were touched in the session"""
        files = set()

        for entry in entries:
            if entry.get('type') == 'tool_call':
                args = entry.get('args', {})

                if 'file_path' in args:
                    files.add(args['file_path'])
                elif 'path' in args:
                    files.add(args['path'])

        return list(files)

    def extract_solution_steps(self, entries: List[Dict]) -> List[Dict]:
        """Extract the key solution steps"""
        steps = []
        step_number = 1

        for entry in entries:
            if entry.get('type') == 'assistant_message':
                content = entry.get('content', '')

                if self._is_significant_step(content):
                    steps.append({
                        'number': step_number,
                        'action': self._summarize_step(content),
                        'timestamp': entry.get('timestamp')
                    })
                    step_number += 1

        return steps

    def _is_significant_step(self, content: str) -> bool:
        """Determine if a message represents a significant step"""
        significant_indicators = [
            'implementing', 'creating', 'adding', 'fixing',
            'updating', 'modifying', 'refactoring', 'testing'
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in significant_indicators)

    def _summarize_step(self, content: str) -> str:
        """Create a brief summary of a step"""
        lines = content.split('\n')
        first_line = lines[0] if lines else content

        if len(first_line) > 100:
            return first_line[:97] + '...'

        return first_line

    def extract_key_operations(self, entries: List[Dict]) -> List[Dict]:
        """Extract key operations performed"""
        operations = []

        for entry in entries:
            if entry.get('type') == 'tool_call':
                tool = entry.get('tool', '')
                args = entry.get('args', {})

                operation = {
                    'tool': tool,
                    'success': entry.get('success', True)
                }

                if tool in ['Edit', 'Write']:
                    operation['file'] = args.get('file_path', '')
                elif tool == 'Bash':
                    operation['command'] = args.get('command', '')[:50]

                operations.append(operation)

        return operations

    def analyze_execution_signals(self, entries: List[Dict]) -> float:
        """Analyze execution signals from command outputs"""
        all_signals = []

        for entry in entries:
            if entry.get('type') == 'tool_call' and entry.get('tool') == 'Bash':
                command = entry.get('args', {}).get('command', '')
                output = entry.get('output', '')

                if output:
                    signals = self.execution_monitor.analyze_output(output, command)
                    all_signals.extend(signals)

        if not all_signals:
            return 0.0

        # Calculate overall success from signals
        success, confidence = self.execution_monitor.calculate_overall_success(all_signals)
        return confidence if success else 0.0