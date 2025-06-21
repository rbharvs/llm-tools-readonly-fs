# llm-tools-readonly-fs

[![PyPI](https://img.shields.io/pypi/v/llm-tools-readonly-fs.svg)](https://pypi.org/project/llm-tools-readonly-fs/)
[![Changelog](https://img.shields.io/github/v/release/rbharvs/llm-tools-readonly-fs?include_prereleases&label=changelog)](https://github.com/rbharvs/llm-tools-readonly-fs/releases)
[![Tests](https://github.com/rbharvs/llm-tools-readonly-fs/actions/workflows/test.yml/badge.svg)](https://github.com/rbharvs/llm-tools-readonly-fs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rbharvs/llm-tools-readonly-fs/blob/main/LICENSE)

Grants LLM the ability to list, view, and search across files within a directory

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-readonly-fs
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool view "Example prompt goes here" --tools-debug
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

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-readonly-fs
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
