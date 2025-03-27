import os

from .nexus_client.NexusClient import NexusClient


def require_env_var(var_name):
    val = os.environ.get(var_name)
    if val is None:
        raise ValueError(f"Environment variable {var_name} is required")
    return val


_nexus_source_url = require_env_var('NEXUS_SOURCE_URL')
_nexus_source_username = require_env_var('NEXUS_SOURCE_USERNAME')
_nexus_source_password = require_env_var('NEXUS_SOURCE_PASSWORD')

_nexus_target_url = require_env_var('NEXUS_TARGET_URL')
_nexus_target_username = require_env_var('NEXUS_TARGET_USERNAME')
_nexus_target_password = require_env_var('NEXUS_TARGET_PASSWORD')


nexus_source = NexusClient(_nexus_source_url, _nexus_source_username, _nexus_source_password)
nexus_target = NexusClient(_nexus_target_url, _nexus_target_username, _nexus_target_password)

