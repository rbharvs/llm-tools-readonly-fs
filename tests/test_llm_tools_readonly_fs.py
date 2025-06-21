import json

import llm

from llm_tools_readonly_fs import view


def test_tool() -> None:
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {"tool_calls": [{"name": "view", "arguments": {"input": "pelican"}}]}
        ),
        tools=[view],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {"name": "view", "output": "hello pelican", "tool_call_id": None}
    ]
