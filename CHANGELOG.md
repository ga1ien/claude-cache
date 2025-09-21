# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-21

### Added
- Initial release of Claude Cache
- Real-time log monitoring for Claude Code sessions
- Success pattern detection using multiple indicators
- SQLite-based knowledge base storage
- Context generation for similar requests
- Slash command generation for Claude Code
- Project convention tracking
- CLI interface with multiple commands
- Export/import functionality for team sharing
- Rich terminal output with progress indicators
- TF-IDF based similarity matching for patterns

### Features
- `start` - Monitor and process Claude Code logs in real-time
- `process` - Process existing logs without monitoring
- `query` - Search patterns from knowledge base
- `generate` - Create slash commands for projects
- `stats` - View knowledge base statistics
- `export/import` - Share patterns with team
- `context` - Generate context for specific requests
- `rebuild` - Rebuild knowledge base from scratch

### Technical Details
- Python 3.8+ support
- Watchdog for file system monitoring
- scikit-learn for pattern matching
- Rich for terminal UI
- Click for CLI interface
- SQLite for local storage

## [Unreleased]

### Planned
- Web dashboard for pattern visualization
- Integration with other AI coding tools
- Pattern clustering and categorization
- VSCode extension