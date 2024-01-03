"""This module provides the andsec CLI."""
# andsec/cli.py

from typing import Optional, List
import typer
from andsec import __app_name__, __version__,what_tool ,welcome, run_emulator, run_drozer, run_trufflehog, run_mobsf, run_RMS
from typing_extensions import Annotated


app = typer.Typer()

@app.command(help="Command to run tools. Type 'run --help' for help.")
def run(
    hello: bool = typer.Option(False, help="Run Welcome screen"),
    emulator: bool = typer.Option(False, help="Run Android emulator"),
    drozer: bool = typer.Option(False, help="Run Drozer tool"),
    mobsf: bool = typer.Option(False, help="Run MobSF tool"),
    truffleLocal: Annotated[Optional[str], typer.Option(help="Run Trufflehog, choose offline or online version")] = None,
    truffleGit: Annotated[Optional[str], typer.Option(help="Run Trufflehog, choose offline or online version")] = None,
    path: Annotated[Optional[str], typer.Option(help="Give path to the apk file")] = None,
    install: bool = typer.Option(False, help="Install .apk on emulator"),
    RMS: bool = typer.Option(False, help="Run RMS tool"),
):
    if hello:
        welcome()
    if emulator:
        run_emulator()
    if drozer and not path:
        raise typer.Exit("--path is required when --drozer is used")
    if drozer and path:
        run_drozer()
        print("works")
    if truffleGit:
        run_trufflehog(False, True, truffleGit)
    if truffleLocal:
        run_trufflehog(False, False, truffleLocal)
    if mobsf and not path:
        raise typer.Exit("--path is required when --drozer is used")
    if mobsf and path:
        run_mobsf(path)
    if install:
        print("work in progress")
    if RMS:
        run_RMS()
        

@app.command(help="Command to run new user version")
def graphical():
    what_tool()

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