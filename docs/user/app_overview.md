# App Overview

This document provides an overview of the App including critical information and import considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

The plugin is composed of multiple features that can be used independently:

- Application Metrics Endpoint (prometheus): `/api/plugins/capacity-metrics/app-metrics`.
- RQ Queue Metrics Endpoint (prometheus): `/api/plugins/capacity-metrics/rq-metrics`.
- RQ Worker Metrics Command: add prometheus endpoint on each RQ worker.

### Application Metrics Endpoint

Nautobot already exposes some information via a Prometheus endpoint but the information currently available are mostly at the system level and not at the application level.

- **SYSTEM Metrics** are very useful to instrument code, track ephemeral information and get a better visibility into what is happening.
    + Example of metrics: number of requests, requests per second, number of exceptions, response time, etc ...
    + The idea is that when multiple instances of Nautobot are running behind a load balancer each one will produce a different set of metrics and the monitoring system needs to collect these metrics from all running instances and aggregate them in a dashboard. Nautobot exposes some system metrics at `localhost/metrics`.
    + Read more in the [Nautobot Documentation](https://docs.nautobot.com/projects/core/en/stable/additional-features/prometheus-metrics/).
- **APPLICATION Metrics** are at a higher level and represent information that is the same across all instances of an application running behind a load balancer. If I have 3 instances of Nautobot running, there is no point to ask each of them how many Device objects I have in the database, since they will always return the same information. In this case, the goal is to expose only 1 endpoint that can be served by any running instance.

System metrics and application level metrics are complementary with each other.

Currently the plugin exposes these simple metrics by default:

- RQ Queues stats
- Jobs stats
- Models count (configurable via `nautobot_config.py`)

### Queue System Metrics Endpoint

In addition to the default Nautobot system metrics which are exposed at `/metrics`, which are largely centered around the Django system on which Nautobot is based, this plugin provides some additional system metrics around the queuing system Nautobot uses to communicate with the Nautobot worker services. This endpoint is provided separately via `/api/plugins/capacity-metrics/rq-metrics`, this endpoint can be scraped more frequently than the other application metrics endpoint.






## Audience (User Personas) - Who should use this App?

!!! warning "Developer Note - Remove Me!"
    Who is this meant for/ who is the common user of this app?

## Authors and Maintainers

## Nautobot Features Used

!!! warning "Developer Note - Remove Me!"
    What is shown today in the Installed Plugins page in Nautobot. What parts of Nautobot does it interact with, what does it add etc. ?

### Extras

!!! warning "Developer Note - Remove Me!"
    Custom Fields - things like which CFs are created by this app?
    Jobs - are jobs, if so, which ones, installed by this app?
