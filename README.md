# Claude Cache

[![PyPI version](https://badge.fury.io/py/claude-cache.svg)](https://pypi.org/project/claude-cache/)
[![Python Support](https://img.shields.io/pypi/pyversions/claude-cache)](https://pypi.org/project/claude-cache/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Memory for your AI coding assistant**

Claude Cache automatically processes your Claude Code logs, identifies successful patterns, and builds memory that reduces AI hallucinations and improves coding effectiveness.

*Note: This is an independent tool for enhancing Claude Code, not an official Anthropic product.*

## 🚨 Important: How Claude Cache Learns

**Claude Cache learns from your feedback!** When Claude helps you successfully, you must tell it:

- Say **"Perfect!"**, **"That worked!"**, or **"Thanks!"** when things work
- Without feedback, Cache won't know what succeeded and won't save patterns
- More feedback = Better memory = Smarter Claude

Example:
```
You: "Add user authentication"
Claude: *implements auth*
You: "Perfect! The login works now" ← This triggers learning!
```

## Features

- **First-Run Documentation Import** - Scans your entire Development folder for existing documentation
- **Automatic Log Processing** - Monitors and processes Claude Code session logs in real-time
- **Intelligent Lesson Organization** - Categorizes lessons by topic (auth, database, API, etc.)
- **Smart Document Management** - Keeps CLAUDE.md under 30KB with overflow handling
- **Success Pattern Detection** - Identifies which approaches worked well for specific tasks
- **Context Generation** - Creates hierarchical context with category-specific files
- **Slash Commands** - Generates Claude Code slash commands for quick access to patterns
- **Convention Tracking** - Learns your project's coding conventions and patterns
- **Team Knowledge Sharing** - Export and import patterns for team collaboration
- **User Content Preservation** - Your custom notes in CLAUDE.md are never overwritten

## How It Works

1. **First Run** - Prompts to scan your Development folder for all existing documentation
2. **Import** - Extracts lessons learned, warnings, and best practices from your docs
3. **Organize** - Categories lessons into topics (authentication, database, API, etc.)
4. **Monitor** - Watches your Claude Code log files (`~/.claude/projects/`)
5. **Analyze** - Detects successful patterns using multiple indicators
6. **Store** - Builds a searchable knowledge base with SQLite
7. **Generate** - Creates intelligent index with category files in `.claude/lessons/`
8. **Learn** - Improves Claude's responses with hierarchical context

### Multi-Project Support

Claude Cache **automatically handles multiple projects** without any configuration:

- **Automatic Detection** - Identifies different projects from Claude Code session logs
- **Separate Knowledge Bases** - Each project gets its own patterns and context
- **Project-Specific Learning** - React patterns for your frontend won't mix with Python patterns from your API
- **Smart Context Injection** - Claude reads the right `.claude/CLAUDE.md` based on which project you're working in

When you switch between projects in Claude Code, Claude Cache automatically switches context too!

## Installation

### From PyPI (Recommended)
```bash
pip install claude-cache
```

### From Source (Development)
```bash
git clone https://github.com/ga1ien/claude-cache.git
cd claude-cache
pip install -e .
```

## Quick Start

### First Time Setup

```bash
cache start
```

**On first run, you'll see:**
```
🎉 Welcome to Claude Cache!

Would you like to scan for existing documentation?
1. Scan all Claude Code projects (from logs)
2. Scan your Development folder     [Default]
3. Scan a custom directory
4. Skip for now

Choose an option [2]: _
```

This imports all your existing documentation, giving you an immediate knowledge base!

### Running Claude Cache

**Option 1: Terminal Tab (Simplest)**
```bash
cache start
# Keep this terminal tab open
```

**Option 2: tmux (Recommended for long sessions)**
```bash
# Install tmux (one-time)
brew install tmux

# Start in tmux
tmux new -s cache
cache start
# Detach: Ctrl+B then D
# Reattach: tmux attach -t cache
```

**Note:** The `--daemon` flag has issues on macOS. Use tmux or a terminal tab instead.

2. **Use Claude Code as normal** - Claude Cache will automatically process your interactions

3. **Give feedback when things work** - Say "Perfect!", "That worked", or "Thanks!" to help Claude Cache learn

4. **Access your patterns** via slash commands in Claude Code:
- `/project-context [task description]` - Get relevant patterns for your current task
- `/best-practices` - View successful approaches
- `/conventions` - See detected project conventions
- `/quick-ref` - Quick reference for frequently used files
- `/debug-helper` - Get debugging assistance

## Usage

### Basic Commands

```bash
# Start monitoring and processing logs
cache start

# Process existing logs without monitoring
cache process

# Query patterns from your knowledge base
cache query "implement authentication"

# Show statistics
cache stats

# Generate slash commands for a project
cache generate --project my-project
```

### Documentation Commands

```bash
# Scan repository for documentation (lessons learned, READMEs, etc.)
cache scan-docs /path/to/repo

# Scan current directory
cache scan-docs .

# Search through indexed documentation
cache search-docs --query "authentication" --project my-app
```

### Advanced Usage

```bash
# Export patterns for backup or sharing
cache export patterns.json --project my-project

# Import patterns from team member
cache import team-patterns.json

# Rebuild knowledge base from scratch
cache rebuild --confirm

# Generate context for specific request
cache context "fix login bug" --project my-app
```

## Configuration

Claude Cache stores its database at:
```
~/.claude/knowledge/cache.db
```

Slash commands are generated in your project's `.claude/commands/` directory.

### Fine-Tuning Detection

The tool automatically detects and adapts to different tech stacks:

**Built-in Stack Detection:**
- **Frontend**: React, Vue, Angular, CSS, Tailwind
- **Backend**: APIs, Express, Django, Rails
- **Database**: SQL, migrations, ORMs, query optimization
- **Mobile**: React Native, Expo, Flutter
- **DevOps**: Docker, Kubernetes, CI/CD
- **Testing**: Jest, Pytest, Cypress

**Customization via `config.yaml`:**
```yaml
# Adjust success weights for your stack
stack_weights:
  frontend:
    user_satisfied: 0.3
    no_console_errors: 0.25
    component_renders: 0.25

# Add custom success patterns
custom_patterns:
  react_success:
    keywords:
      - "useEffect working"
      - "state updated correctly"
    weight: 1.3
```

**Per-Project Configuration:**
```yaml
projects:
  my-frontend-app:
    primary_stack: frontend
    success_threshold: 0.75
    extra_patterns:
      - "lighthouse score improved"
```

The tool learns what "success" means for YOUR specific tech stack and coding patterns.

### Adding Custom Tech Stacks

**Any tech stack can be added!** Edit `config.yaml`:

```yaml
custom_stacks:
  your_stack_name:
    keywords: ["your", "stack", "keywords"]
    file_patterns: ["*.ext", "folder/*"]
    success_indicators:
      - "compilation successful"
      - "your success condition"
    failure_indicators:
      - "your error pattern"
    weight_multiplier: 1.3
```

**Examples included for:**
- Rust/Actix, Elixir/Phoenix, Go/Gin
- Svelte/SvelteKit, Game Development (Unity/Godot)
- Data Science (Pandas/PyTorch), Blockchain/Web3
- Infrastructure as Code, Embedded Systems

See `custom_stacks_example.yaml` for complete examples.

## How Success Detection Works

Claude Cache uses multiple signals to identify successful patterns:

### Your Feedback (Most Important!)
- **User satisfaction** - "Perfect!", "That worked!", "Thanks!"
- **Task completion** - "Fixed!", "Done!", "Working now!"

### Automatic Detection
- **Test Results** - "Tests passed", "Build successful" in output
- **Error-Free Execution** - No exceptions after changes
- **File Modifications** - Successful edits without errors
- **Success Markers** - ✓, ✅, "SUCCESS" in output

Sessions scoring above 70% are stored as successful patterns.

## Pattern Matching

When you make a new request, the system:

1. Searches for similar previous requests using TF-IDF vectorization
2. Ranks patterns by similarity and success score
3. Generates context from the most relevant patterns
4. Injects this context to improve Claude's response

## Project Structure

```
claude-cache/
├── src/
│   └── cache_for_claude/
│       ├── __init__.py
│       ├── agent.py             # Main coordination agent
│       ├── cli.py               # Command-line interface
│       ├── context_injector.py  # Context and command generation
│       ├── doc_scanner.py       # Documentation scanner for imports
│       ├── lesson_organizer.py  # Categorizes lessons by topic
│       ├── knowledge_base.py    # Database storage
│       ├── log_processor.py     # Log parsing
│       ├── log_watcher.py       # File monitoring
│       └── success_detector.py  # Pattern detection
├── pyproject.toml
└── README.md
```

## Privacy & Security

- All data is stored locally on your machine
- No data is sent to external services
- Sensitive information in logs remains private
- Export/import allows controlled sharing

## Use Cases

### For Individual Developers
- Build a personal knowledge base of what works
- Reduce repetitive explanations to Claude
- Speed up problem-solving with historical context
- Track your most successful coding patterns

### For Teams
- Share successful patterns across team members
- Maintain consistent approaches to common tasks
- Onboard new developers with team-specific knowledge
- Build collective intelligence from everyone's interactions

### For Projects
- Document project-specific conventions automatically
- Track which files are frequently modified together
- Identify common debugging patterns
- Maintain project-specific context

## Working with Multiple Projects

Claude Cache seamlessly handles multiple projects. Here's what happens:

### Automatic Project Separation
```bash
# When you work on different projects:
~/Development/my-react-app     → Patterns stored under "my-react-app"
~/Development/python-api        → Patterns stored under "python-api"
~/Development/mobile-app        → Patterns stored under "mobile-app"
```

### Project-Specific Files Created
```
each-project/
├── .claude/
│   ├── CLAUDE.md              # Main index (5-10KB, Claude reads this)
│   ├── lessons/               # Categorized lessons (unlimited)
│   │   ├── authentication_lessons.md
│   │   ├── database_lessons.md
│   │   ├── api_lessons.md
│   │   └── debugging_lessons.md
│   └── commands/              # Slash commands for Claude Code
```

### Intelligent Document Organization

**CLAUDE.md Structure (Kept Small):**
- Top 5 critical warnings
- Category index with file paths
- Instructions for Claude
- User notes section (preserved)

**Lessons Directory:**
- Organized by topic
- 10 lessons per priority level
- Automatic overflow files for >40 lessons
- Smart navigation between parts

### Managing Multiple Projects
```bash
# View all projects
cache stats

# View specific project
cache stats --project "my-react-app"

# Export one project's patterns
cache export react-patterns.json --project "my-react-app"

# Query across all projects
cache query "authentication"

# Query one project only
cache query "authentication" --project "python-api"
```

### How Claude Uses Project Context
1. You open `my-react-app` in Cursor/Claude Code
2. Claude automatically reads `my-react-app/.claude/CLAUDE.md`
3. Claude now knows your React patterns, not your Python patterns
4. Switch to `python-api` → Claude switches context automatically

**No configuration needed** - it just works!

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Roadmap

- [ ] Web dashboard for pattern visualization
- [ ] Integration with other AI coding tools
- [ ] Pattern clustering and categorization
- [ ] Automated pattern quality scoring
- [ ] Multi-project pattern correlation
- [ ] VSCode extension for pattern access

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by the insight that "if you document along the way, AI hallucinates less because it has more documentation that's personalized to the project."

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/claude-cache/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/claude-cache/discussions)
- **Documentation**: [Full Documentation](https://github.com/yourusername/claude-cache/wiki)

---

**Note**: This tool is not officially affiliated with Anthropic or Claude. It's a community tool designed to enhance your Claude Code experience.