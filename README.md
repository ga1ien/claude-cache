> **Superseded by [braintied/watchtower](https://github.com/braintied/watchtower).**
>
> Claude Cache was the first cut of session intelligence for Claude Code. New work lives in Watchtower. This repo stays up for existing installs.

# Claude Cache 🧠

```
                              claude
 ██████╗ █████╗  ██████╗██╗  ██╗███████╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝
██║     ███████║██║     ███████║█████╗      v0.9.0
██║     ██╔══██║██║     ██╔══██║██╔══╝   🤖 Intelligent
╚██████╗██║  ██║╚██████╗██║  ██║███████╗    Detection
 ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
```

[![PyPI version](https://badge.fury.io/py/claude-cache.svg)](https://pypi.org/project/claude-cache/)
[![Python Support](https://img.shields.io/pypi/pyversions/claude-cache)](https://pypi.org/project/claude-cache/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Your personal coding intelligence that learns from both successes AND failures. Claude Cache captures your complete problem-solving journey using truly intelligent conversation understanding - no more keyword guessing.**

## 🧠 Learning from Everything, Storing What Matters

Claude Cache revolutionizes how AI coding assistants remember. Unlike traditional tools that only save working code, we capture your complete learning journey:

### ✅ **Success Patterns** - What Works
- Elegant solutions that worked first time
- Proven approaches you can trust
- Best practices from your actual experience

### 🚫 **Anti-Patterns** - What Doesn't Work
- Failed approaches to avoid
- Dead ends that waste time
- Context-specific pitfalls you've discovered

### 🗺️ **Journey Patterns** - The Path to Solution
- Complete problem-solving sequences
- Key insights that unlock breakthroughs
- The "why" behind the solution

## Why This Changes Everything

Consider this real scenario:
```
Monday: You spend 2 hours debugging an authentication loop
  - Try localStorage fix (fails)
  - Check cookies (fails)
  - Debug state management (fails)
  - Finally realize it's a useEffect issue (success!)

Friday: You hit the same auth loop issue
```

**Without Claude Cache**: You might try localStorage again, wasting time on approaches that didn't work.

**With Claude Cache**:
- ⚠️ Immediately warns: "Don't check localStorage - that failed before"
- ✅ Suggests: "This is likely a useEffect issue - here's what worked"
- 🗺️ Shows the journey: "Last time this took 4 attempts, skip to solution #4"

## 🎯 Pattern Classification System

Every pattern is classified by quality and type:

| Type | Symbol | Description | Example |
|------|--------|-------------|------|
| **Gold** | 🏆 | Worked first time, elegant | "useEffect with cleanup solved it immediately" |
| **Silver** | 🥈 | Worked after 2-3 attempts | "Third approach with useMemo worked" |
| **Bronze** | 🥉 | Eventually worked | "Finally solved after trying 5 approaches" |
| **Anti-Pattern** | 🚫 | Confirmed failure | "localStorage doesn't work for auth tokens" |
| **Journey** | 🗺️ | Complete problem→solution path | "Auth fix: tried A, B failed → C worked because..." |
| **Caution** | ⚠️ | Works but has tradeoffs | "Quick fix but needs refactoring" |

## Native Claude Code Tools

Type `/` in Claude Code to access these powerful tools:

### `/mcp__cache__query`
Search your entire knowledge base instantly
```
Example: /mcp__cache__query "authentication JWT"
Returns: Your previous JWT implementations with context
```

### `/mcp__cache__learn`
Save successful solutions for future use
```
Example: /mcp__cache__learn
  solution: "Fixed CORS with proxy middleware"
  tags: "cors,api,middleware"
```

### `/mcp__cache__suggest`
Get proactive recommendations based on current context
```
Example: /mcp__cache__suggest "working on API endpoints"
Returns: Relevant patterns from your knowledge base
```

### `/mcp__cache__stats`
Monitor your growing knowledge base
```
Shows: Total patterns, projects, search capabilities
```

### `/mcp__cache__browse`
Index documentation for instant access
```
Example: /mcp__cache__browse "https://docs.example.com"
Result: Documentation indexed and searchable
```

## 🚀 Quick Start (2 Minutes)

### 1. Install Claude Cache
```bash
# Using pipx (recommended - isolated installation)
pipx install "claude-cache[mcp]"

# Alternative: Using pip directly
pip install --user "claude-cache[mcp]"

# Basic version
pipx install claude-cache
```

### 2. First Run - Choose Your Mode

**Real-time Learning (Recommended):**
```bash
cache start --watch
```

**One-time Processing:**
```bash
cache start
```

You'll see:
```
✓ Knowledge base initialized at ~/.claude/knowledge/cache.db
Processing 47 existing log files...
  Processing: YourProject/session1.jsonl
  Processing: YourApp/session2.jsonl
  ...
✓ Learned 23 patterns from your history
Starting real-time monitoring...
```

**What's happening?**
- Claude Cache found all your past Claude Code sessions
- It's analyzing your historical coding patterns
- Learning from your successes AND failures
- Building your personal knowledge base

### 3. Use It Immediately
```bash
# Interactive monitoring dashboard (press 'h' for help, 't' for tutorial)
cache monitor

# Query your knowledge
cache query "authentication"

# Get contextual suggestions
cache suggest

# See what you've learned
cache stats
```

### 3. Claude Code Integration (Optional)
Add to your `.claude.json`:
```json
{
  "mcpServers": {
    "cache": {
      "type": "stdio",
      "command": "cache-mcp"
    }
  }
}
```

Start MCP server separately:
```bash
cache-mcp
```

Restart Claude Code and type `/` to see your new tools!

### 4. Test It's Working
```bash
# Check status
cache stats

# Search existing patterns
cache query "authentication"

# Get contextual suggestions
cache suggest
```

## 🤖 Intelligent Pattern Detection

Claude Cache v0.9.0 introduces truly intelligent success detection that goes beyond simple keywords:

### 🧠 **Multi-Signal Fusion**
Combines four analysis techniques for accurate pattern detection:
1. **Conversation Flow Analysis** - Understands the natural progression of problem-solving
2. **Execution Results** - Prioritizes test passes, build success, and error resolution
3. **User Intent Detection** - Analyzes what you're actually trying to accomplish
4. **Behavioral Patterns** - Recognizes implicit success signals like moving to the next task

### 💡 **Smart Success Detection**
- **Implicit Success**: When Claude says "done" and you continue to the next problem = success
- **Test Prioritization**: Passing tests are the strongest success signal
- **Context Understanding**: Knows the difference between exploration and implementation phases
- **Auto-Save**: Automatically saves high-confidence patterns without interrupting your flow

## 🔬 How It Works

Claude Cache uses dual-path learning to build comprehensive intelligence:

### 1. **Historical Analysis** (First Run)
- Processes all your existing Claude Code sessions
- Extracts patterns from past successes and failures
- Builds initial knowledge base from your history
- Takes 30 seconds to 10 minutes depending on history size

### 2. **Real-Time Monitoring** (Continuous)
- Watches your coding sessions in real-time
- Captures successful solutions ("perfect!", "works!")
- Learns from failures (errors, "broken", "failed")
- Records complete problem→solution journeys
- Zero lag - runs silently in background

### 3. **Intelligent Detection & Retrieval**
- **Multi-Signal Analysis**: Combines conversation flow, execution results, user behavior, and intent
- **Behavioral Understanding**: Detects success when AI says "done" and user moves to next task
- **Semantic Search**: ML-powered understanding of meaning beyond keywords
- **Context Awareness**: Right solution for your specific stack and current problem
- **Journey Replay**: Shows the path that worked before

### 4. **Privacy First Design**
- **100% Local**: All data stays on your machine
- **No Cloud**: Never uploads or shares your patterns
- **No Telemetry**: We don't track what you're learning
- **You Own It**: SQLite database you fully control

## 📊 What Gets Captured?

### ✅ Automatically Captured:
- Solutions that work (you say "thanks", "perfect", "works")
- Approaches that fail (errors occur, you say "broken", "failed")
- Complete problem→solution journeys
- Patterns that repeat across projects
- High-confidence solutions (80%+ success rate)
- Consistent failures (repeatedly don't work)

### ❌ Not Captured:
- Every single edit or keystroke
- Low-confidence patterns
- Project-specific hacks
- Trial-and-error noise
- One-off solutions

## Perfect For

- **Solo Developers**: Build a personal knowledge base of solutions
- **Development Teams**: Share successful patterns and best practices
- **Learning**: Capture and revisit complex problem-solving approaches
- **Productivity**: Eliminate repetitive problem-solving across projects

## 💡 Real-World Impact

After using Claude Cache for a month, developers typically have:
- **50-100 high-quality patterns** per project
- **30-50 anti-patterns** preventing repeated mistakes
- **20-30 journey patterns** showing problem-solving paths
- **90%+ relevance rate** when patterns are suggested
- **50% reduction** in time spent on familiar problems

### Example Output
```bash
$ cache query "auth redirect"

🔍 Found 3 relevant patterns:

1. ✅ Success Pattern (React)
   "useEffect cleanup prevents auth redirect loops"
   Project: YourApp | Confidence: 92%

2. 🚫 Anti-Pattern
   "Don't store auth tokens in localStorage"
   Failed in: YourApp, AnotherApp | Alternative: Use httpOnly cookies

3. 🗺️ Journey Pattern
   "Auth loop fix: localStorage ❌ → cookies ❌ → useEffect ✅"
   Time saved next time: ~45 minutes
```

## Performance

- **Speed**: <100ms query response for 10K+ patterns
- **Accuracy**: 60-90% relevance in semantic matching
- **Storage**: Efficient SQLite with optional vector embeddings
- **Privacy**: Zero external API calls, completely local

## Terminal Usage

Claude Cache offers multiple ways to run in terminal:

### **🚀 Quick Start (Recommended)**
```bash
# Start background learning system
cache background

# Search patterns
cache query "authentication patterns"

# Get contextual suggestions
cache suggest

# View statistics
cache stats
```

### **⚙️ Advanced Options**
```bash
# Full system with terminal interface
cache run

# Process existing logs only (one-time)
cache process

# Foreground mode (for testing)
cache start --watch

# Include MCP server
cache run --with-mcp
```

### **🔄 Background Process Methods**
```bash
# Using nohup (survives terminal closure)
nohup cache start --watch > cache.log 2>&1 &

# Using screen (detachable sessions)
screen -S claude-cache -d -m cache start --watch

# Using tmux (session management)
tmux new-session -d -s claude-cache 'cache start --watch'
```

### **💾 Manual Learning**
```bash
# Save successful solutions
cache learn "JWT middleware with validation" --tags "auth,jwt,security"

# Index documentation
cache browse https://docs.example.com
cache scan-docs .  # Scan current repository

# Export/import knowledge
cache export backup.json
cache import backup.json
```

### **🤖 Intelligent Analysis (v0.9.0)**
```bash
# Analyze conversation sessions with intelligent detection
cache analyze --recent                    # Most recent session
cache analyze --project myapp            # Sessions from specific project
cache analyze --session-file session.jsonl  # Specific session file

# Quick pattern capture
cache win "JWT refresh token implementation"     # Save successful solution
cache fail "localStorage for tokens" --why "security risk" --alternative "httpOnly cookies"

# Recent pattern monitoring
cache recent                             # Last 24 hours
cache recent --today                     # Today only
cache recent --week --watch             # Last week with live updates

# Project management
cache project list                       # List all projects
cache project set myapp                  # Set default project
cache project                           # Show current context
```

### **📊 Advanced Features**
```bash
# Interactive monitoring dashboard
cache monitor                           # Live pattern detection
cache monitor --duration 30            # Monitor for 30 seconds

# Pattern quality filtering
cache query "auth" --gold               # Only high-quality patterns
cache query "database" --anti           # Show what NOT to do
cache query "testing" --journey         # Show problem→solution paths

# Documentation search
cache search-docs "API rate limiting"   # Search indexed docs
cache scan-docs . --project webapp     # Index current repository

# System maintenance
cache rebuild                           # Rebuild knowledge base
cache rebuild --confirm                 # Skip confirmation prompt
```

### **🛠️ Process Control**
```bash
# Check what's running
ps aux | grep cache

# Stop background processes
pkill -f 'cache start'

# View logs
tail -f /tmp/claude-cache.log
```

**📚 Complete guide**: See [docs/TERMINAL_SETUP.md](docs/TERMINAL_SETUP.md) for detailed setup options.

## 🏗️ Architecture

```
Claude Cache/
├── 🧠 Dual-Path Learning Engine
│   ├── Success Pattern Detector
│   ├── Anti-Pattern Analyzer
│   ├── Journey Pattern Tracker
│   └── Pattern Classification System
├── 💾 Knowledge Base (SQLite)
│   ├── Success Patterns (Gold/Silver/Bronze)
│   ├── Anti-Patterns (What Not to Do)
│   ├── Journey Patterns (Problem→Solution)
│   ├── Cross-Project Intelligence
│   └── Documentation Index
├── 🔍 Intelligent Search
│   ├── Semantic Understanding (ML)
│   ├── Context-Aware Matching
│   └── Pattern Similarity Analysis
├── 🔌 MCP Integration
│   └── Native Claude Code Tools
└── 📊 Quality Control
    ├── Confidence Scoring
    ├── Pattern Validation
    └── Continuous Evolution
```

## 📚 Documentation

- 📦 [Installation Guide](docs/INSTALLATION.md) - Step-by-step installation for all platforms
- 🚀 [Quick Start Guide](docs/QUICK_START.md) - Get running in 2 minutes
- 🗣️ [Communication](docs/COMMUNICATION.md) - How Claude Cache provides feedback and guidance
- 🧠 [Philosophy](docs/PHILOSOPHY.md) - Why dual-path learning matters
- 🔧 [Configuration](docs/CONFIGURATION.md) - Advanced options
- 📖 [How It Works](docs/HOW_IT_WORKS.md) - Technical deep dive
- 💡 [Use Cases](docs/USE_CASES.md) - Real-world examples
- 🖥️ [Terminal Setup](docs/TERMINAL_SETUP.md) - Command line mastery

## Contributing

We welcome contributions! Areas of interest:
- Additional pattern detection algorithms
- Better journey pattern analysis
- Support for more development environments
- Team collaboration features
- Language-specific pattern recognition

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built with love for the developer community. Special thanks to all early adopters and contributors who helped shape Claude Cache into what it is today.

---

## 🎯 The Ultimate Goal

Claude Cache aims to be your **external coding brain** - remembering not just what worked, but understanding:
- Why it worked
- When it works
- What doesn't work
- How you got there

Every developer's journey is unique. Claude Cache ensures that journey makes you smarter with every line of code you write.

---

**Ready to never repeat the same mistake twice?** Install Claude Cache today and build your personal coding intelligence.

*"The best developers aren't those who never fail, but those who learn from every failure and success alike."*

*Claude Cache is an independent tool for enhancing Claude Code, not an official Anthropic product.*