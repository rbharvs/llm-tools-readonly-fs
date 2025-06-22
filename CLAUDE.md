# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` for dependency management and Python package tooling.

### Setup
```bash
uv sync --dev
```

### Code Quality
```bash
uv run ruff check --fix     # Lint code
uv run ruff format          # Format code
```

### Testing
```bash
uv run pytest              # Run all tests
uv run pytest -v           # Run tests with verbose output
uv run pytest tests/test_llm_tools_readonly_fs.py  # Run specific test file
```

## Project Architecture

This is an LLM plugin that provides readonly filesystem tools through the `llm` framework. The project is a thin wrapper around the `readonly-fs-tools` dependency.

### Core Structure
- `src/llm_tools_readonly_fs/llm_tools_readonly_fs.py` - Main plugin implementation
- Provides 'glob', 'grep', and 'glance' tools for LLM via ReadonlyFsTools toolbox
- Uses `@llm.hookimpl` decorator to register tools with the LLM framework

The plugin follows the LLM framework's tool registration pattern and is designed to be installed as a Python package that extends LLM's capabilities.
