import typer

from .grandmaster import nexus_source, nexus_target
from .history import init_historian


def migrate(
    from_repo: str,
    to_repo: str,
    downloaded_in_days: int = 0,
):
    historian = init_historian(f"FROM-{from_repo}-TO-{to_repo}")
    for component in nexus_source.list_components(from_repo, downloaded_in_days):
        if historian and historian.has_component_been_migrated(component.id):
            typer.echo(f"Component {component} has been already migrated - skipping")
            continue

        typer.echo(f"Migrating component {component} from {from_repo} to {to_repo}")
        nexus_source.download_component(component)
        nexus_target.upload_component(component, to_repo)

        if historian:
            historian.note_component(component.id, has_been_migrated=True)

        component.remove_temp_dir()
