from typing import Annotated, List, NamedTuple

from fastmcp import FastMCP

from todo_db import TodoDB


class Todo(NamedTuple):
    filename: Annotated[str, "Name of source file containing the #TODO"]
    line_number: Annotated[int, "Exact line where the #TODO can be found in the source file"]
    text: Annotated[str, "The #TODO text"]


todo_db = TodoDB()
#todo_db.sample_data()
mcp = FastMCP("TODO-MCP")


def run():
    mcp.run()


@mcp.tool(
    name="tool_add_todos",
    description="Add a list of #TODO from a source file"
)
def add_todos(
    todos: List[Todo],
):
    for todo in todos:
        todo_db.add(todo[0], todo[2], todo[1])
    return len(todos)


@mcp.tool(
    name="tool_add_todo",
    description="Add a single #TODO text from a source file"
)
def add_todo(
    filename: Annotated[str, "Name of source file containing the #TODO"],
    line_number: Annotated[int, "Exact line where the #TODO can be found in the source file"], 
    text: Annotated[str, "The #TODO text"],
) -> bool:
    return todo_db.add(filename, text, line_number)


# Resource (will be listed in template resource since it has a parameter)
@mcp.resource(
    name="resource_get_todos_for_file",
    description="Get all todos from a file. Returns an empty array if source file does not exist or there are not #TODOs in the file.",
    uri="todo://{filename}/todos",
)
def get_todos_for_file(
    filename: Annotated[str, "Name of source file containing the #TODO"],
) -> List[str]:
    todos = todo_db.get(filename)
    return [text for text in todos.values()]


if __name__ == "__main__":
    # Run in terminal "fastmcp todo_mcp.py"
    run()