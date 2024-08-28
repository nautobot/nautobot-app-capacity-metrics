# Metrics & Monitoring Extension App

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/icon-nautobot-capacity-metrics.svg" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-app-capacity-metrics/actions"><img src="https://github.com/nautobot/nautobot-app-capacity-metrics/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/capacity-metrics/en/latest/"><img src="https://readthedocs.org/projects/nautobot-plugin-capacity-metrics/badge/"></a>
  <a href="https://pypi.org/project/nautobot-capacity-metrics/"><img src="https://img.shields.io/pypi/v/nautobot-capacity-metrics"></a>
  <a href="https://pypi.org/project/nautobot-capacity-metrics/"><img src="https://img.shields.io/pypi/dm/nautobot-capacity-metrics"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Metrics Endpoints

Nautobot already exposes some information via a Prometheus endpoint but the information currently available are mostly at the system level and not at the application level. System metrics and application level metrics are complementary with each other.

- **SYSTEM Metrics** are very useful to instrument code, track ephemeral information and get a better visibility into what is happening. (Example of metrics: nbr of requests, requests per second, nbr of exceptions, response time, etc ...) The idea is that when multiple instances of Nautobot are running behind a load balancer each one will produce a different set of metrics and the monitoring system needs to collect these metrics from all running instances and aggregate them in a dashboard. Nautobot exposes some system metrics at `localhost/metrics` - read more in the [Nautobot Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/guides/prometheus-metrics/).
- **APPLICATION Metrics** are at a higher level and represent information that is the same across all instances of an application running behind a load balancer. If I have 3 instances of Nautobot running, there is no point to ask each of them how many Device objects I have in the database, since they will always return the same information. In this case, the goal is to expose only 1 endpoint that can be served by any running instance. The prometheus endpoint is at `/api/plugins/capacity-metrics/app-metrics`.

Currently the app exposes these simple metrics by default:

- Jobs stats
- Models count (configurable via nautobot_config.py)

In addition, it is possible to use the app configuration to expose metrics about the versions of Python, Django, Nautobot and the installed Nautobot apps/apps.

## Try it out!

This App is installed in the Nautobot Community Sandbox found over at [demo.nautobot.com](https://demo.nautobot.com/)!

> For a full list of all the available always-on sandbox environments, head over to the main page on [networktocode.com](https://www.networktocode.com/nautobot/sandbox-environments/).

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/capacity-metrics/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/capacity-metrics/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/capacity-metrics/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/capacity-metrics/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/capacity-metrics/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/nautobot/nautobot-app-capacity-metrics/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/capacity-metrics/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/capacity-metrics/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.


