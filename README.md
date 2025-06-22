# llm-tools-readonly-fs

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Grants LLM the ability to glob, grep, and view files within a directory.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-readonly-fs
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool ReadonlyFsTools "What test cases are missing?" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_readonly_fs import ReadonlyFsTools

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "What are the main classes this repository defines?",
    tools=[ReadonlyFsTools()],
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then install the dependencies and development dependencies:
```bash
cd llm-tools-readonly-fs
uv sync --dev
```

To add the plugin to your local LLM installation, in editable mode, run:
```bash
llm install -e .
```

To run the tests:
```bash
uv run pytest -v
```

To run linting and formatting:
```bash
uv run ruff check --fix
uv run ruff format
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Homepage](https://github.com/rbharvs/llm-tools-readonly-fs)
- [Issues](https://github.com/rbharvs/llm-tools-readonly-fs/issues)
- [Changelog](https://github.com/rbharvs/llm-tools-readonly-fs/releases)
