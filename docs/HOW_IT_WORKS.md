# 🧠 How Claude Cache Works

**Claude Cache v0.6.0 operates in three distinct modes, each building on the previous one's capabilities.**

## Three Usage Modes

### 🔧 Basic Mode
- **Installation**: `pip install claude-cache`
- **Features**: CLI tools, TF-IDF search, CLAUDE.md generation
- **Best for**: Getting started, works everywhere

### ⚡ Enhanced Mode
- **Installation**: `pip install claude-cache[enhanced]`
- **Features**: All Basic + semantic vector search with sentence-transformers
- **Best for**: 2x better pattern matching, context understanding

### 🚀 MCP Mode
- **Installation**: `pip install claude-cache[mcp]`
- **Features**: All Enhanced + native Claude Code tools via MCP
- **Best for**: Ultimate experience, zero context switching

## The Big Picture

### Traditional Mode (Basic/Enhanced)
```
┌──────────────────────────────────────────────────────────────┐
│  YOU CODE WITH CLAUDE IN CLAUDE CODE                        │
│  "Fix the authentication bug"                               │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  CLAUDE CACHE MONITORS LOGS (Background Process)            │
│  🔍 Detects: "Auth bug fixed successfully!"                 │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  UPDATES .claude/CLAUDE.md IN YOUR PROJECT                  │
│  "✓ Authentication: Use JWT refresh pattern"                │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  NEXT TIME: Claude reads CLAUDE.md automatically            │
│  Claude: "I see we fixed auth before with JWT refresh..."   │
└──────────────────────────────────────────────────────────────┘
```

### MCP Mode (Revolutionary)
```
┌──────────────────────────────────────────────────────────────┐
│  YOU CODE WITH CLAUDE IN CLAUDE CODE                        │
│  "Fix the authentication bug"                               │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  TYPE: /mcp__claude-cache__query authentication             │
│  💡 Instant results appear in Claude Code                   │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  WHEN IT WORKS: /mcp__claude-cache__learn                   │
│  🎯 "JWT refresh pattern working perfectly"                 │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  ZERO CONTEXT SWITCH - Everything in Claude Code!          │
│  ⚡ Millisecond response times                               │
└──────────────────────────────────────────────────────────────┘
```

## Step-by-Step Process

### 1️⃣ **You Use Claude Code Normally**
```
You → Claude: "Help me add user login"
Claude → Writes code → You test it → It works! ✅
```

### 2️⃣ **Claude Code Logs Everything**
```json
// ~/.claude/projects/your-app/session-001.jsonl
{"type": "user_message", "content": "Help me add user login"}
{"type": "tool_call", "tool": "Edit", "file": "auth.js", "success": true}
{"type": "assistant_message", "content": "Login implemented"}
{"type": "user_message", "content": "Perfect! It works!"}
```

### 3️⃣ **Claude Cache Analyzes Logs**
```python
# Claude Cache detects:
- ✅ User said "Perfect" (satisfaction)
- ✅ No errors occurred
- ✅ Files were edited successfully
- ✅ Task completed
Score: 95% - SUCCESSFUL PATTERN!
```

### 4️⃣ **Pattern Saved to Knowledge Base**
```sql
INSERT INTO success_patterns
VALUES (
  project: "your-app",
  request: "Help me add user login",
  solution: "JWT implementation",
  files: ["auth.js", "middleware.js"],
  score: 0.95
)
```

### 5️⃣ **Context File Updated**
```markdown
# .claude/CLAUDE.md (Auto-generated)

## Successful Patterns for your-app

### User Authentication
- **Request**: "Help me add user login"
- **Solution**: JWT with middleware
- **Files**: auth.js, middleware.js
- **Success Rate**: 95%
```

### 6️⃣ **Claude Reads Context Automatically**
```
Next conversation:
You → Claude: "Add logout functionality"
Claude → [Reads CLAUDE.md automatically]
Claude → "I'll add logout to the JWT auth system we set up in auth.js..."
```

## 🔑 Key Components by Mode

### **Basic Mode Components**
- **CLI Interface**: Terminal commands for query, stats, browse
- **TF-IDF Search**: Fast keyword-based pattern matching
- **CLAUDE.md Generation**: Automatic context file creation
- **SQLite Database**: Local pattern storage

### **Enhanced Mode Components** (Adds)
- **Semantic Search**: sentence-transformers for context understanding
- **Vector Embeddings**: 384-dimensional semantic similarity
- **Hybrid Search**: Automatic fallback to TF-IDF if needed
- **2x Better Accuracy**: Finds relevant patterns even with different keywords

### **MCP Mode Components** (Adds)
- **MCP Server**: Native Claude Code integration via stdio
- **5 Native Tools**: query, learn, suggest, stats, browse
- **Real-time Communication**: Direct tool access in Claude Code
- **Zero Context Switch**: No copy/paste or terminal switching
- **Proactive Suggestions**: Claude recommends patterns automatically

### **Universal Components** (All Modes)
- **Log Watcher**: Monitors Claude Code session logs
- **Success Detector**: Identifies successful patterns
- **Knowledge Base**: SQLite database with pattern storage
- **Context Injector**: Creates/updates CLAUDE.md files

## 🎯 Success Detection Algorithm

```python
def is_successful(session):
    score = 0

    # Check multiple indicators
    if "error" not in session:
        score += 0.25
    if user_said_thanks(session):
        score += 0.30
    if tests_passed(session):
        score += 0.25
    if files_edited_successfully(session):
        score += 0.20

    return score > 0.70  # 70% threshold
```

## 📊 What Gets Tracked (All Modes)

### **Successful Patterns**
- What you asked for
- How Claude solved it
- Which files were involved
- What approach worked
- Success scores and metrics

### **Project Conventions**
- Import styles
- Naming patterns
- File organization
- Common dependencies
- Technology stack preferences

### **Documentation Content** (MCP browse tool)
- Ingested web documentation
- Best practices from URLs
- API references
- Tutorial content

### **Real-time Learning** (MCP learn tool)
- Manually saved successful solutions
- Categorized patterns
- Code snippets that work
- Problem-solution mappings

## 🔄 The Feedback Loop

```
Better Patterns → Better Context → Better Claude Responses →
More Success → More Patterns → Even Better Context → ...
```

The more you use Claude Code, the smarter Claude Cache makes it!

## 🎮 Interactive Features

### **Real-time Updates**
- Context updates every 30 seconds when new patterns found
- No restart needed

### **Progress Tracking**
```bash
cache stats
# Shows: patterns found, success rate, trending up/down
```

### **Pattern Search**
```bash
cache query "authentication"
# Returns: All successful auth patterns
```

## 🚀 Why This Makes Claude Better

### **Basic Mode Benefits:**
- Claude remembers YOUR successful patterns via CLAUDE.md
- Suggests proven solutions first
- Understands your project structure
- Fast TF-IDF keyword search

### **Enhanced Mode Benefits:**
- All Basic benefits PLUS semantic understanding
- "auth bug" finds JWT solutions even without exact keywords
- Context-aware pattern matching
- 2x better accuracy in finding relevant patterns

### **MCP Mode Benefits:**
- All Enhanced benefits PLUS native tool integration
- Zero context switching - everything in Claude Code
- Proactive pattern suggestions based on your work
- Real-time learning with instant tool access
- Millisecond response times for pattern queries

## 📈 Learning Curve by Mode

### **Basic Mode Growth**
```
Day 1:   📊 5 patterns   → "Getting started"
Week 1:  📊 50 patterns  → "Building knowledge"
Month 1: 📊 200 patterns → "Claude knows your style"
```

### **Enhanced Mode Growth**
```
Day 1:   📊 5 patterns   → "Semantic search active"
Week 1:  📊 50 patterns  → "Context understanding"
Month 1: 📊 200 patterns → "2x better pattern matching"
```

### **MCP Mode Growth**
```
Day 1:   📊 5 patterns   → "Native tools available"
Week 1:  📊 50 patterns  → "Proactive suggestions"
Month 1: 📊 200 patterns → "Like a team member with instant memory!"
```

**All modes**: The more you use Claude Code, the smarter your experience becomes!

## 🔧 Technical Details by Mode

### **Basic Mode Architecture**
- **CLI Interface**: Click-based terminal commands
- **TF-IDF Search**: scikit-learn vectorization
- **SQLite Storage**: Local database for patterns
- **CLAUDE.md Generation**: Automatic context file updates

### **Enhanced Mode Architecture** (Adds)
- **Sentence Transformers**: all-MiniLM-L6-v2 model
- **Vector Embeddings**: 384-dimensional semantic space
- **Hybrid Search**: Automatic fallback mechanism
- **Cosine Similarity**: Semantic pattern matching

### **MCP Mode Architecture** (Adds)
- **MCP Server**: stdio transport for Claude Code
- **Async Tools**: Real-time response handling
- **Native Integration**: Direct tool access in Claude
- **JSON Schema**: Structured tool definitions

### **Universal Architecture** (All Modes)
- **Incremental Processing**: Only new log entries
- **Tech Stack Detection**: React, Vue, Python auto-detection
- **Background Monitoring**: Efficient resource usage
- **Cross-Project Intelligence**: Pattern sharing between projects

---

**The Bottom Line**: Claude Cache v0.6.0 offers three ways to give Claude memory:

- **Basic**: Solid foundation with CLI and automatic CLAUDE.md
- **Enhanced**: 2x better with semantic understanding
- **MCP**: Revolutionary native integration with zero context switching

Choose your mode based on your needs - all make Claude exponentially more helpful over time!