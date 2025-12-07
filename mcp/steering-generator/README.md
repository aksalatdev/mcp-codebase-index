# Steering Generator MCP Server

MCP Server untuk auto-generate steering/context docs dari codebase. Bikin AI lebih paham project lo!

## Apa Ini?

MCP ini scan codebase lo, extract info penting (tech stack, types, routes, dll), terus generate "steering docs" yang bisa dibaca AI. Hasilnya: AI jadi lebih akurat karena udah paham context project.

## Supported Frameworks

- Next.js (App Router & Pages)
- Laravel 12
- React (Vite/CRA)
- Vue.js (Vite)
- Nuxt.js

## Supported IDEs / Output Formats

| IDE | Output File | Format |
|-----|-------------|--------|
| **Kiro** | `.kiro/steering/*.md` | Multiple files |
| **Cursor** | `.cursor/rules/project.mdc` | Single file |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Single file |
| **Windsurf** | `.windsurfrules` | Single file |
| **Cline** | `.clinerules` | Single file |
| **Aider** | `CONVENTIONS.md` | Single file |
| **Generic** | `STEERING.md` | Single file |

---

## Installation

### Prerequisites

- Python 3.10+
- pip atau uv

### Option 1: Install dari Source (Development)

```bash
# Clone/download folder mcp/steering-generator

# Masuk ke folder
cd mcp/steering-generator

# Install dalam editable mode
pip install -e .

# Test run
steering-generator
```

### Option 2: Install via pip (kalau udah publish ke PyPI)

```bash
pip install steering-generator-mcp
```

### Option 3: Run langsung tanpa install

```bash
cd mcp/steering-generator
python -m steering_generator
```

### Optional: Install Ripgrep (Recommended untuk codebase besar)

Ripgrep bikin scanning 10x lebih cepat.

**Windows:**
```bash
# Via Chocolatey
choco install ripgrep

# Via Scoop
scoop install ripgrep

# Via Winget
winget install BurntSushi.ripgrep
```

**Mac:**
```bash
brew install ripgrep
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install ripgrep

# Arch
sudo pacman -S ripgrep
```

---

## MCP Configuration

### Kiro IDE

Edit `.kiro/settings/mcp.json` atau `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "C:/path/to/mcp/steering-generator"
    }
  }
}
```

### Cursor IDE

Edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "/path/to/mcp/steering-generator"
    }
  }
}
```

### Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "/path/to/mcp/steering-generator"
    }
  }
}
```

---

## Tools Available

### `detect_project_framework`
Detect framework dari project directory.

```
Input:  { "project_path": "C:/projects/my-app" }
Output: { "framework": "nextjs", "supported": true }
```

### `analyze_project`
Analyze codebase dan return structured data.

```
Input:  { "project_path": "C:/projects/my-app" }
Output: {
  "framework": "nextjs",
  "techStack": { "dependencies": ["next", "react", ...] },
  "types": [...],
  "components": [...],
  "stats": { "filesScanned": 45, "ripgrepAvailable": true }
}
```

### `generate_steering`
Generate steering docs untuk IDE tertentu.

```
Input:  { 
  "project_path": "C:/projects/my-app",
  "output_format": "cursor"  // kiro, cursor, copilot, windsurf, cline, aider, markdown
}
Output: {
  "framework": "nextjs",
  "files": {
    ".cursor/rules/project.mdc": "---\ndescription: ...\n---\n# Tech Stack\n..."
  }
}
```

### `list_supported_frameworks`
List semua framework yang di-support.

### `list_supported_ides`
List semua IDE dan format output yang di-support.

---

## Example Workflow

### Di Chat AI:

```
User: "Generate steering docs untuk project gw"

AI: *calls detect_project_framework(project_path=".")*
    → Detected: Next.js

AI: *calls generate_steering(project_path=".", output_format="kiro")*
    → Generated 3 files

AI: "Done! Gw udah generate steering docs:
     - .kiro/steering/tech.md
     - .kiro/steering/structure.md  
     - .kiro/steering/entities.md"
```

### Output Files akan berisi:

```markdown
# Tech Stack

## Framework
- Next.js (App Router)

## Key Dependencies
- `next`
- `react`
- `@supabase/ssr`
- `tailwindcss`
...
```

---

## Performance

| Codebase Size | Tanpa Ripgrep | Dengan Ripgrep |
|---------------|---------------|----------------|
| Small (<100 files) | ~1s | ~0.5s |
| Medium (100-1000 files) | ~5s | ~1s |
| Large (1000+ files) | ~30s+ | ~3s |

**Tips:** Install ripgrep untuk codebase besar!

---

## Troubleshooting

### "Module not found"
```bash
# Pastikan install dulu
pip install -e .
```

### "Permission denied" (Windows)
```bash
# Run as Administrator atau pake virtual env
python -m venv venv
venv\Scripts\activate
pip install -e .
```

### MCP gak connect
- Pastikan path di config benar (absolute path)
- Restart IDE setelah edit config
- Check Python ada di PATH

---

## License

MIT
