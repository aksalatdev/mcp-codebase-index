# steering-generator-mcp

[![npm version](https://badge.fury.io/js/steering-generator-mcp.svg)](https://www.npmjs.com/package/steering-generator-mcp)

MCP Server to auto-generate steering/context docs from codebases — like Kiro IDE's built-in feature, but for **all AI IDEs**.

## Quick Install

Just add to your MCP config:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "npx",
      "args": ["-y", "steering-generator-mcp"],
      "type": "stdio"
    }
  }
}
```

That's it! The Python package will be auto-installed on first run.

## Config File Locations

| IDE | Config File |
|-----|-------------|
| **Kiro** | `.kiro/settings/mcp.json` |
| **Cursor** | `.cursor/mcp.json` |
| **VS Code** | `.vscode/mcp.json` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **Claude Desktop** | `claude_desktop_config.json` |
| **Cline** | Cline MCP settings |

## Usage

Chat with your AI:

```
"Generate steering docs for this project"
```

## Requirements

- Node.js 16+
- Python 3.10+ (auto-detected)

## What It Generates

| File | Purpose |
|------|---------|
| `product.md` | Product overview, features, business objectives |
| `tech.md` | Technology stack, frameworks, libraries |
| `structure.md` | File organization, naming conventions |

## Supported Frameworks

- Next.js (App Router & Pages)
- React (Vite/CRA)
- Vue.js / Nuxt.js
- Laravel

## License

MIT
