from typing import Optional

from .models.Component import Component
from .models.HelmComponent import HelmComponent
from .models.MavenComponent import MavenComponent
from .models.RawComponent import RawComponent
from .models.PypiComponent import PypiComponent


def factory_component(item_raw: dict) -> Optional[Component]:
    if item_raw["format"] == "maven2":
        return create_maven_component(item_raw)

    elif item_raw["format"] == "pypi":
        return create_pypi_component(item_raw)

    elif item_raw["format"] == "helm":
        return create_helm_component(item_raw)

    elif item_raw["format"] == "raw":
        return create_raw_component(item_raw)

    raise ValueError(f"Unsupported format: {item_raw['format']}")

def create_maven_component(item_raw: dict) -> Optional[MavenComponent]:
    component = MavenComponent(**item_raw)

    # Return none if there is no jar file in the assets
    found = False
    for asset in component.assets:
        if asset.path.suffix == ".jar":
            found = True
            break

    if not found:
        raise ValueError("No JAR file found in component")

    return component

def create_pypi_component(item_raw: dict) -> Optional[PypiComponent]:
    component = PypiComponent(**item_raw)

    # Return none if there is no wh(ee)l file in the assets
    found = False
    for asset in component.assets:
        if asset.path.suffix == ".whl":
            found = True
            break

    if not found:
        raise ValueError("No WHL file found in component")

    return component

def create_helm_component(item_raw: dict) -> Optional[HelmComponent]:
    return HelmComponent(**item_raw)

def create_raw_component(item_raw: dict) -> Optional[RawComponent]:
    return RawComponent(**item_raw)
