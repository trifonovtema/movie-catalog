from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.movie_catalog.auth.services.redis_tokens_helper import redis_tokens

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    name="tokens",
    help="Work with tokens",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="Token to check"),
    ],
):
    """
    Check if passed token exists or not
    """
    res = redis_tokens.is_token_exists(token)
    print(
        "Token",
        "[bold]" + token + "[/bold]",
        "[green]exists[/green]" if res is True else "[red]does not exist[/red]",
    )


@app.command(name="list")
def list_tokens():
    """
    List all tokens
    """
    print(Markdown("# API Tokens List"))
    print(
        Markdown(
            "".join(["\n - *" + token + "*" for token in redis_tokens.get_tokens()])
        )
    )
    print()


@app.command(name="create")
def create():
    """
    Create a new token and add it to database
    """
    token = redis_tokens.generate_and_save_token()
    print("Token", "[bold]" + token + "[/bold]", "created")


@app.command(name="add")
def add(
    token: Annotated[
        str,
        typer.Argument(help="Token to add"),
    ],
):
    """
    Add passed token to database
    """
    redis_tokens.add_token(token)
    print("Token", "[bold]" + token + "[/bold]", "added")


@app.command(name="rm")
def remove(
    token: Annotated[
        str,
        typer.Argument(help="Token to add"),
    ],
):
    """
    Remove passed token from database
    """
    redis_tokens.delete_token(token)
    print("Token", "[bold]" + token + "[/bold]", "removed")
