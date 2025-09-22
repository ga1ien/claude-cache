# 📦 Claude Cache Installation Guide

## Three Ways to Use Claude Cache

Claude Cache offers **three distinct usage modes**, each building on the previous one's capabilities:

| Mode | Installation | Features | Best For |
|------|-------------|----------|-----------|
| **Basic** | `pip install claude-cache` | CLI tools, keyword search | Getting started |
| **Enhanced** | `pip install claude-cache[enhanced]` | Semantic search, 2x better accuracy | Power users |
| **MCP** | `pip install claude-cache[mcp]` | Native Claude Code tools | Ultimate experience |

---

## 🚀 Mode 1: Basic Installation

### Install
```bash
pip install claude-cache
```

### Features
- ✅ All CLI commands (`cache start`, `cache query`, `cache browse`)
- ✅ Pattern learning and storage
- ✅ Documentation ingestion
- ✅ CLAUDE.md auto-generation
- ✅ TF-IDF keyword search
- ✅ Cross-project intelligence

### Usage
```bash
# Start monitoring (keep terminal open)
cache start

# Query patterns
cache query "authentication"

# Browse documentation
cache browse https://docs.example.com

# Get statistics
cache stats
```

### Perfect For
- Developers starting with Claude Cache
- Simple keyword-based pattern matching
- All core functionality without dependencies

---

## ⚡ Mode 2: Enhanced Installation

### Install
```bash
pip install claude-cache[enhanced]
```

### Additional Features
- ✅ **Semantic Vector Search** (understands context + meaning)
- ✅ **2x Better Pattern Matching** (finds relevant patterns even with different keywords)
- ✅ **Context Understanding** ("auth bug" finds JWT solutions)
- ✅ **Smarter Suggestions** (AI-powered pattern recommendations)

### Technical Details
- Uses `sentence-transformers` with `all-MiniLM-L6-v2` model
- 384-dimensional embeddings for semantic similarity
- Automatic fallback to TF-IDF if model unavailable
- ~2 second startup time (loads ML model)

### Usage (Same CLI + Better Results)
```bash
# Same commands, smarter results
cache query "authentication"
# Now finds: JWT patterns, OAuth flows, session management

cache query "slow database"
# Now finds: connection pooling, query optimization, caching patterns
```

### Perfect For
- Developers who want the best pattern matching
- Projects with large knowledge bases
- When keyword search isn't enough

---

## 🎯 Mode 3: MCP Installation (Recommended)

### Install
```bash
pip install claude-cache[mcp]
```
*Includes both enhanced search AND MCP tools*

### Revolutionary Features
- ✅ **Native Claude Code Integration** (no context switching)
- ✅ **Instant Tool Access** (type `/` in Claude Code)
- ✅ **Proactive Suggestions** (Claude suggests patterns automatically)
- ✅ **Zero Copy/Paste** (results appear directly in Claude)
- ✅ **Real-time Learning** (save patterns with one command)

### Setup (One-Time)

1. **Add to your project's `.claude.json`:**
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

2. **Or add globally to `~/.claude/claude_desktop_config.json`:**
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

3. **Restart Claude Code**

### Available Tools

#### `/mcp__cache__query`
🔍 **Instant Vector Search**
```
Arguments:
- query: "authentication JWT"
- project: (optional) specific project
- limit: max results (default: 5)
```

#### `/mcp__cache__learn`
💾 **Save Success Patterns**
```
Arguments:
- description: "JWT refresh token rotation"
- category: "authentication"
- code_snippet: (optional) working code
```

#### `/mcp__cache__suggest`
💡 **Proactive Recommendations**
```
Arguments:
- context: current code you're working on
- intent: what you're trying to accomplish
```

#### `/mcp__cache__stats`
📊 **Knowledge Base Stats**
```
Shows: pattern counts, search mode, project info
```

#### `/mcp__cache__browse`
🌐 **Ingest Documentation**
```
Arguments:
- url: documentation URL to index
- project: (optional) project name
```

### Usage Examples

**Before (Traditional):**
```
1. Code authentication
2. Open terminal
3. Run: cache query "auth"
4. Copy results
5. Paste in Claude
6. Continue coding
```

**After (MCP Mode):**
```
1. Code authentication
2. Type: /mcp__cache__query auth
3. Get instant results in Claude
4. Continue coding (no context switch!)
```

### Perfect For
- Developers using Claude Code as primary IDE
- Teams wanting seamless AI-assisted development
- Maximum productivity and intelligence

---

## 🔧 Advanced Installation Options

### Install Everything
```bash
pip install claude-cache[all]
```
*Gets enhanced search + MCP tools*

### Development Installation
```bash
git clone https://github.com/ga1ien/claude-cache
cd claude-cache
pip install -e .[all]
```

### Verify Installation
```bash
# Check version
cache --version

# Test enhanced search (if installed)
python -c "import sentence_transformers; print('✅ Enhanced search available')"

# Test MCP server (if installed)
cache-mcp --version
```

---

## 📊 Feature Comparison Matrix

| Feature | Basic | Enhanced | MCP |
|---------|-------|----------|-----|
| CLI Commands | ✅ | ✅ | ✅ |
| Pattern Learning | ✅ | ✅ | ✅ |
| Documentation Ingestion | ✅ | ✅ | ✅ |
| TF-IDF Search | ✅ | ✅ | ✅ |
| Semantic Search | ❌ | ✅ | ✅ |
| Context Understanding | ❌ | ✅ | ✅ |
| Claude Code Integration | ❌ | ❌ | ✅ |
| Native Tools | ❌ | ❌ | ✅ |
| Proactive Suggestions | ❌ | ❌ | ✅ |
| Zero Context Switch | ❌ | ❌ | ✅ |

---

## 🚀 Migration Path

### From Basic → Enhanced
```bash
pip install sentence-transformers
# Automatically enables semantic search
```

### From Enhanced → MCP
```bash
pip install mcp
# Add .claude.json configuration
# Restart Claude Code
```

### From Basic → MCP (Direct)
```bash
pip install claude-cache[mcp]
# Configure Claude Code
# Get all features immediately
```

---

## 🔍 Troubleshooting

### Basic Mode Issues
```bash
# If cache command not found
pip install --upgrade claude-cache

# If permission errors
pip install --user claude-cache
```

### Enhanced Mode Issues
```bash
# If semantic search not working
pip install sentence-transformers

# If model download fails
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### MCP Mode Issues
```bash
# If tools don't appear in Claude Code
claude-code --mcp-debug

# Test MCP server directly
cache-mcp

# Check configuration
cat .claude.json
```

---

## 💡 Recommendations

### For New Users
Start with **Basic** → try for a week → upgrade to **Enhanced** → eventually **MCP**

### For Power Users
Go directly to **MCP mode** for the ultimate experience

### For Teams
Use **MCP mode** with shared `.claude.json` configuration

---

## 🎯 Next Steps

1. **Choose your mode** based on needs
2. **Install** using the commands above
3. **Configure** MCP if using Mode 3
4. **Start learning patterns** with `cache start` or `/mcp__cache__learn`
5. **Query intelligence** with `cache query` or `/mcp__cache__query`

**Happy coding with Claude Cache!** 🚀