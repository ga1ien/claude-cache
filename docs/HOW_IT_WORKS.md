# 🧠 How Claude Cache Works

**Claude Cache gives your AI assistant perfect memory of every successful solution**

## The Simple Concept

When you solve a problem with Claude, Claude Cache remembers:
- **What** you were trying to do
- **How** you solved it
- **Why** it worked

Next time you face a similar problem, the solution appears instantly.

## Three Ways to Use It

### 1️⃣ Native Claude Code Tools (MCP Mode) - Recommended
```
You: "Help me fix authentication"
You: /mcp__claude-cache__cache_query "auth JWT"
→ Instantly see your previous JWT solutions

When it works:
You: /mcp__claude-cache__cache_learn "Fixed with refresh tokens"
→ Solution saved for next time
```

### 2️⃣ Automatic Background Learning (CLI Mode)
```
You: "Help me fix authentication"
Claude: *implements solution*
You: "Perfect, that works!"
→ Claude Cache automatically captures the pattern
→ Updates .claude/CLAUDE.md in your project
→ Claude reads this file next session
```

### 3️⃣ Manual Pattern Saving (Terminal)
```bash
cache learn "Fixed auth with JWT refresh tokens" --tags "auth,jwt"
cache query "authentication"
```

## The Learning Process

### Step 1: Detection
Claude Cache watches for success signals:
- Natural language: "Perfect!", "That worked!", "Great!"
- Execution success: Tests pass, builds succeed, no errors
- Task completion: Problem → Solution → Success

### Step 2: Pattern Extraction
When success is detected:
```json
{
  "problem": "JWT authentication failing",
  "solution": "Implement refresh token rotation",
  "context": "Node.js, Express, JWT",
  "code": "...",
  "timestamp": "2024-01-15"
}
```

### Step 3: Intelligent Storage
Patterns are stored with:
- **Semantic embeddings** (if enhanced mode)
- **Keyword index** (always available)
- **Project context**
- **Success score**

### Step 4: Smart Retrieval
When you need help:
- **Semantic search**: Understands "auth broken" → finds JWT solutions
- **Keyword fallback**: Always works even without ML
- **Relevance ranking**: Best solutions first

## What Gets Captured

### Automatic Captures
- ✅ Successful code implementations
- ✅ Bug fixes that work
- ✅ Performance optimizations
- ✅ Configuration changes
- ✅ Error resolutions

### Manual Captures
- 💡 Best practices you discover
- 📚 Documentation insights
- 🎯 Team knowledge
- 🔧 Workarounds that work

## Privacy & Security

### Everything is Local
- **No cloud storage** - All data in `~/.claude/`
- **No external API calls** - Works offline
- **No tracking** - Your code stays yours
- **Project isolation** - Each project separate

### What's Stored
```
~/.claude/
├── knowledge/
│   └── cache.db          # SQLite database
├── lessons/              # Organized patterns
└── projects/             # Per-project data
```

## Performance

### Speed
- **Query response**: <100ms for 10K patterns
- **Pattern capture**: Real-time, no lag
- **Memory usage**: <100MB typical
- **CPU usage**: <1% idle, <5% active

### Accuracy
- **Semantic mode**: 60-90% relevance matching
- **Keyword mode**: 40-60% relevance matching
- **Improves over time**: More patterns = better accuracy

## The Feedback Loop

```
You code → Success → Pattern saved →
Next time → Instant solution → Code faster →
More successes → More patterns → Even faster
```

## Why It Works

### 1. Context is Everything
Claude Cache doesn't just save code - it saves the entire context of what worked, when, and why.

### 2. Semantic Understanding
With enhanced mode, it understands that "auth broken" and "JWT failing" are related, even without matching keywords.

### 3. Zero Friction
With MCP tools, there's no context switching. Query and learn without leaving your conversation.

### 4. Continuous Improvement
Every successful coding session makes future sessions better. Your AI assistant gets smarter every day.

## Getting Started

1. **Install**: `pip install "claude-cache[mcp]"`
2. **Configure**: Add to `.claude.json`
3. **Use**: Type `/` in Claude Code to see your tools
4. **Learn**: Every success makes you faster

That's it! Claude Cache is now learning from every successful solution, building your personal knowledge base that makes coding faster every day.