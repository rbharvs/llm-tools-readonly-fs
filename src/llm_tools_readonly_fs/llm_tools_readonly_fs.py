import llm


def view(input: str) -> str:
    return f"hello {input}"


@llm.hookimpl
def register_tools(register) -> None:
    register(view)
