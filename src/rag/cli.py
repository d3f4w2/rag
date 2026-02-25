import typer

app = typer.Typer()


@app.command()
def index() -> None:
    typer.echo("index")


@app.command()
def ask() -> None:
    typer.echo("ask")


@app.command("eval")
def eval_cmd() -> None:
    typer.echo("eval")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
