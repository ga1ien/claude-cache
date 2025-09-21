"""Enhanced success detection with tech stack awareness"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from .config import DetectionConfig
from .success_detector import SuccessDetector

class EnhancedSuccessDetector(SuccessDetector):
    """Stack-aware success pattern detection"""

    def __init__(self):
        super().__init__()
        self.config = DetectionConfig()

        # Add stack-specific success patterns
        self.stack_success_patterns = {
            'frontend': {
                'component_working': r'component\s+(renders?|works?|displays?)',
                'styling_fixed': r'(css|style|styling|layout)\s+(fixed|working|correct)',
                'state_managed': r'state\s+(management|updated|synchronized)',
                'responsive': r'responsive|mobile.*(working|fixed)',
                'performance': r'(render|load|performance).*(optimized|improved|faster)'
            },
            'backend': {
                'api_working': r'(api|endpoint|route).*(working|successful|returns)',
                'auth_implemented': r'(auth|authentication|authorization).*(working|implemented)',
                'validation': r'validation.*(added|working|successful)',
                'error_handled': r'error.*(handled|caught|fixed)',
                'tested': r'(unit|integration|api).*(test|tests).*(pass|passing)'
            },
            'database': {
                'query_optimized': r'query.*(optimized|faster|improved)',
                'migration_successful': r'migration.*(successful|completed|applied)',
                'index_added': r'index.*(added|created|optimized)',
                'schema_updated': r'schema.*(updated|modified|migrated)',
                'performance': r'(database|query|db).*(faster|optimized)'
            }
        }

    def analyze_session_success(self, session_entries: List[Dict]) -> Dict:
        """Enhanced analysis with stack awareness"""
        # Detect tech stack from session
        tech_stacks = self._detect_session_stacks(session_entries)

        # Get base analysis
        base_result = super().analyze_session_success(session_entries)

        # Enhance with stack-specific analysis
        if tech_stacks:
            stack_scores = self._analyze_stack_specific_success(session_entries, tech_stacks)

            # Adjust overall score based on stack-specific success
            enhanced_score = self._calculate_enhanced_score(
                base_result['score'],
                stack_scores
            )

            base_result['enhanced_score'] = enhanced_score
            base_result['tech_stacks'] = tech_stacks
            base_result['stack_scores'] = stack_scores

            # Use enhanced score for success determination
            # Ensure enhanced_score is a float
            if isinstance(enhanced_score, (int, float)) and enhanced_score > 0.7:
                base_result['success'] = True
                if not base_result.get('pattern'):
                    base_result['pattern'] = self.extract_success_pattern(session_entries)

                # Add stack-specific metadata
                base_result['pattern']['tech_stacks'] = tech_stacks
                base_result['pattern']['stack_specific_wins'] = self._extract_stack_wins(
                    session_entries, tech_stacks
                )

        return base_result

    def _detect_session_stacks(self, entries: List[Dict]) -> List[str]:
        """Detect which tech stacks are involved in the session"""
        stacks = set()

        for entry in entries:
            # Check file operations
            if entry.get('type') == 'tool_call':
                args = entry.get('args', {})
                file_path = args.get('file_path', '') or args.get('path', '')

                if file_path:
                    detected = self.config.get_stack_for_file(file_path)
                    stacks.update(detected)

            # Check content for keywords
            content = str(entry.get('content', '')).lower()
            for stack_name, stack_config in self.config.stack_patterns.items():
                if any(keyword in content for keyword in stack_config['keywords']):
                    stacks.add(stack_name)

        return list(stacks)

    def _analyze_stack_specific_success(self, entries: List[Dict], stacks: List[str]) -> Dict[str, float]:
        """Analyze success for each detected stack"""
        stack_scores = {}

        for stack in stacks:
            if stack in self.stack_success_patterns:
                patterns = self.stack_success_patterns[stack]
                score = self._calculate_stack_score(entries, patterns, stack)
                stack_scores[stack] = score

        return stack_scores

    def _calculate_stack_score(self, entries: List[Dict], patterns: Dict[str, str], stack: str) -> float:
        """Calculate success score for a specific stack"""
        total_matches = 0
        pattern_weights = {
            'frontend': {
                'component_working': 0.3,
                'styling_fixed': 0.2,
                'state_managed': 0.2,
                'responsive': 0.15,
                'performance': 0.15
            },
            'backend': {
                'api_working': 0.3,
                'auth_implemented': 0.25,
                'validation': 0.15,
                'error_handled': 0.15,
                'tested': 0.15
            },
            'database': {
                'query_optimized': 0.3,
                'migration_successful': 0.25,
                'index_added': 0.2,
                'schema_updated': 0.15,
                'performance': 0.1
            }
        }

        weights = pattern_weights.get(stack, {})
        score = 0

        for entry in entries:
            content = str(entry.get('content', ''))

            for pattern_name, regex in patterns.items():
                if re.search(regex, content, re.IGNORECASE):
                    weight = weights.get(pattern_name, 0.2)
                    score += weight

        # Check for stack-specific error patterns
        error_penalty = self._check_stack_errors(entries, stack)
        score = max(0, score - error_penalty)

        return min(score, 1.0)  # Cap at 1.0

    def _check_stack_errors(self, entries: List[Dict], stack: str) -> float:
        """Check for stack-specific errors"""
        error_patterns = {
            'frontend': [
                r'console\.(error|warn)',
                r'cannot read property',
                r'undefined is not',
                r'hydration failed',
                r'react error'
            ],
            'backend': [
                r'500\s+error',
                r'internal server error',
                r'unauthorized',
                r'forbidden',
                r'connection refused'
            ],
            'database': [
                r'syntax error',
                r'connection failed',
                r'deadlock',
                r'constraint violation',
                r'timeout'
            ]
        }

        patterns = error_patterns.get(stack, [])
        error_count = 0

        for entry in entries:
            content = str(entry.get('content', '')).lower()
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    error_count += 1

        # Each error reduces score by 0.1
        return min(error_count * 0.1, 0.5)  # Cap penalty at 0.5

    def _calculate_enhanced_score(self, base_score: float, stack_scores: Dict[str, float]) -> float:
        """Combine base and stack-specific scores"""
        if not stack_scores:
            return float(base_score) if base_score else 0.0

        try:
            # Weight: 60% base score, 40% stack-specific
            # Ensure all values are floats
            base = float(base_score) if base_score else 0.0
            stack_values = [float(v) for v in stack_scores.values() if isinstance(v, (int, float))]
            if not stack_values:
                return base
            stack_avg = sum(stack_values) / len(stack_values)
            return (base * 0.6) + (stack_avg * 0.4)
        except (TypeError, ValueError):
            # Fallback to base score if calculation fails
            return float(base_score) if base_score else 0.0

    def _extract_stack_wins(self, entries: List[Dict], stacks: List[str]) -> Dict[str, List[str]]:
        """Extract specific wins for each stack"""
        wins = {stack: [] for stack in stacks}

        for entry in entries:
            if entry.get('type') == 'assistant_message':
                content = entry.get('content', '')

                for stack in stacks:
                    if stack == 'frontend':
                        if 'component' in content.lower() and 'working' in content.lower():
                            wins[stack].append('Component implementation successful')
                        if 'styled' in content.lower() or 'css' in content.lower():
                            wins[stack].append('Styling completed')

                    elif stack == 'backend':
                        if 'endpoint' in content.lower() or 'api' in content.lower():
                            wins[stack].append('API endpoint implemented')
                        if 'auth' in content.lower():
                            wins[stack].append('Authentication handled')

                    elif stack == 'database':
                        if 'query' in content.lower() and 'optimized' in content.lower():
                            wins[stack].append('Query optimization successful')
                        if 'migration' in content.lower():
                            wins[stack].append('Database migration completed')

        return wins

    def get_stack_specific_patterns(self, project_name: str, stack: str) -> List[Dict]:
        """Get patterns specific to a tech stack"""
        # This would query the knowledge base for stack-specific patterns
        # Implementation would be in the KnowledgeBase class
        pass