import typer
from typing import Annotated
from rich import print

app = typer.Typer()


@app.command(help="Greet user by name")
def hello(
    name: Annotated[
        str,
        typer.Argument(help="Name to greet"),
    ],
):
    print(f"Hello, [green]{name}[/green]")


if __name__ == "__main__":
    app()
