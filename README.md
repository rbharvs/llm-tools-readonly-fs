# llm-tools-readonly-fs

[![PyPI](https://img.shields.io/pypi/v/llm-tools-readonly-fs.svg)](https://pypi.org/project/llm-tools-readonly-fs/)
[![Changelog](https://img.shields.io/github/v/release/rbharvs/llm-tools-readonly-fs?include_prereleases&label=changelog)](https://github.com/rbharvs/llm-tools-readonly-fs/releases)
[![Tests](https://github.com/rbharvs/llm-tools-readonly-fs/actions/workflows/test.yml/badge.svg)](https://github.com/rbharvs/llm-tools-readonly-fs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rbharvs/llm-tools-readonly-fs/blob/main/LICENSE)

Grants LLM the ability to glob, grep, and view files within a directory.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-readonly-fs
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool ReadonlyFsTools "Example prompt goes here" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_readonly_fs import view

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Example prompt goes here",
    tools=[view]
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
