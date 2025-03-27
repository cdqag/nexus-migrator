import typer
from typing_extensions import Annotated

from .migrate import migrate as migrate_fn
from .version import version as app_version

cli = typer.Typer()

def version_callback(value: bool):
    if value:
        typer.echo(f"Nexus Migrator v{app_version}\n\nCreated by CDQ AG - https://www.cdq.com\nSharing is caring! ❤️\n\nLicensed under the Apache License 2.0 - https://github.com/cdqag/nexus-migrator/blob/main/LICENSE")
        raise typer.Exit()

@cli.command()
def migrate(
        from_repo: Annotated[str, typer.Option("--from", help="The source repository to migrate from")],
        to_repo: Annotated[str, typer.Option("--to", help="The target repository to migrate to")],
        downloaded_in_days: Annotated[int, typer.Option(help="The number of days to consider for downloaded components")] = 0,
):
    typer.echo("Migrating Repositories...")
    migrate_fn(from_repo, to_repo, downloaded_in_days)


@cli.callback()
def main(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    # Do other global stuff, handle other global options here
    return


def run():
    cli(prog_name="nexus_migrator")


if __name__ == "__main__":
    run()
