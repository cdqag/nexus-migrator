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

1. Download a binary from [releases](https://github.com/cdqag/nexus-migrator/releases) page.
1. Add execution permissions to the binary:

    ```shell
    chmod +x nexus-migrator
    ```

1. Export the following environment variables:

    ```shell
    export NEXUS_SOURCE_URL=https://nexus-old.example.com
    export NEXUS_SOURCE_USERNAME=***
    export NEXUS_SOURCE_PASSWORD=***

    export NEXUS_TARGET_URL=https://nexus-new.example.com
    export NEXUS_TARGET_USERNAME=***
    export NEXUS_TARGET_PASSWORD=***
    ```

1. Run the migrator:

    ```shell
    ./nexus-migrator --from=NAME_OF_SOURCE_REPO --to=NAME_OF_TARGET_REPO
    ```

    If you want to filter by last downloaded date, you can use the `--last-downloaded` flag:

    ```shell
    ./nexus-migrator --from=NAME_OF_SOURCE_REPO --to=NAME_OF_TARGET_REPO --downloaded-in-days=90
    ```

> [!TIP]
> From our experiance we highly recommend to run the migrator from some VPS machine, like AWS EC2, with a good internet connection.
> The migrator will download and upload a lot of artifacts, so it's better to have a good internet connection.
> Nexus Components API is slow (especially Maven repositories), so the migration process can take a long time.
> We recommend to run the migrator inside a `screen` session, so you can detach from the session and the migrator will continue to run.

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.
