from pathlib import Path
import asyncio
import typer

from gae.core.bootstrap import bootstrap
from gae.core.controller import Controller

app = typer.Typer()


@app.command()
def run(
    manifest: Path = typer.Argument(..., help="Path to dataset manifest")
):
    registry = bootstrap()
    controller = Controller(registry)

    result = asyncio.run(controller.run(manifest))

    print(result)


if __name__ == "__main__":
    app()
