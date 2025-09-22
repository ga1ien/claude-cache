# Claude Cache

[![PyPI version](https://badge.fury.io/py/claude-cache.svg)](https://pypi.org/project/claude-cache/)
[![Python Support](https://img.shields.io/pypi/pyversions/claude-cache)](https://pypi.org/project/claude-cache/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent memory system for AI coding with MCP integration, hybrid vector search, and proactive pattern suggestions**

Claude Cache v0.6.0 introduces **native Claude Code integration** via MCP (Model Context Protocol), providing instant access to your knowledge base directly in Claude Code. Three usage modes: Basic CLI, Enhanced semantic search, and revolutionary MCP tools.

*Note: This is an independent tool for enhancing Claude Code, not an official Anthropic product.*

## 🚀 What's New in v0.6.0

### 🎯 Native Claude Code Integration (MCP)
- **5 Native Tools** accessible via `/mcp__claude-cache__*` commands
- **Zero Context Switch** - query patterns directly in Claude Code
- **Instant Results** - millisecond response times
- **Proactive Suggestions** - Claude recommends relevant patterns
- **Real-time Learning** - save patterns with one command

### 🔧 Three Clear Usage Modes
- **Basic**: `pip install claude-cache` (CLI + TF-IDF search)
- **Enhanced**: `pip install claude-cache[enhanced]` (+ semantic search)
- **MCP**: `pip install claude-cache[mcp]` (+ native Claude Code tools)

## 🎯 MCP Tools Available in Claude Code

### `/mcp__claude-cache__query`
🔍 **Instant Pattern Search** - Find relevant solutions from past sessions
```
Arguments:
- query: "authentication JWT"
- project: (optional) specific project
- limit: max results (default: 5)
```

### `/mcp__claude-cache__learn`
💾 **Save Success Patterns** - Store working solutions for future use
```
Arguments:
- description: "JWT refresh token implementation"
- category: "authentication"
- code_snippet: (optional) working code
```

### `/mcp__claude-cache__suggest`
💡 **Proactive Recommendations** - Get pattern suggestions based on context
```
Arguments:
- context: current code you're working on
- intent: what you're trying to accomplish
```

### `/mcp__claude-cache__stats`
📊 **Knowledge Base Statistics** - View patterns, search mode, project info

### `/mcp__claude-cache__browse`
🌐 **Ingest Documentation** - Index URLs for searchable content

## 🧠 How Claude Cache Learns (v0.5.0+)

Claude Cache now has **5 ways to learn and retrieve patterns**:

### 1. **Semantic Intent Detection** (v0.3.0)
- Understands subtle feedback like "ok let's move on" or "makes sense"
- Uses TF-IDF vectorization and cosine similarity
- No need for explicit "Perfect!" anymore

### 2. **Execution Monitoring** (v0.3.0)
- Detects when tests pass
- Recognizes successful builds
- Identifies server startups
- Captures 10x more patterns automatically

### 3. **Error Learning** (NEW in v0.4.0)
- Learns from every error encountered
- Maps errors to their solutions
- Builds a "what not to do" knowledge base

### 4. **Cross-Project Transfer** (NEW in v0.4.0)
- Authentication patterns that work in one project apply to others
- API patterns transfer between similar tech stacks
- Database solutions work across projects

### 5. **Hybrid Vector Search** (NEW in v0.5.0)
- Semantic search understands context and meaning when available
- Automatic fallback to keyword matching ensures always works
- No required dependencies, optional enhancement available

## Features

### Core Features
- **First-Run Documentation Import** - Scans your entire Development folder for existing documentation
- **Automatic Log Processing** - Monitors and processes Claude Code session logs in real-time
- **Hierarchical Documentation** - Lightweight CLAUDE.md index + unlimited categorized lessons
- **Smart Document Management** - Keeps CLAUDE.md under 5-10KB with overflow to category files
- **Multi-Project Support** - Each project gets its own `.claude/` directory

### v0.3.0 Features
- **Semantic Intent Detection** - Understands user satisfaction without explicit keywords
- **Automated Execution Monitoring** - Learns from test results, builds, and server outputs
- **Context Prioritization** - Ranks patterns by relevance, recency, and success rate

### v0.5.0 Features (NEW)
- **Hybrid Vector Search** - Semantic understanding with graceful fallback
- **Optional Enhancement** - Works perfectly without, better with sentence-transformers
- **Search Mode Transparency** - Know whether using semantic or keyword search
- **Automatic Pattern Indexing** - All patterns indexed for optimal retrieval

### v0.4.0 Features
- **Error Pattern Database** - Comprehensive error → solution mappings
- **Efficiency Tracking** - Time and complexity metrics for every solution
- **Global Pattern Library** - Transferable solutions across projects
- **Technology Compatibility Matrix** - Intelligent pattern adaptation
- **Prevention Tips Generator** - Automatic best practices from errors

## How It Works

### File Organization

Claude Cache creates a hierarchical documentation structure **in each project**:

```
your-project/
├── .claude/
│   ├── CLAUDE.md              # Main index (5-10KB) - Claude reads this first
│   ├── lessons/               # Categorized lessons (unlimited size)
│   │   ├── authentication_lessons.md
│   │   ├── database_lessons.md
│   │   ├── api_lessons.md
│   │   ├── debugging_lessons.md
│   │   ├── performance_lessons.md
│   │   ├── security_lessons.md
│   │   └── [category]_lessons.md
│   └── commands/              # Slash commands for Claude Code
│       ├── project-context.md
│       ├── best-practices.md
│       └── quick-ref.md
```

**Key Points:**
- **CLAUDE.md** is a lightweight index (5-10KB) that Claude reads
- **lessons/** contains unlimited categorized documentation
- **Each project** maintains its own `.claude/` directory
- **Automatic organization** by topic (auth, database, API, etc.)

### Learning Pipeline
1. **Monitor** - Watches Claude Code sessions in real-time
2. **Analyze** - Detects patterns using 4 learning systems:
   - Success patterns (what worked)
   - Error patterns (what failed and how to fix)
   - Efficiency metrics (what's fastest)
   - Cross-project patterns (what transfers)
3. **Rank** - Prioritizes patterns by efficiency and success rate
4. **Transfer** - Shares applicable patterns across projects
5. **Inject** - Provides context to Claude for better responses

### Intelligence Systems

#### Error Pattern Learning
```python
# Automatically learns from errors:
ModuleNotFoundError → npm install [package]
TypeError → Add type checking
NullReference → Implement null checks
Build Failed → Fix import paths
```

#### Differential Learning
```python
# Tracks and compares solutions:
Pattern A: 5 minutes, 10 lines changed → Score: 95
Pattern B: 30 minutes, 100 lines changed → Score: 40
# Always suggests Pattern A for similar tasks
```

#### Cross-Project Intelligence
```python
# Shares patterns intelligently:
Project A (React + Node) → Auth pattern
Project B (React + Express) → Can use same auth pattern
Project C (Vue + Django) → Adapts auth pattern for Vue
```

## Installation

### Choose Your Mode

#### 🚀 MCP Mode (Recommended - Native Claude Code Tools)
```bash
pip install claude-cache[mcp]

# Add to .claude.json:
{
  "mcpServers": {
    "claude-cache": {
      "type": "stdio",
      "command": "cache-mcp"
    }
  }
}

# Restart Claude Code - Type / to see new tools!
```

#### ⚡ Enhanced Mode (Semantic Search)
```bash
pip install claude-cache[enhanced]
# All CLI features + 2x better pattern matching
```

#### 🔧 Basic Mode (CLI Only)
```bash
pip install claude-cache
# Core functionality, TF-IDF search, works everywhere
```

### From Source (Development)
```bash
git clone https://github.com/ga1ien/claude-cache.git
cd claude-cache
pip install -e .[mcp]  # For full features
```

## Quick Start

### MCP Mode (Revolutionary Experience)

1. **Install with MCP support:**
   ```bash
   pip install claude-cache[mcp]
   ```

2. **Configure Claude Code** - Add to `.claude.json`:
   ```json
   {
     "mcpServers": {
       "claude-cache": {
         "type": "stdio",
         "command": "cache-mcp"
       }
     }
   }
   ```

3. **Restart Claude Code**

4. **Use native tools:**
   ```
   Type "/" in Claude Code to see:
   /mcp__claude-cache__query
   /mcp__claude-cache__learn
   /mcp__claude-cache__suggest
   /mcp__claude-cache__stats
   /mcp__claude-cache__browse
   ```

### CLI Mode (Traditional)

```bash
# Start monitoring (keep terminal open)
cache start

# Query patterns
cache query "authentication"

# Get statistics
cache stats
```

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

### Intelligence Commands (v0.4.0)

```bash
# View error patterns and prevention tips
cache errors --project my-app

# Compare solution efficiency
cache compare "user authentication" --show-metrics

# Find transferable patterns
cache transfer --from project-a --to project-b

# Generate efficiency report
cache efficiency --project my-app

# Show cross-project insights
cache insights --global
```

### Documentation Commands

```bash
# Scan repository for documentation
cache scan-docs /path/to/repo

# Search through indexed documentation
cache search-docs --query "authentication" --project my-app
```

### Advanced Usage

```bash
# Export patterns for backup or sharing
cache export patterns.json --project my-project

# Import patterns from team member
cache import team-patterns.json

# View prevention guide for common errors
cache prevent --project my-app

# Analyze pattern transferability
cache analyze --pattern auth --target new-project
```

## Configuration

### Data Storage

Claude Cache stores its global knowledge base at:
```
~/.claude/knowledge/
├── cache.db          # Main knowledge base
├── errors.db         # Error patterns (v0.4.0)
├── metrics.db        # Efficiency metrics (v0.4.0)
└── global.db         # Cross-project patterns (v0.4.0)
```

### Intelligence Configuration (v0.4.0)

Customize learning weights in `~/.claude/config.json`:
```json
{
  "efficiency_weights": {
    "time_weight": 0.3,
    "simplicity_weight": 0.2,
    "reliability_weight": 0.25,
    "recency_weight": 0.15,
    "frequency_weight": 0.1
  },
  "error_learning": {
    "min_occurrences": 2,
    "prevention_tips": true
  },
  "cross_project": {
    "min_transferability": 0.3,
    "auto_adapt": true
  }
}
```

## How Learning Works

### Error Pattern Example
```
1. You encounter: "ModuleNotFoundError: No module named 'requests'"
2. You fix it: "pip install requests"
3. Cache learns: Error type → Solution → Prevention
4. Next time: Cache suggests the fix immediately
5. Prevention tip: "Add requests to requirements.txt"
```

### Efficiency Tracking Example
```
1. Task: "Add user authentication"
2. Attempt 1: Custom implementation (2 hours)
3. Attempt 2: Use Auth0 library (30 minutes)
4. Cache learns: Auth0 approach is 4x faster
5. Next project: Suggests Auth0 first
```

### Cross-Project Transfer Example
```
1. Project A (React): Implement JWT authentication
2. Success: Pattern stored with React/JWT tags
3. Project B (React): Needs authentication
4. Cache: Automatically suggests Project A's JWT pattern
5. Project C (Vue): Needs authentication
6. Cache: Adapts JWT pattern for Vue syntax
```

## Metrics & Impact

### v0.6.0 Performance Improvements
- **Zero context switch** - access patterns without leaving Claude Code
- **Millisecond response** times for pattern queries
- **5 native tools** for comprehensive knowledge base access
- **Proactive suggestions** - Claude recommends patterns before you ask
- **Real-time learning** - save patterns with single command

### Three-Mode Architecture Benefits
- **100% compatibility** - works everywhere with Basic mode
- **2x better accuracy** - Enhanced mode semantic search
- **Ultimate experience** - MCP mode native integration

### Learning Statistics
```bash
cache stats --detailed

# Shows:
# - Total patterns learned: 1,247
# - Error patterns prevented: 89
# - Average time saved per pattern: 12 minutes
# - Cross-project transfers: 34
# - Efficiency improvement: 67%
```

## Examples

### MCP Mode in Action
```
# Working on authentication in Claude Code:
You: "I need to implement user login"

# Instead of copying/pasting from terminal:
You: "/mcp__claude-cache__query user authentication"

# Instant results in Claude Code:
Claude: "🔍 Found 3 results for 'user authentication'

**1. 🧠 Pattern** (Score: 0.945)
📁 Project: my-react-app
📝 JWT implementation with refresh tokens...

**2. 🧠 Pattern** (Score: 0.823)
📁 Project: mobile-app
📝 OAuth flow with Google/Facebook..."

# When it works:
You: "/mcp__claude-cache__learn JWT login with validation working"
Claude: "✅ Pattern Saved Successfully!"
```

### Proactive Suggestions
```
# Claude analyzes your code context:
You: "/mcp__claude-cache__suggest"
     context="Setting up Express API routes"
     intent="add authentication middleware"

Claude: "💡 Based on your context, I found these relevant patterns:
- JWT middleware pattern (95% relevance) from my-api project
- Rate limiting implementation (87% relevance) from web-service
- Session management (79% relevance) from dashboard-app"
```

### Zero Context Switch Workflow
```
# Traditional approach:
1. Code in Claude Code
2. Open terminal
3. Run: cache query "auth"
4. Copy results
5. Paste in Claude Code
6. Continue coding

# MCP approach:
1. Code in Claude Code
2. Type: /mcp__claude-cache__query auth
3. Get instant results
4. Continue coding (no interruption!)
```

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get running in 2-5 minutes
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup for all modes
- **[How It Works](docs/HOW_IT_WORKS.md)** - Technical architecture details
- **[Usage Examples](docs/example_usage.md)** - Real-world workflows
- **[MCP Integration](docs/MCP_INTEGRATION.md)** - Native Claude Code tools
- **[Release Notes](docs/v0.6.0_RELEASE.md)** - What's new in v0.6.0

## Contributing

We welcome contributions! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional error pattern detectors
- New efficiency metrics
- Language-specific adapters for cross-project transfer
- Performance optimizations
- Documentation improvements

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the Claude Code community
- Inspired by the need for persistent AI memory
- Special thanks to all contributors and early adopters

## Support

- **Issues**: [GitHub Issues](https://github.com/ga1ien/claude-cache/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ga1ien/claude-cache/discussions)
- **Documentation**: [Full Docs](https://github.com/ga1ien/claude-cache/wiki)

---

**Note**: This is an independent project and not affiliated with Anthropic. Claude Cache is designed to enhance your Claude Code experience through intelligent memory and learning systems.