# Claude Cache MCP Integration 🚀

## Native Claude Code Tools for Lightning-Fast Development

Version 0.6.1 introduces **MCP (Model Context Protocol)** integration, making Claude Cache tools available directly in Claude Code as native slash commands!

## 🎯 What This Means

Instead of:
1. Opening terminal
2. Running `cache query`
3. Copying results
4. Pasting into Claude

Now you just:
- Type `/mcp__cache__query` in Claude Code
- Get instant results from your vector database
- Claude uses patterns automatically!

## ⚡ Available Tools

### `/mcp__cache__query`
**Instant Vector Search** - Search your patterns and documentation
```
Arguments:
- query: What to search for
- project: (optional) Specific project
- limit: Max results (default: 5)
```

### `/mcp__cache__learn`
**Save Success Patterns** - When something works, save it instantly
```
Arguments:
- description: What worked
- category: Type of solution
- code_snippet: The working code
```

### `/mcp__cache__suggest`
**Proactive Suggestions** - Get relevant patterns based on current work
```
Arguments:
- context: Current code
- intent: What you're trying to do
```

### `/mcp__cache__stats`
**Knowledge Base Stats** - See what you've learned
```
Arguments:
- project: (optional) Specific project stats
```

### `/mcp__cache__browse`
**Documentation Ingestion** - Index documentation and websites
```
Arguments:
- url: Documentation URL to index
- project: (optional) Project name
```

## 🔧 Setup (One-Time)

### 1. Install Claude Cache with MCP
```bash
pip install claude-cache[mcp]
# or if already installed:
pip install --upgrade claude-cache
```

### 2. Configure Claude Code

Add to your project's `.claude.json`:
```json
{
  "mcpServers": {
    "cache": {
      "type": "stdio",
      "command": "cache-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

Or globally in `~/.claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "cache": {
      "type": "stdio",
      "command": "cache-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

### 3. Restart Claude Code

The tools will appear when you type `/` in Claude Code!

## 🧠 Smart Features

### Proactive Pattern Detection
Claude Cache watches what you're working on and proactively suggests relevant patterns. No need to search - it finds what you need!

### Semantic Understanding
With sentence-transformers installed, Claude Cache understands context:
- "auth bug" finds authentication-related fixes
- "speed up database" finds performance optimizations
- "test failing" finds testing solutions

### Auto-Learning
When you say "Perfect!" or "That worked!", Claude Cache automatically saves the pattern for future use.

## 💡 Usage Examples

### Example 1: Finding Authentication Patterns
```
You: /mcp__cache__query authentication JWT
Claude Cache: Found 3 patterns:
1. 🧠 JWT validation with refresh tokens (0.89)
2. 📚 Authentication best practices doc (0.76)
3. 🧠 OAuth2 implementation pattern (0.65)
```

### Example 2: Saving What Works
```
You: That JWT refresh implementation worked perfectly!
You: /mcp__cache__learn
     description: "JWT refresh token rotation"
     category: "authentication"
Claude Cache: ✅ Pattern saved! Now searchable for future use.
```

### Example 3: Getting Proactive Help
```
You: /mcp__cache__suggest
     context: "async function fetchUser(id) { ... }"
     intent: "add caching"
Claude Cache: 💡 Found similar patterns:
1. Redis caching for user queries (95% match)
2. In-memory LRU cache implementation (87% match)
```

## 🚀 Why This Is Game-Changing

1. **Zero Context Switch** - Stay in Claude Code
2. **Instant Access** - Vector search in milliseconds
3. **Proactive** - Suggestions before you ask
4. **Learning** - Gets smarter with every session
5. **Project-Aware** - Different patterns per project

## 📊 Performance

- Query time: <100ms for 10,000 patterns
- Semantic search: 2x better accuracy than keyword
- Auto-indexing: Real-time as you work
- Memory efficient: SQLite + optional embeddings

## 🔍 Debugging

If MCP tools don't appear:

1. Check Claude Code logs:
```bash
claude-code --mcp-debug
```

2. Test MCP server directly:
```bash
cache-mcp
# Should start without errors
```

3. Verify config:
```bash
cat .claude.json
# Should show mcpServers configuration
```

## 🎯 Best Practices

1. **Learn Often** - Use `/mcp__cache__learn` when things work
2. **Query First** - Check patterns before implementing
3. **Be Specific** - Better queries = better results
4. **Use Categories** - Organize patterns by type
5. **Project Separation** - Keep project patterns separate

## 🔮 Coming Next

- Visual pattern browser
- Team pattern sharing
- Auto-categorization
- Pattern quality scoring
- Cross-project pattern suggestions

---

**Claude Cache v0.6.1** - Making AI coding faster, smarter, and more intuitive!

Need help? Check `/mcp__cache__stats` to see your knowledge base status.