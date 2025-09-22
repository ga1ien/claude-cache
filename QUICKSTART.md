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
# Just run:
cache start

# On first run, you'll see:
# 🎉 Welcome to Claude Cache!
#
# Would you like to scan for existing documentation?
# 1. Scan all Claude Code projects (from logs)
# 2. Scan your Development folder     [Default]
# 3. Scan a custom directory
# 4. Skip for now
#
# Choose an option [2]: _
```

Choose option 2 (default) to scan your entire Development folder!

```bash
# After scanning, you'll see:
# Found 42 projects to scan
# Scanning my-react-app...  [████████] 100%
#
# ✓ Successfully imported 156 documentation files!
# Projects scanned: my-react-app, python-api, mobile-app...
#
# 📊 Your Knowledge Base Starting Point:
#
#   💡 342 lessons learned imported
#   ⚠️  28 critical warnings found
#   ✅ 89 best practices documented
#
#   📁 Knowledge organized across 42 projects
#   📚 Ready to learn from your coding sessions!
```

### Start Monitoring

#### Option 1: Run in Terminal Tab (Simplest)
```bash
# Open a new terminal tab and run:
cache start

# You'll see:
# ╔═══════════════════════════════════════════╗
# ║              claude                       ║
# ║     CACHE v0.1.0                         ║
# ╚═══════════════════════════════════════════╝
# ✓ Monitoring Claude Code logs

# Leave this terminal tab open while you work
```

#### Option 2: Use tmux (Recommended for long-term use)
```bash
# Install tmux first (one-time setup)
brew install tmux

# Start tmux session
tmux new -s cache

# Inside tmux, run:
cache start

# Detach with Ctrl+B then D (leaves it running)
# Reattach later with: tmux attach -t cache
```

**Note:** The `--daemon` flag has compatibility issues on macOS. Use tmux or a dedicated terminal tab instead.

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
│   ├── CLAUDE.md           # ← Claude reads this automatically! (5-10KB)
│   ├── lessons/            # ← Organized lessons by category
│   │   ├── authentication_lessons.md
│   │   ├── database_lessons.md
│   │   ├── api_lessons.md
│   │   └── debugging_lessons.md
│   └── commands/
│       ├── project-context.md
│       ├── best-practices.md
│       └── debug-helper.md
```

### The Magic: CLAUDE.md

This file is automatically read by Claude Code. It's kept small (5-10KB) and contains:
- Top 5 critical warnings from your docs
- Category index pointing to detailed lessons
- Instructions for Claude on where to find specific info
- Your custom notes (preserved during updates)

**Example CLAUDE.md content:**
```markdown
# Claude Code Knowledge Base - your-project

📚 **342 lessons organized across 8 categories**

## 📁 Lesson Categories
- **Authentication** (85 lessons - **12 CRITICAL**): `.claude/lessons/authentication_lessons.md`
  > Never store passwords in plain text...
- **Database** (62 lessons): `.claude/lessons/database_lessons.md`
  > Always use parameterized queries...

## ⚠️ CRITICAL WARNINGS - READ FIRST
1. Never commit API keys to git...
2. SQL injection vulnerability in user inputs...
3. JWT tokens must have expiration...

## 🤖 Claude Instructions
When the user asks about a specific topic:
1. Check the relevant category file in `.claude/lessons/`
2. For authentication issues → `.claude/lessons/authentication_lessons.md`

## 📝 User Notes
<!-- USER_CONTENT_START -->
[Your custom notes here - never deleted!]
<!-- USER_CONTENT_END -->
```

---

## 💡 Step 4: Using Claude Cache

### Important: Give Feedback to Help Cache Learn!

**Claude Cache learns from your success signals.** When Claude helps you and it works, say:
- ✅ **"Perfect!"** or **"That worked!"**
- ✅ **"Thanks, that fixed it!"**
- ✅ **"Great, tests pass now!"**

Without feedback, Cache won't know what worked and won't save patterns!

### While Coding with Claude in Cursor

1. **Start a new Claude chat in Cursor**
2. **Claude automatically sees your patterns** (via CLAUDE.md)
3. **Ask Claude to do something**
4. **When it works, tell Claude!** → This triggers learning
5. **Claude will reference successful past approaches**

### Example Conversations

**Without Feedback (Cache doesn't learn):**
```
You: "Add user authentication"
Claude: *implements auth*
You: [silence, move to next task]
Cache: ❓ Didn't detect success, pattern not saved
```

**With Feedback (Cache learns!):**
```
You: "Add user authentication"
Claude: *implements auth*
You: "Perfect! The login works now"
Cache: ✅ Success detected! Pattern saved for next time
```

**Next Time:**
```
You: "Add password reset"
Claude: "I see you've successfully used JWT with refresh tokens
        for auth. Let me follow that same pattern..."
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

## 🗂️ Multiple Projects? No Problem!

Claude Cache **automatically handles all your projects**:

```bash
# Work on Project A
cd ~/Development/my-react-app
# Claude Code uses my-react-app patterns

# Switch to Project B
cd ~/Development/python-api
# Claude Code automatically uses python-api patterns

# Switch to Project C
cd ~/Development/mobile-app
# Claude Code automatically uses mobile-app patterns
```

**Each project gets its own:**
- `.claude/CLAUDE.md` - Project-specific patterns
- `.claude/commands/` - Project-specific slash commands
- Separate knowledge base - No pattern mixing!

**Check your projects:**
```bash
cache stats                          # See all projects
cache stats --project "my-app"       # See specific project
cache query "auth" --project "api"   # Search in one project
```

---

## 🎮 Common Commands

```bash
# Starting and Stopping
cache start            # Start in terminal (keep tab open)
# Ctrl+C to stop

# Using with tmux
tmux new -s cache      # Create tmux session
tmux attach -t cache   # Reattach to session
tmux ls               # List sessions
tmux kill-session -t cache  # Stop session

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
4. **Cache running**: Check your terminal tab or tmux session

### Live Example

```bash
# 1. Check if cache is running
# In terminal: You see the live status display
# In tmux: tmux ls shows "cache" session

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
3. Make sure cache is running (check terminal or tmux)

### No patterns are being detected
1. Use Claude Code for a few sessions first
2. Check logs exist: `ls ~/.claude/projects/`
3. Lower threshold in `config.yaml` if needed

### Cache won't stay running
```bash
# Use tmux for persistent sessions:
tmux new -s cache
# Run cache start inside tmux
# Detach with Ctrl+B then D

# Or just keep a terminal tab open with:
cache start
```

### macOS-specific issues
The `--daemon` flag has compatibility issues on macOS. Use tmux or a dedicated terminal tab instead.

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