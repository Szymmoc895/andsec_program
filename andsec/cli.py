"""This module provides the andsec CLI."""
# andsec/cli.py

from typing import Optional
import typer
from andsec import __app_name__, __version__, welcome, run_emulator, run_drozer
from typing_extensions import Annotated


app = typer.Typer()

@app.command(help="Command to run tools. Type 'run --help' for help.")
def run(
    hello: bool = typer.Option(False, help="Run Welcome screen"),
    emulator: bool = typer.Option(False, help="Run Android emulator"),
    drozer: bool = typer.Option(False, help="Run Drozer tool"),
    path: bool = typer.Option(False, help="Give apk path"),
):
    if hello:
        welcome()
    if emulator:
        run_emulator()
    if drozer and not path:
        raise typer.Exit("--emulator is required when --hello is used")
    if drozer and path:
        run_drozer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return