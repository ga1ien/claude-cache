"""Knowledge base storage and retrieval system"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rich.console import Console
from .vector_search import VectorSearchEngine

console = Console()


class KnowledgeBase:
    """Store and retrieve successful patterns and project conventions"""

    def __init__(self, db_path: str = None, silent: bool = False):
        self.silent = silent
        if db_path is None:
            db_dir = Path.home() / '.claude' / 'knowledge'
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / 'cache.db'

        self.db_path = str(db_path)
        self.setup_database()

        # Initialize vector search engine (with automatic fallback)
        self.vector_search = VectorSearchEngine(db_path, silent=self.silent)

        # Keep legacy TF-IDF for backward compatibility
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.use_vector_search = True  # Flag to enable/disable new search

    def setup_database(self):
        """Create database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS success_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                request_type TEXT,
                user_request TEXT,
                approach TEXT,
                files_involved TEXT,
                solution_steps TEXT,
                key_operations TEXT,
                timestamp DATETIME,
                success_score REAL,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_conventions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                convention_type TEXT,
                pattern TEXT,
                description TEXT,
                frequency INTEGER DEFAULT 1,
                last_seen DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                content TEXT,
                request_type TEXT,
                timestamp DATETIME,
                source_file TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                tool TEXT,
                args TEXT,
                success BOOLEAN,
                timestamp DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                content TEXT,
                reasoning TEXT,
                timestamp DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                doc_type TEXT,
                content TEXT,
                extracted_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(project_name, file_path)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_patterns_project
            ON success_patterns(project_name)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conventions_project
            ON project_conventions(project_name)
        ''')

        conn.commit()
        conn.close()

        if not self.silent:
            console.print(f"[green]✓ Knowledge base initialized at {self.db_path}[/green]")

    def store_success_pattern(self, pattern: Dict, project_name: str, success_score: float = 1.0):
        """Store a successful pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO success_patterns
            (project_name, request_type, user_request, approach, files_involved,
             solution_steps, key_operations, timestamp, success_score, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_name,
            pattern.get('request_type', 'unknown'),
            pattern.get('user_request', ''),
            pattern.get('approach', ''),
            json.dumps(pattern.get('files_involved', [])),
            json.dumps(pattern.get('solution_steps', [])),
            json.dumps(pattern.get('key_operations', [])),
            pattern.get('timestamp', datetime.now().isoformat()),
            success_score,
            json.dumps(pattern.get('tags', []))
        ))

        pattern_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Add to vector search index if available
        if self.use_vector_search and self.vector_search:
            try:
                # Create searchable text from pattern
                search_text = pattern.get('user_request', '')
                if pattern.get('approach'):
                    search_text += f" {pattern['approach']}"

                # Store metadata for later retrieval
                metadata = {
                    'type': 'pattern',  # Important for unified search
                    'project': project_name,
                    'success_score': success_score,
                    'request_type': pattern.get('request_type', 'unknown'),
                    'timestamp': pattern.get('timestamp', datetime.now().isoformat())
                }

                # Add to vector index
                self.vector_search.add_pattern(
                    text=search_text,
                    pattern_id=f"pattern_{pattern_id}",
                    metadata=metadata
                )

                console.print(f"[green]✓ Stored and indexed pattern for {project_name}[/green]")
            except Exception as e:
                console.print(f"[yellow]Pattern stored but indexing failed: {str(e)}[/yellow]")
        else:
            console.print(f"[green]✓ Stored success pattern for {project_name}[/green]")

    def store_request(self, request_data: Dict):
        """Store a user request"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user_requests
            (project_name, content, request_type, timestamp, source_file)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            request_data.get('project', 'unknown'),
            request_data.get('content', ''),
            request_data.get('type', 'other'),
            request_data.get('timestamp', datetime.now().isoformat()),
            request_data.get('source', '')
        ))

        conn.commit()
        conn.close()

    def store_tool_usage(self, tool_data: Dict):
        """Store tool usage data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tool_usage
            (project_name, tool, args, success, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            tool_data.get('project', 'unknown'),
            tool_data.get('tool', ''),
            json.dumps(tool_data.get('args', {})),
            tool_data.get('success', True),
            tool_data.get('timestamp', datetime.now().isoformat())
        ))

        conn.commit()
        conn.close()

    def store_response(self, response_data: Dict):
        """Store assistant response"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO responses
            (project_name, content, reasoning, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (
            response_data.get('project', 'unknown'),
            response_data.get('content', ''),
            response_data.get('reasoning', ''),
            response_data.get('timestamp', datetime.now().isoformat())
        ))

        conn.commit()
        conn.close()

    def find_similar_patterns(self, current_request: str, project_name: str, threshold: float = 0.3) -> List[Dict]:
        """Find similar successful patterns using hybrid vector search"""
        # Try vector search first if available
        if self.use_vector_search and self.vector_search:
            try:
                # Use the vector search engine for better results
                vector_results = self.vector_search.search(
                    query=current_request,
                    limit=10,
                    project=project_name
                )

                # Convert vector search results to expected format
                similar_patterns = []
                for result in vector_results:
                    if result['similarity'] > threshold:
                        # Fetch full pattern data from database
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()

                        pattern_id = result.get('pattern_id', '')
                        # Try to extract numeric ID from pattern_id
                        try:
                            numeric_id = int(pattern_id.split('_')[-1]) if '_' in pattern_id else int(pattern_id)
                        except:
                            numeric_id = pattern_id

                        cursor.execute('''
                            SELECT id, user_request, approach, solution_steps, success_score,
                                   files_involved, key_operations
                            FROM success_patterns
                            WHERE id = ? OR user_request = ?
                        ''', (numeric_id, result.get('text', '')))

                        pattern_data = cursor.fetchone()
                        conn.close()

                        if pattern_data:
                            similar_patterns.append({
                                'id': pattern_data[0],
                                'request': pattern_data[1],
                                'approach': pattern_data[2],
                                'solution_steps': json.loads(pattern_data[3]) if pattern_data[3] else [],
                                'files_involved': json.loads(pattern_data[5]) if pattern_data[5] else [],
                                'key_operations': json.loads(pattern_data[6]) if pattern_data[6] else [],
                                'success_score': pattern_data[4],
                                'similarity': result['similarity'],
                                'search_mode': result.get('search_mode', 'unknown')
                            })

                if similar_patterns:
                    return sorted(similar_patterns, key=lambda x: x['similarity'], reverse=True)[:5]
            except Exception as e:
                console.print(f"[yellow]Vector search failed, falling back to TF-IDF: {str(e)}[/yellow]")

        # Fallback to legacy TF-IDF search
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, user_request, approach, solution_steps, success_score, files_involved, key_operations
            FROM success_patterns
            WHERE project_name = ?
            ORDER BY success_score DESC
            LIMIT 100
        ''', (project_name,))

        patterns = cursor.fetchall()
        conn.close()

        if not patterns:
            return []

        requests = [current_request] + [p[1] for p in patterns]

        try:
            tfidf_matrix = self.vectorizer.fit_transform(requests)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        except:
            similarities = [0] * len(patterns)

        similar_patterns = []
        for i, (pattern_id, request, approach, steps, score, files, operations) in enumerate(patterns):
            if similarities[i] > threshold:
                similar_patterns.append({
                    'id': pattern_id,
                    'request': request,
                    'approach': approach,
                    'solution_steps': json.loads(steps) if steps else [],
                    'files_involved': json.loads(files) if files else [],
                    'key_operations': json.loads(operations) if operations else [],
                    'success_score': score,
                    'similarity': similarities[i],
                    'search_mode': 'tfidf'
                })

        return sorted(similar_patterns, key=lambda x: x['similarity'], reverse=True)[:5]

    def get_project_conventions(self, project_name: str) -> List[Dict]:
        """Get conventions for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT convention_type, pattern, description, frequency
            FROM project_conventions
            WHERE project_name = ?
            ORDER BY frequency DESC
        ''', (project_name,))

        conventions = []
        for row in cursor.fetchall():
            conventions.append({
                'type': row[0],
                'pattern': row[1],
                'description': row[2],
                'frequency': row[3]
            })

        conn.close()
        return conventions

    def store_convention(self, project_name: str, convention_type: str, pattern: str, description: str = ''):
        """Store or update a project convention"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, frequency FROM project_conventions
            WHERE project_name = ? AND convention_type = ? AND pattern = ?
        ''', (project_name, convention_type, pattern))

        existing = cursor.fetchone()

        if existing:
            cursor.execute('''
                UPDATE project_conventions
                SET frequency = frequency + 1, last_seen = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (existing[0],))
        else:
            cursor.execute('''
                INSERT INTO project_conventions
                (project_name, convention_type, pattern, description, last_seen)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (project_name, convention_type, pattern, description))

        conn.commit()
        conn.close()

    def get_statistics(self, project_name: Optional[str] = None) -> Dict:
        """Get statistics about the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        if project_name:
            cursor.execute('SELECT COUNT(*) FROM success_patterns WHERE project_name = ?', (project_name,))
            stats['patterns'] = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM project_conventions WHERE project_name = ?', (project_name,))
            stats['conventions'] = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM user_requests WHERE project_name = ?', (project_name,))
            stats['requests'] = cursor.fetchone()[0]
        else:
            cursor.execute('SELECT COUNT(*) FROM success_patterns')
            stats['total_patterns'] = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(DISTINCT project_name) FROM success_patterns')
            stats['projects'] = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM user_requests')
            stats['total_requests'] = cursor.fetchone()[0]

        conn.close()
        return stats

    def export_patterns(self, project_name: Optional[str] = None) -> Dict:
        """Export patterns for sharing or backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if project_name:
            cursor.execute('''
                SELECT * FROM success_patterns
                WHERE project_name = ?
            ''', (project_name,))
        else:
            cursor.execute('SELECT * FROM success_patterns')

        columns = [description[0] for description in cursor.description]
        patterns = []

        for row in cursor.fetchall():
            pattern_dict = dict(zip(columns, row))

            for field in ['files_involved', 'solution_steps', 'key_operations', 'tags']:
                if field in pattern_dict and pattern_dict[field]:
                    try:
                        pattern_dict[field] = json.loads(pattern_dict[field])
                    except:
                        pass

            patterns.append(pattern_dict)

        conn.close()

        return {
            'version': '1.0',
            'exported_at': datetime.now().isoformat(),
            'project': project_name or 'all',
            'patterns': patterns
        }

    def import_patterns(self, data: Dict):
        """Import patterns from export"""
        patterns = data.get('patterns', [])

        for pattern in patterns:
            for field in ['files_involved', 'solution_steps', 'key_operations', 'tags']:
                if field in pattern and isinstance(pattern[field], list):
                    pattern[field] = json.dumps(pattern[field])

            self.store_success_pattern(pattern, pattern.get('project_name', 'imported'))

        console.print(f"[green]✓ Imported {len(patterns)} patterns[/green]")

    def store_documentation(self, project_name: str, file_path: str, doc_type: str,
                           content: str, extracted_at: str):
        """Store extracted documentation in the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO documentation
                (project_name, file_path, doc_type, content, extracted_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (project_name, file_path, doc_type, content, extracted_at))

            conn.commit()
        finally:
            conn.close()

        # Automatically index documentation into vector search if available
        if self.use_vector_search and self.vector_search:
            try:
                import json
                doc_data = json.loads(content)

                # Create searchable text from lessons, warnings, etc.
                search_text_parts = []

                if 'lessons' in doc_data:
                    search_text_parts.extend(doc_data['lessons'])

                if 'warnings' in doc_data:
                    search_text_parts.extend(doc_data['warnings'])

                if 'best_practices' in doc_data:
                    search_text_parts.extend(doc_data['best_practices'])

                if 'architecture' in doc_data:
                    search_text_parts.append(doc_data['architecture'])

                # Combine all text
                search_text = " ".join(search_text_parts)

                if search_text.strip():
                    # Add to vector search index
                    pattern_id = f"doc_{project_name}_{file_path}".replace("/", "_").replace(" ", "_")[:100]

                    self.vector_search.add_pattern(
                        text=search_text,
                        pattern_id=pattern_id,
                        metadata={
                            'type': 'documentation',
                            'project': project_name,
                            'file_path': file_path,
                            'doc_type': doc_type
                        }
                    )
            except Exception as e:
                # Don't fail if indexing fails, just log it
                console.print(f"[dim]Could not index documentation: {str(e)}[/dim]")

    def search_documentation(self, query: str, project_name: Optional[str] = None,
                           limit: int = 10) -> List[Dict[str, Any]]:
        """Search through stored documentation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            if project_name:
                cursor.execute('''
                    SELECT project_name, file_path, doc_type, content, extracted_at
                    FROM documentation
                    WHERE project_name = ?
                    ORDER BY extracted_at DESC
                    LIMIT ?
                ''', (project_name, limit))
            else:
                cursor.execute('''
                    SELECT project_name, file_path, doc_type, content, extracted_at
                    FROM documentation
                    ORDER BY extracted_at DESC
                    LIMIT ?
                ''', (limit,))

            results = []
            for row in cursor.fetchall():
                results.append({
                    'project_name': row[0],
                    'file_path': row[1],
                    'doc_type': row[2],
                    'content': row[3],
                    'extracted_at': row[4]
                })

            # Filter by query relevance if provided
            if query and results:
                import json
                scored_results = []
                for result in results:
                    doc_data = json.loads(result['content'])
                    # Simple relevance scoring based on query terms
                    score = 0
                    query_terms = query.lower().split()
                    content_str = json.dumps(doc_data).lower()

                    for term in query_terms:
                        score += content_str.count(term)

                    if score > 0:
                        result['relevance_score'] = score
                        scored_results.append(result)

                # Sort by relevance
                scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
                return scored_results[:limit]

            return results

        finally:
            conn.close()

    def unified_search(self, query: str, project_name: Optional[str] = None,
                       limit: int = 10) -> List[Dict[str, Any]]:
        """Unified search across all content: patterns, documentation, everything"""
        if self.use_vector_search and self.vector_search:
            # Use vector search for everything
            results = self.vector_search.search(
                query=query,
                limit=limit,
                project=project_name
            )

            # Enrich results with additional metadata
            enriched_results = []
            for result in results:
                metadata = result.get('metadata', {})
                content_type = metadata.get('type', 'unknown')

                enriched_result = {
                    'type': content_type,
                    'content': result.get('text', ''),
                    'similarity': result.get('similarity', 0),
                    'project': metadata.get('project', ''),
                    'search_mode': result.get('search_mode', 'unknown')
                }

                # Add type-specific fields
                if content_type == 'documentation':
                    enriched_result['file_path'] = metadata.get('file_path', '')
                    enriched_result['doc_type'] = metadata.get('doc_type', '')
                elif content_type == 'pattern':
                    enriched_result['pattern_id'] = result.get('pattern_id', '')

                enriched_results.append(enriched_result)

            return enriched_results
        else:
            # Fallback to pattern search only (legacy)
            patterns = self.find_similar_patterns(query, project_name or 'unknown', 0.1)
            return [{
                'type': 'pattern',
                'content': p.get('request', ''),
                'similarity': p.get('similarity', 0),
                'project': project_name or '',
                'search_mode': 'tfidf'
            } for p in patterns[:limit]]

    def get_documentation_for_context(self, project_name: str) -> List[Dict[str, Any]]:
        """Get relevant documentation for context injection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT file_path, doc_type, content
                FROM documentation
                WHERE project_name = ?
                AND doc_type IN ('lessons', 'postmortem', 'architecture', 'guide')
                ORDER BY
                    CASE doc_type
                        WHEN 'lessons' THEN 1
                        WHEN 'postmortem' THEN 2
                        WHEN 'architecture' THEN 3
                        WHEN 'guide' THEN 4
                        ELSE 5
                    END
                LIMIT 10
            ''', (project_name,))

            docs = []
            for row in cursor.fetchall():
                docs.append({
                    'file_path': row[0],
                    'doc_type': row[1],
                    'content': row[2]
                })

            return docs

        finally:
            conn.close()

    def get_project_patterns(self, project_name: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent patterns for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            if project_name:
                cursor.execute('''
                    SELECT project_name, request_type, user_request, approach,
                           files_involved, solution_steps, timestamp
                    FROM success_patterns
                    WHERE project_name = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (project_name, limit))
            else:
                cursor.execute('''
                    SELECT project_name, request_type, user_request, approach,
                           files_involved, solution_steps, timestamp
                    FROM success_patterns
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))

            patterns = []
            for row in cursor.fetchall():
                pattern = {
                    'project_name': row[0],
                    'request_type': row[1],
                    'user_request': row[2],
                    'approach': row[3],
                    'files_involved': json.loads(row[4]) if row[4] else [],
                    'solution_steps': json.loads(row[5]) if row[5] else [],
                    'timestamp': row[6]
                }
                patterns.append(pattern)

            return patterns

        finally:
            conn.close()