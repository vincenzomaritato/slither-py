import typer
from slither.core.game import run_game

app = typer.Typer(help="Slither.py — A modern Snake game in Python 🐍")

@app.command()
def play() -> None:
    """Start the game."""
    run_game()
    
@app.command()
def info() -> None:
    """Print project info."""
    typer.echo("Slither.py — Open Source Snake Game made with Python and ❤️")

if __name__ == "__main__":
    app()