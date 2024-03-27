# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The app is compatible with Nautobot 2.0.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

## App Security

The Capacity Metrics App will use the `METRICS_AUTHENTICATED` setting from Nautobot Core if set to `True` to require authentication to reach the URL endpoint. The `METRICS_AUTHENTICATED` setting was added in Nautobot 2.1.5. See [Nautobot Core Optional Settings](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/configuration/optional-settings/#metrics_authenticated) for further configuration details. If not set or set to `False`, the URL endpoint will work as it currently does without authentication.

## Install Guide

!!! note
    Apps can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this app is [`nautobot-capacity-metrics`](https://pypi.org/project/nautobot-capacity-metrics/).

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-capacity-metrics
```

To ensure Metrics & Monitoring Extension App is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-capacity-metrics` package:

```shell
echo nautobot-capacity-metrics >> local_requirements.txt
```

Once installed, the app needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_capacity_metrics"` to the `PLUGINS` list.
- Append the `"nautobot_capacity_metrics"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_capacity_metrics"]

# PLUGINS_CONFIG = {
#     "nautobot_capacity_metrics": {
#         "app_metrics": {
#             "gitrepositories": True,
#             "jobs": True,
#             "models": {
#                 "dcim": {
#                     "Site": True,
#                     "Rack": True,
#                     "Device": True,
#                     "Interface": True,
#                     "Cable": True,
#                 },
#                 "ipam": {
#                     "IPAddress": True,
#                     "Prefix": True,
#                 },
#                 "extras": {
#                     "GitRepository": True
#                 },
#             },
#             "queues": True,
#             "versions": {
#                 "basic": True,
#                 "plugins": True,
#             }
#         }
#     },
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

The app behavior can be controlled with the following list of settings:

| Key     | Example | Default | Description                          |
| ------- | ------ | -------- | ------------------------------------- |
| `app_metrics` | `{"models": {"dcim": "Device": True}}` | `{"models": {"dcim": {"Site": True, "Rack": True, "Device": True}, "ipam": {"IPAddress": True, "Prefix": True}}, "jobs": True, "queues": True, "versions": {"basic": False, "plugins": False}` | Specifies which metrics to publish for each app. |

## Included Grafana Dashboard

Included within this app is a Grafana dashboard which will work with the example configuration above. To install this dashboard import the JSON from [Grafana Dashboard](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/nautobot_grafana_dashboard.json) into Grafana.

![Nautobot Grafana Dashboard](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/nautobot_grafana_dashboard.png)
