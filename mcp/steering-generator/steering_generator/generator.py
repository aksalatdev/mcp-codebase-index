"""Steering document generator with deep analysis support.

Generates foundational steering files like Kiro IDE:
- product.md - Product overview, target users, key features, business objectives
- tech.md - Technology stack, frameworks, libraries, dev tools, constraints
- structure.md - File organization, naming conventions, import patterns, architecture

Supports inclusion modes:
- always (default) - Loaded into every interaction
- fileMatch - Conditional based on file pattern
- manual - On-demand via #steering-file-name

Supports file references: #[[file:<relative_file_name>]]
"""
from typing import Any, Literal

OutputFormat = Literal["kiro", "cursor", "copilot", "windsurf", "cline", "aider", "markdown"]
InclusionMode = Literal["always", "fileMatch", "manual"]

# IDE-specific file locations and formats
IDE_CONFIGS = {
    "kiro": {
        "path": ".kiro/steering/",
        "multiple_files": True,
        "description": "Kiro IDE - Multiple .md files in .kiro/steering/",
        "files": ["product.md", "tech.md", "structure.md"],
    },
    "cursor": {
        "path": ".cursor/rules/",
        "filename": "project.mdc",
        "multiple_files": False,
        "description": "Cursor IDE - .cursor/rules/*.mdc",
    },
    "copilot": {
        "path": ".github/",
        "filename": "copilot-instructions.md",
        "multiple_files": False,
        "description": "GitHub Copilot - .github/copilot-instructions.md",
    },
    "windsurf": {
        "path": "",
        "filename": ".windsurfrules",
        "multiple_files": False,
        "description": "Windsurf/Codeium - .windsurfrules in root",
    },
    "cline": {
        "path": "",
        "filename": ".clinerules",
        "multiple_files": False,
        "description": "Cline - .clinerules in root",
    },
    "aider": {
        "path": "",
        "filename": "CONVENTIONS.md",
        "multiple_files": False,
        "description": "Aider - CONVENTIONS.md",
    },
    "markdown": {
        "path": "",
        "filename": "STEERING.md",
        "multiple_files": False,
        "description": "Generic markdown - Single STEERING.md file",
    },
}

FRAMEWORK_NAMES = {
    "nextjs": "Next.js 15 (App Router)",
    "nextjs-pages": "Next.js 15 (Pages Router)",
    "laravel": "Laravel 12",
    "react": "React 19 (Vite)",
    "vue": "Vue.js 3 (Vite)",
    "nuxt": "Nuxt 3",
}


def generate_tech_md(deep_analysis: dict[str, Any]) -> str:
    """Generate tech.md - Technology stack documentation.
    
    Documents chosen frameworks, libraries, development tools, and technical constraints.
    When AI suggests implementations, it will prefer established stack over alternatives.
    """
    framework = deep_analysis.get("framework", "unknown")
    categorized = deep_analysis.get("categorizedDependencies", {}) or deep_analysis.get("categorizedDeps", {})
    patterns = deep_analysis.get("architecturePatterns", {})
    scripts = deep_analysis.get("scripts", {})
    env_vars = deep_analysis.get("envVars", [])
    
    lines = ["# Technology Stack\n"]
    lines.append("This document defines the technology choices for this project. ")
    lines.append("Use these technologies when generating code and suggestions.\n")
    
    # Framework & Runtime
    lines.append("## Framework & Runtime\n")
    lines.append(f"- **Framework**: {FRAMEWORK_NAMES.get(framework, framework)}")
    if framework in ["nextjs", "nextjs-pages", "react"]:
        lines.append("- **UI Library**: React 19")
        lines.append("- **Language**: TypeScript 5")
        lines.append("- **Runtime**: Node.js 20+")
    elif framework in ["vue", "nuxt"]:
        lines.append("- **UI Library**: Vue 3 (Composition API)")
        lines.append("- **Language**: TypeScript 5")
        lines.append("- **Runtime**: Node.js 20+")
    elif framework == "laravel":
        lines.append("- **Language**: PHP 8.2+")
        lines.append("- **Runtime**: PHP-FPM / Laravel Octane")
    lines.append("")
    
    # Database & Backend
    if categorized.get("Database"):
        lines.append("## Database & Backend\n")
        for dep in categorized["Database"]:
            purpose = dep.get("purpose", "")
            name = dep.get("name", "")
            if "supabase" in name.lower():
                lines.append("- **Database**: Supabase (PostgreSQL)")
                lines.append("- **Auth**: Supabase Auth")
                lines.append("- **Storage**: Supabase Storage")
            elif "prisma" in name.lower():
                lines.append("- **ORM**: Prisma")
            elif "drizzle" in name.lower():
                lines.append("- **ORM**: Drizzle ORM")
            elif purpose:
                lines.append(f"- {purpose}")
        lines.append("")
    
    # UI & Styling
    if categorized.get("UI & Styling"):
        lines.append("## UI & Styling\n")
        
        has_tailwind = any("tailwind" in d["name"].lower() for d in categorized["UI & Styling"])
        radix_count = sum(1 for d in categorized["UI & Styling"] if "@radix-ui" in d["name"])
        
        if has_tailwind:
            lines.append("- **CSS Framework**: Tailwind CSS (utility-first)")
        
        if radix_count > 5 and has_tailwind:
            lines.append("- **Component Library**: shadcn/ui (built on Radix UI)")
        elif radix_count > 0:
            lines.append("- **UI Primitives**: Radix UI")
        
        for dep in categorized["UI & Styling"]:
            if dep["name"] == "lucide-react":
                lines.append("- **Icons**: Lucide React")
            elif dep["name"] == "@heroicons/react":
                lines.append("- **Icons**: Heroicons")
        
        if categorized.get("Other"):
            for dep in categorized["Other"]:
                if dep["name"] == "geist":
                    lines.append("- **Font**: Geist font family")
        
        lines.append("")
    
    # Key Libraries
    key_libs = []
    
    if categorized.get("Forms"):
        for dep in categorized["Forms"]:
            name = dep["name"].split("/")[-1]
            if name == "zod":
                key_libs.append("**Validation**: Zod (schema validation)")
            elif "react-hook-form" in dep["name"]:
                key_libs.append("**Forms**: React Hook Form")
    
    if categorized.get("State"):
        for dep in categorized["State"]:
            name = dep["name"]
            if name == "zustand":
                key_libs.append("**State Management**: Zustand")
            elif name == "jotai":
                key_libs.append("**State Management**: Jotai (atomic)")
            elif "@reduxjs/toolkit" in name:
                key_libs.append("**State Management**: Redux Toolkit")
    
    if categorized.get("Data Fetching"):
        for dep in categorized["Data Fetching"]:
            name = dep["name"]
            if "@tanstack/react-query" in name:
                key_libs.append("**Data Fetching**: TanStack Query")
            elif name == "swr":
                key_libs.append("**Data Fetching**: SWR")
    
    if categorized.get("Utilities"):
        for dep in categorized["Utilities"]:
            name = dep["name"]
            if name == "date-fns":
                key_libs.append("**Date Utilities**: date-fns")
            elif name == "dayjs":
                key_libs.append("**Date Utilities**: Day.js")
    
    if categorized.get("Charts"):
        for dep in categorized["Charts"]:
            key_libs.append(f"**Charts**: {dep['name']}")
    
    if categorized.get("Notifications"):
        for dep in categorized["Notifications"]:
            if dep["name"] == "sonner":
                key_libs.append("**Notifications**: Sonner (toast)")
            else:
                key_libs.append(f"**Notifications**: {dep['name']}")
    
    if categorized.get("Theme"):
        for dep in categorized["Theme"]:
            if dep["name"] == "next-themes":
                key_libs.append("**Theming**: next-themes")
    
    if key_libs:
        lines.append("## Key Libraries\n")
        for lib in key_libs:
            lines.append(f"- {lib}")
        lines.append("")
    
    # Development Commands
    if scripts:
        lines.append("## Development Commands\n")
        lines.append("```bash")
        if "dev" in scripts:
            lines.append("npm run dev       # Start development server")
        if "build" in scripts:
            lines.append("npm run build     # Build for production")
        if "start" in scripts:
            lines.append("npm run start     # Start production server")
        if "lint" in scripts:
            lines.append("npm run lint      # Run linter")
        if "test" in scripts:
            lines.append("npm run test      # Run tests")
        lines.append("```\n")
    
    # Environment Variables
    if env_vars:
        lines.append("## Environment Variables\n")
        lines.append("Required environment variables (`.env.local`):\n")
        lines.append("| Variable | Description |")
        lines.append("|----------|-------------|")
        for var in env_vars:
            desc = _get_env_var_description(var)
            lines.append(f"| `{var}` | {desc} |")
        lines.append("")
    
    # Technical Constraints
    lines.append("## Technical Constraints\n")
    lines.append("When generating code, follow these constraints:\n")
    if framework in ["nextjs", "nextjs-pages"]:
        lines.append("- Use Server Components by default, Client Components only when needed")
        lines.append("- Prefer Server Actions for mutations")
        lines.append("- Use `next/image` for images, `next/link` for navigation")
    if has_tailwind if 'has_tailwind' in dir() else False:
        lines.append("- Use Tailwind CSS classes, avoid inline styles")
    lines.append("- Follow TypeScript strict mode")
    lines.append("")
    
    return "\n".join(lines)


def _get_env_var_description(var: str) -> str:
    """Get description for common environment variables."""
    descriptions = {
        "DATABASE_URL": "Database connection string",
        "NEXT_PUBLIC_SUPABASE_URL": "Supabase project URL",
        "NEXT_PUBLIC_SUPABASE_ANON_KEY": "Supabase anonymous key (public)",
        "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key (server-only)",
        "NEXTAUTH_SECRET": "NextAuth.js secret",
        "NEXTAUTH_URL": "NextAuth.js URL",
        "OPENAI_API_KEY": "OpenAI API key",
        "STRIPE_SECRET_KEY": "Stripe secret key",
        "STRIPE_PUBLISHABLE_KEY": "Stripe publishable key",
    }
    
    # Check exact match first
    if var in descriptions:
        return descriptions[var]
    
    # Pattern matching
    var_upper = var.upper()
    if "SUPABASE" in var_upper and "URL" in var_upper:
        return "Supabase project URL"
    elif "SUPABASE" in var_upper and "ANON" in var_upper:
        return "Supabase anonymous key"
    elif "SUPABASE" in var_upper and "SERVICE" in var_upper:
        return "Supabase service role key"
    elif "DATABASE" in var_upper or "DB_" in var_upper:
        return "Database connection"
    elif "API_KEY" in var_upper or "APIKEY" in var_upper:
        return "API key"
    elif "SECRET" in var_upper:
        return "Secret key"
    elif "URL" in var_upper:
        return "Service URL"
    
    return "Required"


def generate_structure_md(deep_analysis: dict[str, Any]) -> str:
    """Generate detailed structure.md with architecture patterns."""
    framework = deep_analysis.get("framework", "unknown")
    patterns = deep_analysis.get("architecturePatterns", {})
    components = deep_analysis.get("components", [])
    
    lines = ["# Project Structure\n"]
    
    # Framework-specific structure
    structures = {
        "nextjs": """```
├── app/                    # Next.js App Router
│   ├── api/               # API routes (Route Handlers)
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Main entry point
│   └── globals.css        # Global styles & Tailwind
│
├── components/            # React components
│   ├── ui/               # shadcn/ui primitives
│   └── *.tsx             # Feature components
│
├── hooks/                 # Custom React hooks
│
├── lib/                   # Utilities and core logic
│   ├── types.ts          # TypeScript interfaces
│   └── utils.ts          # Utility functions
│
└── public/               # Static assets
```""",
        "laravel": """```
├── app/
│   ├── Http/
│   │   ├── Controllers/   # Request handlers
│   │   └── Middleware/    # HTTP middleware
│   └── Models/            # Eloquent models
│
├── config/                # Configuration files
│
├── database/
│   └── migrations/        # Database migrations
│
├── resources/views/       # Blade templates
│
├── routes/
│   ├── web.php           # Web routes
│   └── api.php           # API routes
│
└── public/               # Public assets
```""",
        "react": """```
├── src/
│   ├── components/        # React components
│   ├── hooks/            # Custom hooks
│   ├── store/            # State management
│   ├── api/              # API services
│   ├── types/            # TypeScript types
│   └── App.tsx           # Root component
│
├── public/               # Static assets
└── vite.config.ts        # Vite configuration
```""",
        "vue": """```
├── src/
│   ├── components/        # Vue components
│   ├── composables/      # Composition API hooks
│   ├── stores/           # Pinia stores
│   ├── router/           # Vue Router config
│   ├── types/            # TypeScript types
│   └── App.vue           # Root component
│
├── public/               # Static assets
└── vite.config.ts        # Vite configuration
```""",
        "nuxt": """```
├── pages/                 # File-based routing
├── components/            # Auto-imported components
├── composables/          # Auto-imported composables
├── server/
│   └── api/              # Server API routes
├── public/               # Static assets
└── nuxt.config.ts        # Nuxt configuration
```""",
    }
    
    lines.append(structures.get(framework, "```\n# Project structure\n```"))
    lines.append("")
    
    # Architecture Patterns
    if any(patterns.values()):
        lines.append("\n## Architecture Patterns\n")
        
        if patterns.get("stateManagement"):
            lines.append("### State Management")
            lines.append(f"- {patterns['stateManagement']}")
            lines.append("")
        
        if patterns.get("componentPattern"):
            lines.append("### Component Patterns")
            lines.append(f"- {patterns['componentPattern']}")
            lines.append("")
        
        if patterns.get("apiPattern"):
            lines.append("### API Pattern")
            lines.append(f"- {patterns['apiPattern']}")
            lines.append("")
        
        if patterns.get("styling"):
            lines.append("### Styling")
            lines.append(f"- {patterns['styling']}")
            lines.append("")
    
    return "\n".join(lines)


def generate_product_md(deep_analysis: dict[str, Any]) -> str:
    """Generate product.md from README and entities."""
    readme = deep_analysis.get("readme", {})
    entities = deep_analysis.get("entities", [])
    
    lines = ["# Product Overview\n"]
    
    # From README
    if readme.get("title") and "deploy" not in readme["title"].lower():
        lines.append(f"{readme['title']}\n")
    
    if readme.get("description"):
        lines.append(readme["description"])
        lines.append("")
    
    if readme.get("features"):
        lines.append("## Features\n")
        for feature in readme["features"]:
            lines.append(f"- {feature}")
        lines.append("")
    
    # Core Entities
    if entities:
        lines.append("## Core Entities\n")
        for entity in entities[:6]:
            name = entity.get("name", "")
            desc = entity.get("description", "")
            if name:
                if desc:
                    lines.append(f"- **{name}**: {desc}")
                else:
                    lines.append(f"- **{name}**")
        lines.append("")
    
    return "\n".join(lines)


def generate_business_rules_md(deep_analysis: dict[str, Any]) -> str:
    """Generate business-rules.md from entities and status enums."""
    entities = deep_analysis.get("entities", [])
    status_enums = deep_analysis.get("statusEnums", [])
    
    lines = ["# Business Rules\n"]
    
    # Status/Workflow from enums
    if status_enums:
        lines.append("## Status Values\n")
        for enum in status_enums:
            lines.append(f"### {enum['name']}")
            for value in enum["values"]:
                lines.append(f"- `{value}`")
            lines.append("")
    
    # Entity details
    if entities:
        lines.append("## Data Entities\n")
        for entity in entities[:5]:
            name = entity.get("name", "")
            fields = entity.get("fields", [])
            
            if name and fields:
                lines.append(f"### {name}\n")
                lines.append("| Field | Type | Required |")
                lines.append("|-------|------|----------|")
                for field in fields[:10]:
                    fname = field.get("name", "")
                    ftype = field.get("type", "").split("\n")[0][:30]
                    required = "No" if field.get("optional") else "Yes"
                    lines.append(f"| {fname} | `{ftype}` | {required} |")
                lines.append("")
    
    return "\n".join(lines)


def _wrap_kiro_format(content: str) -> str:
    """Wrap content with Kiro front-matter."""
    return f"""---
inclusion: always
---
{content}"""


def _wrap_cursor_format(content: str, description: str) -> str:
    """Wrap content with Cursor MDC front-matter."""
    return f"""---
description: {description}
alwaysApply: true
---
{content}"""


def generate_steering_docs_deep(
    deep_analysis: dict[str, Any],
    output_format: OutputFormat = "kiro"
) -> dict[str, str]:
    """Generate comprehensive steering docs from deep analysis."""
    
    framework = deep_analysis.get("framework", "unknown")
    
    # Generate all docs
    docs = {
        "tech.md": generate_tech_md(deep_analysis),
        "structure.md": generate_structure_md(deep_analysis),
        "product.md": generate_product_md(deep_analysis),
        "business-rules.md": generate_business_rules_md(deep_analysis),
    }
    
    config = IDE_CONFIGS.get(output_format, IDE_CONFIGS["markdown"])
    
    # === KIRO: Multiple files with front-matter ===
    if output_format == "kiro":
        result = {}
        for name, content in docs.items():
            wrapped = _wrap_kiro_format(content)
            result[f"{config['path']}{name}"] = wrapped
        return result
    
    # === Single file formats ===
    combined = "\n\n---\n\n".join(docs.values())
    
    if output_format == "cursor":
        wrapped = _wrap_cursor_format(combined, f"Steering rules for {FRAMEWORK_NAMES.get(framework, framework)} project")
        return {f"{config['path']}{config['filename']}": wrapped}
    
    # All others: plain markdown
    filename = config.get("filename", "STEERING.md")
    path = config.get("path", "")
    return {f"{path}{filename}": combined}


# Keep old function for backward compatibility
def generate_steering_docs(
    analysis: dict[str, Any],
    output_format: OutputFormat = "kiro"
) -> dict[str, str]:
    """Generate steering docs (basic version for backward compatibility)."""
    # If deep analysis data is present, use new generator
    if "categorizedDependencies" in analysis:
        return generate_steering_docs_deep(analysis, output_format)
    
    # Otherwise use simple generation
    from .analyzer import analyze_codebase
    from .deep_analyzer import deep_analyze_codebase
    
    framework = analysis.get("framework", "unknown")
    project_path = analysis.get("projectPath", ".")
    
    # Do deep analysis
    deep = deep_analyze_codebase(project_path, framework, analysis)
    
    # Merge
    deep["framework"] = framework
    deep["scripts"] = analysis.get("scripts", {})
    deep["envVars"] = analysis.get("envVars", [])
    deep["components"] = analysis.get("components", [])
    
    return generate_steering_docs_deep(deep, output_format)


def get_supported_ides() -> dict[str, dict]:
    """Return info about all supported IDEs."""
    return IDE_CONFIGS
