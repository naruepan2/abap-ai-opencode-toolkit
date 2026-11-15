# tool-snapshot plugin

An OpenCode server plugin that writes the live tool catalog into the workspace:

- `registries/tools-snapshot.json` — total and namespace counts
- `registries/tools-full.json` — one row per tool (`id`, `name`, `namespace`, `description`)

It runs at plugin load (after a short delay so MCP servers can connect), every
10 minutes, and when an `mcp.*`, `tool.*`, or `session.*` event arrives
(debounced, at most once per minute).

## Why

The registry scanner runs in Python and cannot call MCP tools. The plugin runs in
the OpenCode server and can call `ctx.tool.list()`, so this is the bridge between
the live catalog and the repo.

## Load

Add the plugin directory to the global `opencode.json`:

```jsonc
{
  "plugins": [
    {
      "package": "D:/path/to/abap-ai-opencode-toolkit/plugins/tool-snapshot",
      "options": {
        "workspace": "D:/path/to/abap-ai-opencode-toolkit"
      }
    }
  ]
}
```

The plugin only writes inside `<workspace>/registries/`. It never enables or
disables an MCP server.
