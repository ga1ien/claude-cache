# Claude Cache 🧠

[![PyPI version](https://badge.fury.io/py/claude-cache.svg)](https://pypi.org/project/claude-cache/)
[![Python Support](https://img.shields.io/pypi/pyversions/claude-cache)](https://pypi.org/project/claude-cache/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Your AI coding assistant now has perfect memory**

Claude Cache is an intelligent memory system that ensures you never solve the same problem twice. It learns from every successful solution, understands context through semantic search, and provides instant access to your accumulated knowledge directly within Claude Code.

## ✨ Why Claude Cache?

Every developer loses hours re-solving problems they've already fixed. Claude Cache acts as your AI's perfect memory:

- **Remember Everything**: Automatically captures successful solutions and patterns
- **Find Instantly**: Semantic search understands what you need, not just keywords
- **Learn Continuously**: Every coding session makes future development faster
- **Zero Context Switching**: Access everything directly in Claude Code via MCP tools

## 🚀 Quick Start

### Installation

Choose your experience level:

```bash
# Basic - CLI tools with keyword search
pip install claude-cache

# Enhanced - Semantic search with AI understanding
pip install "claude-cache[enhanced]"

# Complete - Full MCP integration for Claude Code (Recommended)
pip install "claude-cache[mcp]"
```

### Setup for Claude Code

1. **Add to `.claude.json`** in your project root:
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

2. **Restart Claude Code**

3. **Type `/` to see your new tools!**

## 🎯 Native Claude Code Tools

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

## 🧠 How It Works

Claude Cache creates an intelligent layer between you and your AI assistant:

1. **Automatic Learning**: Detects successful patterns through:
   - Natural language understanding ("that worked!", "perfect!")
   - Execution monitoring (passing tests, successful builds)
   - Error resolution tracking

2. **Smart Retrieval**: Three-tier search system:
   - **Semantic Search**: Understands meaning and context (with sentence-transformers)
   - **TF-IDF Fallback**: Always works even without ML libraries
   - **Pattern Matching**: Finds similar code structures

3. **Context Awareness**: Maintains separate knowledge bases per project while sharing common patterns across projects

## 💡 Real-World Examples

### Example 1: Authentication Debugging
```python
# Monday: Spend 2 hours debugging JWT refresh tokens
# Save the solution automatically when it works

# Friday: Hit the same issue
/mcp__cache__query "JWT refresh failing"
# → Instantly get your exact solution with context
```

### Example 2: API Pattern Reuse
```python
# Project A: Build a perfect rate limiter
# Claude Cache automatically captures the pattern

# Project B: Need rate limiting
/mcp__cache__suggest "API middleware"
# → Get your rate limiter pattern with implementation details
```

### Example 3: Team Knowledge Sharing
```python
# Senior dev solves complex database optimization
/mcp__cache__learn "Optimized query with indexes"

# Junior dev hits performance issue
/mcp__cache__query "slow database query"
# → Finds senior dev's solution with explanation
```

## 📊 Performance & Privacy

- **Speed**: <100ms query response for 10K+ patterns
- **Accuracy**: 60-90% relevance in semantic matching
- **Storage**: Efficient SQLite with optional vector embeddings
- **Privacy**: All data stored locally in `~/.claude/knowledge/`
- **No External Calls**: Works completely offline

## 🔧 CLI Usage

For terminal power users:

```bash
# Start monitoring (runs in background)
cache start

# Manual pattern save
cache learn "Solution description" --tags "tag1,tag2"

# Search patterns
cache query "search term"

# Index documentation
cache browse https://docs.example.com

# View statistics
cache stats
```

## 📦 Architecture

```
Claude Cache/
├── Knowledge Base (SQLite)
│   ├── Success Patterns
│   ├── Error Resolutions
│   ├── Documentation
│   └── Cross-Project Index
├── Vector Search Engine
│   ├── Semantic Embeddings (optional)
│   └── TF-IDF Fallback
├── MCP Server
│   └── Native Claude Code Tools
└── Auto-Learning System
    ├── Intent Detection
    ├── Execution Monitor
    └── Pattern Extractor
```

## 🤝 Contributing

We welcome contributions! Areas of interest:
- Additional MCP tools
- Better pattern extraction algorithms
- Support for more development environments
- Team collaboration features

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with love for the developer community. Special thanks to all early adopters and contributors who helped shape Claude Cache into what it is today.

---

*Note: Claude Cache is an independent tool for enhancing Claude Code, not an official Anthropic product.*

**Ready to give your AI perfect memory?** Install now and never solve the same problem twice!