# Nexus Migrator

Tool for migrating artifacts between Sonatype Nexus repositories.

## Motivation

The motivation behind this tool is to provide a way to migrate artifacts between Nexus repositories.
We had a Nexus OSS instance, but we wanted to migrate to Nexus Pro. Additionally, we were using old Orient DB as
a storage backend, and we wanted to switch to the PostgreSQL database. Unfortunately, the company behind Nexus neither
provide a tool nor a guide on how to migrate artifacts between different Nexus instances. So, we decided to write our
own tool and share it with the community.

## Features

* Supported formats:

    * Maven
    * Helm
    * PyPI
    * Raw

* Can filter by last downloaded date (in days)
* Keeps a history for each migration run:

    * On which page of the components list the migration stopped
    * Cause of the component migration skip/failure
    * Already migrated components

## Usage

TODO

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.
