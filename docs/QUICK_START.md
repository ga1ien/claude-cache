# 🚀 Claude Cache Quick Start

Get your personal coding intelligence up and running in under 2 minutes!

## Prerequisites

- Python 3.8+
- Claude Code (VS Code with Claude extension or Cursor)
- You've used Claude Code at least once before

## Installation

### 1. Basic Install (Most Users)

```bash
pip install claude-cache
```

### 2. Enhanced Install (Semantic Search)

```bash
pip install "claude-cache[enhanced]"
```

*Includes ML-powered semantic search for 2x better pattern matching*

### 3. Full Install (With MCP Integration)

```bash
pip install "claude-cache[mcp]"
```

*Includes native Claude Code integration via MCP*

## First Run

### Step 1: Start Claude Cache

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

### Step 2: Let It Learn (One-Time)

The first run processes all your history. This takes:
- **< 10 sessions**: ~30 seconds
- **10-50 sessions**: 1-2 minutes
- **50-200 sessions**: 3-5 minutes
- **200+ sessions**: 5-10 minutes

After this initial processing, it runs in real-time with zero lag.

### Step 3: Start Coding!

Just use Claude Code normally. Claude Cache now:
- ✅ Watches your coding sessions in real-time
- ✅ Learns from successful solutions
- ✅ Captures what doesn't work
- ✅ Builds journey patterns automatically

## Using Claude Cache

### Query Your Knowledge

```bash
# Search for patterns
cache query "authentication"

# Get suggestions for current work
cache suggest

# See what you've learned
cache stats
```

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

### Manual Learning

When you solve something particularly clever:

```bash
cache learn "Fixed auth by using httpOnly cookies with SameSite=strict"
```

## MCP Integration (Optional)

For seamless Claude Code integration, add to your `.claude.json`:

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

Now you can use these commands directly in Claude Code:
- `/cache query [topic]` - Search patterns
- `/cache suggest` - Get contextual suggestions
- `/cache learn [solution]` - Save a pattern

## Background Mode

Run Claude Cache as a background service:

```bash
# Start in background
cache background

# Stop background service
cache stop
```

## What Gets Captured?

### ✅ Automatically Captured:
- Solutions that work (you say "thanks", "perfect", "works")
- Approaches that fail (errors occur, you say "broken", "failed")
- Complete problem→solution journeys
- Patterns that repeat across projects

### ❌ Not Captured:
- Every single edit or keystroke
- Low-confidence patterns
- Project-specific hacks
- Trial-and-error noise

## Privacy & Data

- **100% Local**: All data stays on your machine
- **Your patterns**: Never shared or uploaded
- **No telemetry**: We don't track your usage
- **SQLite database**: Located at `~/.claude/knowledge/cache.db`
- **You control everything**: Export, delete, or modify anytime

## Common Patterns You'll See

After a few days, Claude Cache will recognize patterns like:

```python
# 🏆 Gold Pattern (worked first time)
"useState in event handlers causes stale closures - use useRef"

# 🚫 Anti-Pattern (confirmed failure)
"fs.readFileSync in Next.js API routes causes build failures"

# 🗺️ Journey Pattern (the path to solution)
"CORS error → tried proxy ❌ → tried headers ❌ → configured server ✅"

# ⚠️ Caution Pattern (works but risky)
"Force unwrap in TypeScript bypasses error but hides type issues"
```

## Tips for Best Results

1. **Be expressive**: Say "perfect!", "that worked", "failed", etc.
2. **Let it run**: Keep Claude Cache running during coding sessions
3. **Trust the patterns**: When it says "don't do X", it learned that from YOUR experience
4. **Review periodically**: Run `cache stats` to see what you've learned

## Next Steps

- 📖 Read the [Philosophy](PHILOSOPHY.md) to understand dual-path learning
- 🔧 Check [Configuration](CONFIGURATION.md) for advanced options
- 🧠 Learn [How It Works](HOW_IT_WORKS.md) for technical details
- 💡 See [Use Cases](USE_CASES.md) for real-world examples

## Troubleshooting

### No patterns found?
- Make sure you've used Claude Code before
- Check `~/.claude/projects/` exists
- Run `cache process` to manually process logs

### Not detecting new patterns?
- Ensure Claude Cache is running (`cache start`)
- Be explicit about success/failure ("works!", "failed")
- Check you're in a git repository

### Need help?
```bash
cache --help
```

---

**Ready to never repeat the same mistake twice?** You're all set! Claude Cache is now building your personal coding intelligence. 🎉