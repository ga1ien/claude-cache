# Claude Cache

Superseded by [Watchtower](https://github.com/braintied/watchtower).

Claude Cache was the first cut of session intelligence: a local
Python tool that read Claude Code logs into SQLite and tried to
label successes and failures. New work is Watchtower.

## Watchtower

Watchtower records what your coding agents tried, which of those
attempts failed, and the error that came back, so the next session
does not repeat the same approach.

It does not call a model. It does not care which model wrote the
turns. You run the capture client on hardware you control. It is
not Braintied's Fly app and not Braintied's database. The hook
refuses `ora-watchtower.fly.dev`.

- Code: [github.com/braintied/watchtower](https://github.com/braintied/watchtower)
- Humans: [README](https://github.com/braintied/watchtower/blob/main/README.md)
- Agents: [AGENTS.md](https://github.com/braintied/watchtower/blob/main/AGENTS.md)
- Consulting: [braintied.com/consulting](https://www.braintied.com/consulting)

## This repository

The code here stays as history. Do not `pip install claude-cache`.
Do not add features here. Do not open pull requests against this
tree expecting them to ship.

If you still have `~/.claude/knowledge/cache.db` from an old
install, that file is yours. Watchtower does not read it.

MIT. Not an Anthropic product.
