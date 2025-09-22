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

### Added (New Features)
- **First-Run Documentation Scanner** - Automatically prompts to scan Development folder on first launch
- **Batch Project Import** - Import documentation from all projects at once
- **Intelligent Lesson Organization** - Auto-categorizes lessons by topic (auth, database, API, debugging, etc.)
- **Hierarchical Documentation System** - Lightweight index (CLAUDE.md) + detailed category files
- **Smart Document Length Management** - Keeps CLAUDE.md under 30KB with automatic overflow handling
- **User Content Preservation** - Protected sections in CLAUDE.md that are never overwritten
- **Multi-Part Category Files** - Automatic file splitting when categories exceed 40 lessons
- **Documentation Scanner Module** - New `doc_scanner.py` for extracting lessons from existing docs
- **Lesson Organizer Module** - New `lesson_organizer.py` for intelligent categorization
- **CLI Documentation Commands** - `cache scan-docs` and `cache search-docs` commands
- **Lesson Prioritization System** - Critical, High, Medium, Low priority levels with visual indicators
- **Navigation Links** - Automatic navigation between multi-part lesson files
- **Import Progress Display** - Shows detailed statistics immediately after scanning

### Changed
- **CLAUDE.md Structure** - Now acts as lightweight index (5-10KB) pointing to category files
- **Context Generation** - Uses hierarchical structure with intelligent file references
- **Statistics Display** - Enhanced to show documentation metrics alongside pattern metrics
- **First Run Experience** - Interactive menu for choosing scan source (Development folder, custom, or skip)
- **File Organization** - Lessons now stored in `.claude/lessons/` directory by category

### Improved
- **Scalability** - Can now handle thousands of lessons without performance degradation
- **Organization** - Automatic topic categorization for better discoverability
- **Claude Integration** - CLAUDE.md includes instructions for Claude on where to find specific topics
- **Memory Efficiency** - Reduced main context size while maintaining comprehensive coverage
- **User Experience** - Clear starting point with imported lesson counts shown immediately

### Technical Details
- Maximum 10 lessons per priority level per file
- Maximum 8 categories shown in main index
- Top 5 critical warnings displayed in CLAUDE.md
- Automatic file splitting at 40 lessons per category
- User content preserved between HTML comment markers

### Planned
- Web dashboard for pattern visualization
- Integration with other AI coding tools
- Pattern clustering using ML
- VSCode extension
- Team synchronization features