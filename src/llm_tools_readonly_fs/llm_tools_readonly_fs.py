from pathlib import Path
from typing import List

import llm
from llm import Toolbox
from readonly_fs_tools import (
    FileWindow,
    Globber,
    Grepper,
    OutputBudget,
    Sandbox,
    Viewer,
)


class ReadonlyFsTools(Toolbox):
    """Tools for reading and searching files in a sandboxed filesystem.

    These tools provide the ability to:
        - List files and directories using advanced glob patterns (`glob`)
        - Search for text or code with regular expressions across file sets (`grep`)
        - View and read file contents in controlled, windowed slices (`view`)

    Best practices:
        - Use `glob` to discover files before searching or viewing to understand broad context.
        - Use `grep` to narrow down specific content or patterns of interest.
        - Use `view` to read additional context in manageable chunks.
    """

    def __init__(
        self,
        *,
        sandbox_dir: str = str(Path.cwd()),
        blocked_files: List[str] = [],
        allow_hidden: bool = False,
        output_limit: int = 10000,
    ) -> None:
        super().__init__()
        sandbox = Sandbox(
            sandbox_dir=Path(sandbox_dir),
            blocked_files=[Path(fname) for fname in blocked_files],
            allow_hidden=allow_hidden,
        )
        self._output_limit = output_limit
        self._globber = Globber.from_sandbox(sandbox)
        self._grepper = Grepper.from_sandbox(sandbox)
        self._viewer = Viewer.from_sandbox(sandbox)

    def glob(self, glob_patterns: List[str]) -> str:
        """Find files matching glob patterns within the sandbox directory.

        Use this tool to discover files in a codebase or directory structure. Supports
        standard glob patterns including wildcards and recursive search.

        Args:
            patterns: List of glob patterns to match files against. Common patterns:
                - "*.py" - All Python files in current directory
                - "**/*.py" - All Python files recursively in all subdirectories
                - "src/**/*.js" - All JavaScript files in src/ directory tree
                - "test_*.py" - Python files starting with "test_"
                - "**/README.md" - All README.md files in any subdirectory

        Returns:
            String representation of `GlobOutput` containing:
            - `paths`: List of matched file paths relative to the sandbox directory.
            - `truncated`: Boolean indicating if the output was truncated due to size limits.

        Examples:
            Find all Python files in the sandbox root:
            ```
            toolbox.glob(["*.py"])
            # Returns:
            # GlobOutput(paths=[Path('main.py'), Path('utils.py'), Path('config.py')], truncated=False)
            ```

            Find configuration files recursively:
            ```
            toolbox.glob(["**/*.json", "**/*.yaml", "**/*.toml"])
            # Returns:
            # GlobOutput(paths=[Path('config/settings.json'), Path('docker-compose.yaml'), Path('pyproject.toml')], truncated=False)
            ```

            Find test files:
            ```
            toolbox.glob(["test_*.py", "**/test_*.py", "**/tests/*.py"])
            ```

        Note:
            - Patterns are relative to the sandbox directory
            - Hidden files (starting with '.') are excluded unless allow_hidden=True
            - Blocked files are automatically filtered out
            - Results are deduplicated if multiple patterns match the same file
        """
        return self._globber.glob(glob_patterns, OutputBudget(limit=self._output_limit))

    def grep(self, search_regex: str, glob_patterns: List[str]) -> str:
        """Search for regex patterns within files matching glob patterns.

        Use this tool to find specific content, code patterns, or text within files.
        Combines file discovery (via glob patterns) with content searching (via regex).

        Args:
            search_regex: Regular expression pattern to search for. Examples:
                - "def \w+" - Function definitions (Python)
                - "class \w+" - Class definitions
                - "import \w+" - Import statements
                - "TODO|FIXME" - Code comments with tasks
                - "@\w+\(" - Decorators (Python)
                - "function \w+\(" - JavaScript functions
                - "\\b\w+Error\\b" - Error class names
                - "https?://[^\s]+" - URLs
                - "\d{4}-\d{2}-\d{2}" - Dates in YYYY-MM-DD format

            file_patterns: List of glob patterns to limit search scope. Same format
                as glob() method patterns. Examples:
                - ["*.py"] - Search only Python files in the sandbox root
                - ["**/*.js", "**/*.ts"] - Search JavaScript and TypeScript files
                - ["src/**/*"] - Search all files in src directory
                - ["app/main.py", "app/utils.py"] - Search specific files

        Returns:
            String representation of `GrepOutput` containing:
            - `matches`: List of matching lines as FileContent objects.
            - `truncated`: Boolean indicating if the output was truncated due to size limits.

        Examples:
            Find function definitions in Python files:
            ```
            toolbox.grep("def \w+", ["**/*.py"])
            # Returns:
            # === src/main.py ===
            # def process_data():
            #
            # def validate_input():
            #
            # === utils/helpers.py ===
            # def format_output():
            # GrepOutput(
            #   matches=[
            #       FileContent(
            #           path=Path('src/main.py'),
            #           contents='def process_data():\n',
            #           FileWindow(line_offset=23, line_count=1),
            #       ),
            #       FileContent(
            #           path=Path('src/main.py'),
            #           contents='def validate_input():\n',
            #           FileWindow(line_offset=45, line_count=1),
            #       ),
            #       FileContent(
            #           path=Path('utils/helpers.py'),
            #           contents='def format_output():\n',
            #           FileWindow(line_offset=12, line_count=1),
            #       ),
            #   ],
            #   truncated=False,
            # )
            ```

            Find TODO comments across codebase:
            ```
            toolbox.grep("TODO|FIXME|XXX", ["**/*.py", "**/*.js", "**/*.md"])
            # Returns:
            # GrepOutput(
            #   matches=[
            #       FileContent(
            #           path=Path('src/parser.py'),
            #           contents='# TODO: Implement error handling\n',
            #           FileWindow(line_offset=10, line_count=1),
            #       ),
            #       FileContent(
            #           path=Path('docs/README.md'),
            #           contents='<!-- FIXME: Update installation instructions -->\n',
            #           FileWindow(line_offset=5, line_count=1),
            #       ),
            #   ],
            #   truncated=False,
            # )
            ```

            Find import statements:
            ```
            toolbox.grep("^from .* import|^import .*", ["**/*.py"])
            ```

            Find configuration values:
            ```
            toolbox.grep('"[A-Z_]+"\s*:', ["**/*.json"])
            ```

        Note:
            - Regex patterns use line-by-line matching (not multiline)
            - Case-sensitive by default (use (?i) prefix for case-insensitive)
            - Each matching line is returned as a separate result
            - Content is searched in UTF-8 encoding with error tolerance
            - Binary files are handled gracefully (may produce garbled text)
        """
        return self._grepper.grep(
            search_regex, glob_patterns, OutputBudget(limit=self._output_limit)
        )

    def view(
        self,
        file_path: str,
        line_offset: int = 0,
        line_count: int = 100,
    ) -> str:
        """Read and view contents of a specific file within a defined window.

        Use this tool to examine file contents, understand code structure, or read
        documentation. Supports windowed reading to focus on specific sections.

        Args:
            file_path: Path to the file to read, relative to sandbox directory.
                Examples: "main.py", "src/utils.py", "docs/README.md"

            line_offset: Starting line number (0-based). Use to skip to specific
                sections of large files. Defaults to 0 (start of file).

            line_count: Number of lines to read from the starting offset.
                Defaults to 100 lines. Adjust based on file size and needs.

        Returns:
            String representation of `ViewOutput` containing:
            - `view`: FileContent object containing the path, contents, and line window read.
            - `truncated`: Boolean indicating if the output was truncated due to size limits.

        Examples:
            Read beginning of a file:
            ```
            toolbox.view("main.py")
            # Returns:
            # ViewOutput(
            #   view=FileContent(
            #       path=Path('main.py'),
            #       contents='#!/usr/bin/env python3\n\"\"\"Main application entry point.\"\""\n\nimport sys\nfrom pathlib import Path\n...',
            #       FileWindow(line_offset=0, line_count=50),
            #   ),
            #   truncated=False,
            # )
            ```

            Read specific section of a large file:
            ```
            toolbox.view("src/parser.py", line_offset=100, line_count=20)
            # Returns:
            # === src/parser.py (lines 101-120) ===
            # def parse_expression(self, tokens):
            #     \"\"\"Parse mathematical expression.\"\"\"
            #     ...
            # ViewOutput(
            #   view=FileContent(
            #       path=Path('src/parser.py'),
            #       contents='def parse_expression(self, tokens):\n    \"\"\"Parse mathematical expression.\"\"\"\n...',
            #       FileWindow(line_offset=100, line_count=20),
            #   ),
            #   truncated=False,
            # )
            ```

            Read configuration file:
            ```
            toolbox.view("pyproject.toml", line_count=30)
            ```

            Read end of a log file (if you know approximate size):
            ```
            toolbox.view("logs/app.log", line_offset=1000, line_count=50)
            ```

            Read just a few lines to check file format:
            ```
            toolbox.view("data.csv", line_count=5)
            # Returns:
            # ViewOutput(
            #   view=FileContent(
            #       path=Path('data.csv'),
            #       contents='name,age,city\nJohn,25,NYC\nJane,30,LA\nBob,35,Chicago\nAlice,28,Boston\n',
            #       FileWindow(line_offset=0, line_count=5),
            #   ),
            #   truncated=False,
            # )
            ```

        Note:
            - File paths are relative to the sandbox directory
            - Line numbers in output are 0-indexed (i.e., number of lines offset from top)
            - Files are read with UTF-8 encoding and error tolerance
            - Binary files may produce garbled output but won't crash
            - Empty files return empty content (not an error)
            - If line_offset is beyond file end, returns empty content
            - Large files are handled efficiently (streaming, not full load)

        Best Practices:
            - Use smaller line_count for initial exploration
            - Use line_offset to jump to known sections (after using grep)
            - Check file size first with glob if dealing with very large files
            - For code review, start with line_count=20-50 to get context
        """
        return self._viewer.view(
            Path(file_path),
            FileWindow(line_offset=line_offset, line_count=line_count),
            OutputBudget(limit=self._output_limit),
        )


@llm.hookimpl
def register_tools(register) -> None:
    register(ReadonlyFsTools)
