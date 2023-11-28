# Contributing to the App

The project is packaged with a light [development environment](dev_environment.md) based on `docker-compose` to help with the local development of the project and to run tests.

The project is following Network to Code software development guidelines and is leveraging the following:

- Python linting and formatting: `black`, `pylint`, `bandit`, `flake8`, and `pydocstyle`.
- YAML linting is done with `yamllint`.
- Django unit test to ensure the plugin is working properly.

Documentation is built using [mkdocs](https://www.mkdocs.org/). The [Docker based development environment](dev_environment.md#docker-development-environment) automatically starts a container hosting a live version of the documentation website on [http://localhost:8001](http://localhost:8001) that auto-refreshes when you make any changes to your local files.

## Branching Policy

The branching policy includes the following tenets:

- The `develop` branch is the primary branch to develop off of.
- PRs intended to add new features should be sourced from the `develop` branch.
- PRs intended to address bug fixes and security patches should be sourced from the `develop` branch.
- PRs intended to add new features that break backward compatibility should be discussed before a PR is created.

Nautobot Capacity Metrics app will observe semantic versioning, as of 1.0. This may result in a quick turn around in minor versions to keep pace with an ever-growing feature set.

## Release Policy

!!! warning "Developer Note - Remove Me!"
    How new versions are released.
