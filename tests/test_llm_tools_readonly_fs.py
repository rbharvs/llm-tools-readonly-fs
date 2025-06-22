import json

import llm

from llm_tools_readonly_fs import ReadonlyFsTools


def test_tool() -> None:
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {
                        "name": "ReadonlyFsTools_glob",
                        "arguments": {"glob_patterns": ["pelican"]},
                    }
                ]
            }
        ),
        tools=[ReadonlyFsTools()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {
            "name": "ReadonlyFsTools_glob",
            "output": '"GlobOutput(paths=[], truncated=False)"',
            "tool_call_id": None,
        }
    ]
