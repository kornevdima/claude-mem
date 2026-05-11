#!/usr/bin/env bash
# claude-mem: graphify installer
#
# Installs graphifyy (the Python library powering the graphify-ingest and
# graphify-update skills) into a compatible Python interpreter and pins
# the path so subsequent skill invocations skip the install/detect step.
#
# graphifyy requires Python >=3.10,<3.14.
#
# Usage:
#   bash bin/setup-graphify.sh                      # install globally; report only
#   bash bin/setup-graphify.sh /path/to/project     # install + pin to project
#
# Idempotent — safe to re-run.

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

PROJECT="${1:-}"

echo "claude-mem: graphify installer"
echo

# ── 1. Detect best Python interpreter ─────────────────────────────────────────
# Priority: uv tool > pipx > pyenv-managed > system python3
# Required: >=3.10, <3.14

PYTHON=""

# Check if a python is at the right version
check_version() {
    local py="$1"
    if ! command -v "$py" >/dev/null 2>&1 && [ ! -x "$py" ]; then
        return 1
    fi
    "$py" -c '
import sys
ok = sys.version_info >= (3, 10) and sys.version_info < (3, 14)
sys.exit(0 if ok else 1)
' 2>/dev/null
}

# Try common candidates in order
for cand in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if check_version "$cand"; then
        PYTHON=$(command -v "$cand")
        echo -e "${GREEN}✓${NC} Found compatible Python: $PYTHON"
        "$PYTHON" --version
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED}✗${NC} No Python in range >=3.10,<3.14 found on PATH."
    echo
    echo "Install one via pyenv:"
    echo "  pyenv install 3.13"
    echo "  pyenv global 3.13   # or: pyenv local 3.13 inside the project"
    echo
    echo "Or via Homebrew:"
    echo "  brew install python@3.13"
    exit 1
fi

# ── 2. Check if graphify is already importable ────────────────────────────────
if "$PYTHON" -c "import graphify" 2>/dev/null; then
    GRAPHIFY_VER=$("$PYTHON" -c "from importlib.metadata import version; print(version('graphifyy'))" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓${NC} graphifyy already installed (version $GRAPHIFY_VER) for this Python."
else
    echo -e "${GRAY}…${NC} graphifyy not installed for $PYTHON. Installing..."

    # Try plain pip install first
    if "$PYTHON" -m pip install graphifyy -q 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Installed via pip"
    elif "$PYTHON" -m pip install graphifyy -q --user 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Installed via pip --user"
    elif "$PYTHON" -m pip install graphifyy -q --break-system-packages 2>&1 | tail -3; then
        echo -e "${YELLOW}!${NC} Installed via --break-system-packages (PEP 668 environment)"
    else
        echo -e "${RED}✗${NC} pip install failed for all strategies."
        echo "   Try a virtualenv or pipx instead:"
        echo "     $PYTHON -m venv ~/.venvs/graphify"
        echo "     ~/.venvs/graphify/bin/pip install graphifyy"
        echo "     bash bin/setup-graphify.sh   # re-run; this script will detect the venv"
        exit 1
    fi

    if ! "$PYTHON" -c "import graphify" 2>/dev/null; then
        echo -e "${RED}✗${NC} pip reported success but 'import graphify' still fails."
        echo "   Possibly installed into a different Python. Check $PYTHON -m site"
        exit 1
    fi

    GRAPHIFY_VER=$("$PYTHON" -c "from importlib.metadata import version; print(version('graphifyy'))" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓${NC} graphifyy $GRAPHIFY_VER ready"
fi

# ── 3. Optionally pin to a project ────────────────────────────────────────────
if [ -n "$PROJECT" ]; then
    PROJECT=$(cd "$PROJECT" && pwd)
    if [ ! -d "$PROJECT" ]; then
        echo -e "${RED}✗${NC} Project path does not exist: $PROJECT"
        exit 1
    fi

    mkdir -p "$PROJECT/graphify-out"
    PIN_PATH="$PROJECT/graphify-out/.graphify_python"
    echo "$PYTHON" > "$PIN_PATH"
    echo -e "${GREEN}✓${NC} Pinned interpreter to $PIN_PATH"
    echo "   The graphify-ingest and graphify-update skills will now use this Python directly."
else
    echo
    echo -e "${GRAY}Tip:${NC} pass a project path to pin the interpreter for that project:"
    echo "    bash bin/setup-graphify.sh ~/path/to/your/code-project"
fi

echo
echo -e "${GREEN}Done.${NC}"
echo "Next: run /graphify-ingest in a code project to build its first graph."
