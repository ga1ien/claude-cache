# 🚀 Claude Cache - Quick Start Guide

**Get up and running in 5 minutes!**

Claude Cache learns from your Claude Code sessions and builds a memory that makes your AI assistant smarter over time. Here's exactly how to set it up and use it.

---

## 📦 What You're Installing

Claude Cache is a tool that:
- **Watches** your Claude Code conversation logs
- **Learns** which solutions worked well
- **Remembers** successful patterns
- **Shares** this knowledge with future Claude sessions

Think of it as giving Claude a "memory" of what worked before in YOUR specific projects.

---

## 🎯 Step 1: Installation (2 minutes)

### Option A: Quick Install (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/claude-cache.git
cd claude-cache

# 2. Run the quick start script
./quickstart.sh

# That's it! 🎉
```

### Option B: Manual Install
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/claude-cache.git
cd claude-cache

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install
pip install -e .
```

---

## 🏃 Step 2: Start Claude Cache (30 seconds)

### First Time Setup
```bash
# Run this once to process your existing Claude logs
cache process

# You'll see something like:
# ✓ Processing existing logs...
# ✓ Found 15 successful patterns
# ✓ Generated context for my-project
```

### Start Background Monitoring
```bash
# Option 1: Run in background (recommended)
cache start --daemon

# Option 2: Run in foreground (see live updates)
cache start

# You'll see:
# ╔═══════════════════════════════════════════╗
# ║     Claude Cache v0.1.0                  ║
# ╚═══════════════════════════════════════════╝
# ✓ Monitoring Claude Code logs
```

---

## 🔗 Step 3: Integration with Cursor/Claude Code

### How It Works Automatically

**You don't need to do anything special!** Claude Cache works behind the scenes:

1. **You use Claude Code in Cursor normally**
2. **Claude Cache watches the logs automatically**
3. **It updates a file called `.claude/CLAUDE.md` in your project**
4. **Claude reads this file automatically when you start a new chat**

### What Gets Created

Claude Cache creates these files in your project:

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # ← Claude reads this automatically!
│   └── commands/
│       ├── project-context.md
│       ├── best-practices.md
│       └── debug-helper.md
```

### The Magic: CLAUDE.md

This file is automatically read by Claude Code. It contains:
- Your successful coding patterns
- What worked before for similar problems
- Project-specific conventions
- Files that are frequently modified together

**Example CLAUDE.md content:**
```markdown
# Claude Cache Knowledge Base for your-project

## Successful Patterns Detected

### Pattern 1: Authentication Implementation
- **What Worked**: JWT with refresh tokens
- **Files**: auth.js, middleware.js
- **Approach**: Middleware-first implementation

### Pattern 2: Database Migrations
- **What Worked**: Rollback, fix, re-apply
- **Key Learning**: Always backup before migrations
```

---

## 💡 Step 4: Using Claude Cache

### While Coding with Claude in Cursor

**Just code normally!** Claude Cache enhances Claude automatically:

1. **Start a new Claude chat in Cursor**
2. **Claude automatically sees your patterns** (via CLAUDE.md)
3. **Ask Claude to do something similar to before**
4. **Claude will reference successful past approaches**

### Example Conversation

**Before Claude Cache:**
```
You: "Add user authentication"
Claude: [Might suggest wrong library or approach]
```

**After Claude Cache:**
```
You: "Add user authentication"
Claude: "I see you've successfully used JWT with refresh tokens
        in this project. Let me follow the same pattern that
        worked in auth.js..."
```

### Using Slash Commands

In Claude Code, you can use these commands:

```bash
# Get context for a specific task
/project-context implement payment system

# See best practices for your project
/best-practices

# Get debugging help based on past fixes
/debug-helper

# Quick reference of frequently edited files
/quick-ref
```

---

## 📊 Step 5: Check Your Progress

### View Statistics
```bash
cache stats

# You'll see:
# ✨ Claude Cache Statistics ✨
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 Total Patterns    | 42    | 🚀 Thriving!
# 📁 Projects          | 3     | ~14 patterns each
# 💬 Total Requests    | 156   | 73% success rate
```

### Monitor in Real-Time
```bash
# See what's happening live
cache start  # (without --daemon flag)

# Watch as it:
# - Detects new Claude Code sessions
# - Identifies successful patterns
# - Updates your knowledge base
```

---

## 🎮 Common Commands

```bash
# Background Operations
cache start --daemon    # Start in background
cache daemon stop      # Stop background process
cache daemon status    # Check if running

# Data Management
cache process          # Process existing logs
cache stats           # View statistics
cache rebuild         # Rebuild from scratch

# Search and Query
cache query "auth"     # Search for patterns about auth
cache context "fix bug" --project myapp  # Get context for task

# Import/Export
cache export patterns.json    # Backup your patterns
cache import team-patterns.json  # Import team patterns
```

---

## ❓ How Do I Know It's Working?

### Check These Signs:

1. **File exists**: Look for `.claude/CLAUDE.md` in your project
2. **Stats growing**: Run `cache stats` - numbers should increase
3. **Claude references past patterns**: Claude mentions "I see you've done X before"
4. **Daemon running**: `cache daemon status` shows "✓ Running"

### Live Example

```bash
# 1. Check if daemon is running
$ cache daemon status
✓ Claude Cache daemon is running (PID: 12345)

# 2. Check your stats
$ cache stats
🧠 Total Patterns: 25
📁 Projects: 2

# 3. Look for the context file
$ ls .claude/
CLAUDE.md  commands/

# 4. See what Claude knows
$ head .claude/CLAUDE.md
# Claude Cache Knowledge Base for my-project
## Pattern 1: API Endpoint Creation...
```

---

## 🔧 Troubleshooting

### Claude doesn't seem to see my patterns
1. Check if `.claude/CLAUDE.md` exists in your project
2. Run `cache process` to regenerate
3. Make sure daemon is running: `cache daemon status`

### No patterns are being detected
1. Use Claude Code for a few sessions first
2. Check logs exist: `ls ~/.claude/projects/`
3. Lower threshold in `config.yaml` if needed

### Daemon won't start
```bash
# Stop any existing process
cache daemon stop

# Remove stale PID file if needed
rm ~/.claude/knowledge/cache.pid

# Start fresh
cache daemon start
```

---

## 🎉 Success Checklist

- [ ] Installed Claude Cache
- [ ] Ran `cache process` to analyze existing logs
- [ ] Started daemon with `cache start --daemon`
- [ ] See `.claude/CLAUDE.md` in your project
- [ ] Claude references your patterns in conversations
- [ ] Stats show growing pattern count

---

## 💡 Pro Tips

1. **Let it run for a week** - The more you code, the smarter it gets
2. **Check stats weekly** - `cache stats` shows your progress
3. **Export patterns regularly** - `cache export backup.json`
4. **Share with team** - Export and share successful patterns
5. **Restart after updates** - `cache daemon restart`

---

## 🎯 What Happens Next?

Once running, Claude Cache works **completely automatically**:

1. **Every Claude Code session** → Analyzed for patterns
2. **Every successful fix** → Saved to knowledge base
3. **Every new chat** → Claude sees your patterns
4. **Every similar problem** → Claude suggests what worked before

The longer you use it, the more personalized and effective Claude becomes for YOUR specific coding style and projects!

---

## 📚 Learn More

- Run `cache info` for version and details
- Check `cache --help` for all commands
- Visit the [GitHub repo](https://github.com/yourusername/claude-cache) for updates

**Happy coding with your new AI memory! 🚀**