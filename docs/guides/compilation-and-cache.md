---
title: Compilation and Cache
---

# Compilation and Cache

Playbooks compiles `.pb` files to PBASM. It caches results next to the source in `.pbasm_cache/`.

## Compile

```bash
playbooks compile program.pb --output program.pbasm
```

## Cache

- Location: `.pbasm_cache/<name>.playbooks-<version>.pbasm`
- Valid when newer than the source and the compiler prompt template
- Safe to delete to force recompilation (e.g., when switching between different LLMs)
- Compiled files can be run directly and will not be re-compiled
```bash
playbooks run program.pbasm
```

See also: [Environment Variables](environment-variables.md)

