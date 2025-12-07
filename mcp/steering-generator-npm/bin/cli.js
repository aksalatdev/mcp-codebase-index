#!/usr/bin/env node

const { spawn, execSync } = require("child_process");

const PYTHON_PACKAGE = "steering-generator-mcp";

// Check if Python is available
function getPythonCommand() {
  const commands = process.platform === "win32" 
    ? ["python", "python3", "py"] 
    : ["python3", "python"];
  
  for (const cmd of commands) {
    try {
      execSync(`${cmd} --version`, { stdio: "ignore" });
      return cmd;
    } catch {
      continue;
    }
  }
  return null;
}

// Check if package is installed
function isPackageInstalled(pythonCmd) {
  try {
    execSync(`${pythonCmd} -c "import steering_generator"`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

// Install the Python package
function installPackage(pythonCmd) {
  console.error(`[steering-generator-mcp] Installing Python package...`);
  try {
    // Use --user flag to avoid permission issues
    execSync(
      `${pythonCmd} -m pip install ${PYTHON_PACKAGE} --user --quiet --disable-pip-version-check`,
      { stdio: "inherit" }
    );
    console.error(`[steering-generator-mcp] Installation complete!`);
    return true;
  } catch {
    // Try without --user if it fails
    try {
      execSync(
        `${pythonCmd} -m pip install ${PYTHON_PACKAGE} --quiet --disable-pip-version-check`,
        { stdio: "inherit" }
      );
      console.error(`[steering-generator-mcp] Installation complete!`);
      return true;
    } catch (error) {
      console.error(`[steering-generator-mcp] Failed to install. Please run manually:`);
      console.error(`  pip install ${PYTHON_PACKAGE}`);
      return false;
    }
  }
}

// Main
async function main() {
  const pythonCmd = getPythonCommand();

  if (!pythonCmd) {
    console.error("[steering-generator-mcp] Error: Python not found!");
    console.error("Please install Python 3.10+ from https://python.org");
    process.exit(1);
  }

  // Auto-install if not present
  if (!isPackageInstalled(pythonCmd)) {
    if (!installPackage(pythonCmd)) {
      process.exit(1);
    }
  }

  // Run the MCP server
  const server = spawn(pythonCmd, ["-m", "steering_generator"], {
    stdio: "inherit",
  });

  server.on("error", (err) => {
    console.error(`[steering-generator-mcp] Error: ${err.message}`);
    process.exit(1);
  });

  server.on("close", (code) => {
    process.exit(code || 0);
  });
}

main();
