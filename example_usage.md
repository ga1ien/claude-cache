# Claude Cache - Example Usage

## Quick Start

### 1. Install the Tool

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-cache.git
cd claude-cache

# Run the quick start script
./quickstart.sh

# Or install manually
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 2. Start Monitoring

```bash
# Start monitoring Claude Code logs in real-time
cache start
```

The tool will:
- Process all existing Claude Code logs
- Generate slash commands for each project
- Start monitoring for new log entries
- Update patterns as you use Claude Code

### 3. Use Claude Code Normally

Continue using Claude Code as you normally would. Claude Cache runs in the background, learning from your interactions.

### 4. Access Your Patterns

In Claude Code, use the generated slash commands:

```
/project-context implement user authentication
```

This loads relevant successful patterns from similar past tasks.

## Common Workflows

### Processing Existing Logs Only

```bash
# Process logs without continuous monitoring
cache process
```

### Querying Your Knowledge Base

```bash
# Search for patterns related to a topic
cache query "fix authentication bug"

# Filter by project
cache query "database migration" --project my-app
```

### Viewing Statistics

```bash
# Overall statistics
cache stats

# Project-specific statistics
cache stats --project my-app
```

### Generating Commands for a Project

```bash
# Generate all slash commands for a specific project
cache generate --project my-app
```

This creates:
- `/project-context` - Context for specific tasks
- `/best-practices` - Most successful approaches
- `/conventions` - Project conventions
- `/quick-ref` - Frequently used files
- `/debug-helper` - Debugging assistance

### Exporting and Sharing Patterns

```bash
# Export patterns for backup or sharing
cache export my-patterns.json --project my-app

# Import patterns from a teammate
cache import team-patterns.json
```

### Getting Context for a Specific Task

```bash
# Generate context for a request
cache context "implement stripe payments" --project ecommerce
```

## Example Output

When you run `cache start`, you'll see:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Claude Cache                    ┃
┃ Learning from your Claude Code  ┃
┃ interactions                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Processing existing logs...
  Processing: my-project/session-001.jsonl
  Processing: my-project/session-002.jsonl
✓ Found 5 successful patterns in my-project
✓ Generated all commands for my-project
✓ Exported to .claude/CLAUDE.md

Starting real-time monitoring...
✓ Monitoring Claude Code logs in ~/.claude/projects

┌─────────────────────────────────┐
│ Claude Cache - Live             │
├─────────────────┬───────────────┤
│ Metric          │ Value         │
├─────────────────┼───────────────┤
│ Patterns        │ 42            │
│ Projects        │ 3             │
│ Requests        │ 156           │
│ Status          │ ● Monitoring  │
└─────────────────┴───────────────┘
```

## Tips

1. **Let it run in the background** - The more sessions it processes, the better it gets
2. **Check generated commands** - Look in `.claude/commands/` for your slash commands
3. **Review CLAUDE.md** - Check `.claude/CLAUDE.md` for auto-generated documentation
4. **Export regularly** - Back up your patterns with the export command
5. **Share with team** - Export and share successful patterns with teammates

## Troubleshooting

### No logs found
- Make sure you've used Claude Code at least once
- Check that `~/.claude/projects/` exists
- Try running Claude Code and then `cache process`

### Commands not appearing
- Ensure you have successful patterns (check with `cache stats`)
- Manually generate with `cache generate --project [name]`
- Check `.claude/commands/` directory

### Database issues
- Use `cache rebuild --confirm` to rebuild from scratch
- Check permissions on `~/.claude/knowledge/`