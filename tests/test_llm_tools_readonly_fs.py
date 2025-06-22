import json
import os

import llm

from llm_tools_readonly_fs import ReadonlyFsTools


def test_glob_finds_python_files() -> None:
    """Test glob functionality by finding Python files including this test file itself."""
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "ReadonlyFsTools_glob",
                        "arguments": {"glob_patterns": ["**/*.py"]},
                    }
                ]
            }
        ),
        tools=[ReadonlyFsTools()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    # Parse the output string to verify structure
    output_str = tool_results[0]["output"]
    assert "GlobOutput" in output_str
    assert "paths=" in output_str
    assert "truncated=False" in output_str

    # Should find at least this test file
    test_filename = os.path.basename(__file__)
    assert test_filename in output_str


def test_grep_finds_function_definitions() -> None:
    """Test grep by searching for function definitions in this test file itself."""
    model = llm.get_model("echo")
    test_filename = os.path.basename(__file__)

    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "ReadonlyFsTools_grep",
                        "arguments": {
                            "search_regex": "def test_",
                            "glob_patterns": [f"**/{test_filename}"],
                        },
                    }
                ]
            }
        ),
        tools=[ReadonlyFsTools()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    output_str = tool_results[0]["output"]
    assert "GrepOutput" in output_str
    assert "matches=" in output_str

    # Should find our test function definitions
    assert "def test_" in output_str
    assert test_filename in output_str


def test_view_reads_own_imports() -> None:
    """Test view by reading the import section of this test file itself."""
    model = llm.get_model("echo")
    test_filename = __file__

    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "ReadonlyFsTools_view",
                        "arguments": {
                            "file_path": test_filename,
                            "line_offset": 0,
                            "line_count": 10,
                        },
                    }
                ]
            }
        ),
        tools=[ReadonlyFsTools()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    output_str = tool_results[0]["output"]
    assert "ViewOutput" in output_str
    assert "view=" in output_str

    # Should contain our import statements
    assert "import json" in output_str
    assert "import llm" in output_str
    assert test_filename in output_str


def test_grep_finds_imports_across_project() -> None:
    """Test grep across multiple files to find import statements throughout the project."""
    model = llm.get_model("echo")

    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "ReadonlyFsTools_grep",
                        "arguments": {
                            "search_regex": "^import |^from .* import",
                            "glob_patterns": ["**/*.py"],
                        },
                    }
                ]
            }
        ),
        tools=[ReadonlyFsTools()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    output_str = tool_results[0]["output"]
    assert "GrepOutput" in output_str
    assert "matches=" in output_str

    # Should find imports from different files
    assert "import" in output_str
    # Should find imports from both test file and main module
    common_imports = ["import json", "import llm", "from llm"]
    assert any(imp in output_str for imp in common_imports)
