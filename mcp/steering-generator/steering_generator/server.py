"""FastMCP Server for Steering Generator."""
from fastmcp import FastMCP
from typing import Literal
import json

from .detector import detect_framework, get_important_files, FrameworkType
from .analyzer import analyze_codebase
from .deep_analyzer import deep_analyze_codebase
from .generator import generate_steering_docs, OutputFormat, get_supported_ides, IDE_CONFIGS

mcp = FastMCP(
    name="Steering Generator",
    instructions="""
    This MCP server helps you auto-generate steering/context documentation from codebases.
    
    Supported frameworks: Next.js, Laravel, React, Vue, Nuxt
    
    Workflow:
    1. Call detect_framework with project path to identify the framework
    2. Call analyze_codebase to extract structured data
    3. Call generate_steering to create documentation files
    
    Output formats:
    - kiro: Separate .md files for .kiro/steering/
    - cursor: Single .cursorrules file
    - markdown: Single STEERING.md file
    """
)

@mcp.tool
def detect_project_framework(project_path: str) -> dict:
    """
    Detect the framework used in a project directory.
    
    Args:
        project_path: Absolute or relative path to the project root
        
    Returns:
        Dictionary with detected framework and important files to analyze
    """
    framework = detect_framework(project_path)
    important_files = get_important_files(framework)
    
    return {
        "framework": framework,
        "importantFiles": important_files,
        "supported": framework != "unknown",
    }

@mcp.tool
def analyze_project(project_path: str, framework: str | None = None) -> dict:
    """
    Analyze a codebase and extract structured information.
    
    Args:
        project_path: Absolute or relative path to the project root
        framework: Optional framework override (nextjs, laravel, react, vue, nuxt).
                   If not provided, will auto-detect.
    
    Returns:
        Structured analysis including tech stack, types, routes, models, etc.
    """
    if framework is None:
        framework = detect_framework(project_path)
    
    analysis = analyze_codebase(project_path, framework)
    return analysis

@mcp.tool
def generate_steering(
    project_path: str,
    output_format: str = "kiro",
    framework: str | None = None,
) -> dict:
    """
    Generate steering documentation from a codebase.
    
    Args:
        project_path: Absolute or relative path to the project root
        output_format: Output format - "kiro" (separate files), "cursor" (.cursorrules), 
                       or "markdown" (single file)
        framework: Optional framework override. If not provided, will auto-detect.
    
    Returns:
        Dictionary with filename -> content mappings for generated docs
    """
    if framework is None:
        framework = detect_framework(project_path)
    
    analysis = analyze_codebase(project_path, framework)
    
    # Validate output format
    valid_formats = ["kiro", "cursor", "copilot", "windsurf", "cline", "aider", "markdown"]
    if output_format not in valid_formats:
        output_format = "kiro"
    
    docs = generate_steering_docs(analysis, output_format)
    
    return {
        "framework": framework,
        "outputFormat": output_format,
        "files": docs,
        "analysis": {
            "typesFound": len(analysis.get("types", [])),
            "modelsFound": len(analysis.get("models", [])),
            "routesFound": len(analysis.get("routes", [])),
            "componentsFound": len(analysis.get("components", [])),
            "envVarsFound": len(analysis.get("envVars", [])),
        }
    }

@mcp.tool
def deep_analyze_project(project_path: str, framework: str | None = None) -> dict:
    """
    Perform deep analysis of a codebase for comprehensive context.
    
    This extracts much more detail than analyze_project, including:
    - Categorized dependencies with purposes
    - README/product info
    - Architecture patterns (state management, auth, styling)
    - Key code snippets
    - Detailed entity definitions with fields
    - Status enums and workflows
    
    Use this when you need to generate detailed steering docs like Kiro does.
    
    Args:
        project_path: Absolute or relative path to the project root
        framework: Optional framework override. If not provided, will auto-detect.
    
    Returns:
        Comprehensive analysis with categorized deps, patterns, code snippets, etc.
    """
    if framework is None:
        framework = detect_framework(project_path)
    
    # Get basic analysis first
    basic_analysis = analyze_codebase(project_path, framework)
    
    # Perform deep analysis
    deep_analysis = deep_analyze_codebase(project_path, framework, basic_analysis)
    
    # Merge results
    return {
        "framework": framework,
        "projectPath": basic_analysis.get("projectPath"),
        
        # Basic info
        "scripts": basic_analysis.get("scripts", {}),
        "envVars": basic_analysis.get("envVars", []),
        "components": basic_analysis.get("components", []),
        
        # Deep analysis
        "categorizedDependencies": deep_analysis.get("categorizedDeps", {}),
        "readme": deep_analysis.get("readme", {}),
        "architecturePatterns": deep_analysis.get("patterns", {}),
        "codeSnippets": deep_analysis.get("codeSnippets", {}),
        "entities": deep_analysis.get("entities", []),
        "statusEnums": deep_analysis.get("statusEnums", []),
        
        # Stats
        "stats": basic_analysis.get("stats", {}),
    }


@mcp.tool
def list_supported_frameworks() -> dict:
    """
    List all supported frameworks and their detection signatures.
    
    Returns:
        Dictionary of supported frameworks with detection info
    """
    return {
        "frameworks": [
            {
                "id": "nextjs",
                "name": "Next.js",
                "signatures": ["next.config.js", "next.config.mjs", "next.config.ts"],
            },
            {
                "id": "laravel",
                "name": "Laravel",
                "signatures": ["artisan", "composer.json with laravel/framework"],
            },
            {
                "id": "react",
                "name": "React (Vite/CRA)",
                "signatures": ["vite.config with react plugin", "package.json with react"],
            },
            {
                "id": "vue",
                "name": "Vue.js",
                "signatures": ["vite.config with vue plugin", "package.json with vue"],
            },
            {
                "id": "nuxt",
                "name": "Nuxt.js",
                "signatures": ["nuxt.config.js", "nuxt.config.ts"],
            },
        ]
    }


@mcp.tool
def list_supported_ides() -> dict:
    """
    List all supported IDEs and their steering file formats.
    
    Returns:
        Dictionary of supported IDEs with file path info
    """
    ides = []
    for ide_id, config in IDE_CONFIGS.items():
        ides.append({
            "id": ide_id,
            "description": config["description"],
            "path": config.get("path", "") + config.get("filename", "*.md"),
            "multipleFiles": config.get("multiple_files", False),
        })
    
    return {"ides": ides}

def main():
    """Entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
