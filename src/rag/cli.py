import json

import typer

from rag.eval.ragas_runner import run_eval
from rag.index.build_index import rebuild_index
from rag.workflow.graph import run_rag

app = typer.Typer()


@app.command()
def index(
    data_dir: str = typer.Option("example-data", "--data-dir"),
    index_dir: str = typer.Option(".rag_index", "--index-dir"),
) -> None:
    stats = rebuild_index(data_dir=data_dir, index_dir=index_dir)
    typer.echo(json.dumps(stats, ensure_ascii=False))


@app.command()
def ask(
    question: str,
    top_k: int = typer.Option(3, "--top-k"),
    label_filter: str | None = typer.Option(None, "--label-filter"),
    json_pretty: bool = typer.Option(False, "--json-pretty"),
    index_dir: str = typer.Option(".rag_index", "--index-dir"),
    data_dir: str = typer.Option("example-data", "--data-dir"),
) -> None:
    result = run_rag(
        question=question,
        top_k=top_k,
        label_filter=label_filter,
        index_dir=index_dir,
        data_dir=data_dir,
    )
    indent = 2 if json_pretty else None
    typer.echo(json.dumps(result, ensure_ascii=False, indent=indent))


@app.command("eval")
def eval_cmd(
    dataset_path: str = typer.Option("eval/dataset.jsonl", "--dataset-path"),
    data_dir: str = typer.Option("example-data", "--data-dir"),
    index_dir: str = typer.Option(".rag_index", "--index-dir"),
    json_pretty: bool = typer.Option(False, "--json-pretty"),
) -> None:
    result = run_eval(dataset_path=dataset_path, data_dir=data_dir, index_dir=index_dir)
    indent = 2 if json_pretty else None
    typer.echo(json.dumps(result, ensure_ascii=False, indent=indent))
    if not bool(result.get("pass_gate", False)):
        raise typer.Exit(code=1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
