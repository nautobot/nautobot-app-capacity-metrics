# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The plugin is compatible with Nautobot 2.0.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

## Install Guide

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this plugin is [`nautobot-capacity-metrics`](https://pypi.org/project/nautobot-capacity-metrics/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-capacity-metrics
```

To ensure Metrics & Monitoring Extension Plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-capacity-metrics` package:

```shell
echo nautobot-capacity-metrics >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_capacity_metrics"` to the `PLUGINS` list.
- Append the `"nautobot_capacity_metrics"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_capacity_metrics"]

# PLUGINS_CONFIG = {
#   "nautobot_capacity_metrics": {
#     ADD YOUR SETTINGS HERE
#   }
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

!!! warning "Developer Note - Remove Me!"
    Any configuration required to get the App set up. Edit the table below as per the examples provided.

The plugin behavior can be controlled with the following list of settings:

| Key     | Example | Default | Description                          |
| ------- | ------ | -------- | ------------------------------------- |
| `app_metrics` | `{"models": {"dcim": "Device": True}}` | `{"models": {"dcim": {"Site": True, "Rack": True, "Device": True}, "ipam": {"IPAddress": True, "Prefix": True}}, "jobs": True, "queues": True, "versions": {"basic": False, "plugins": False}` | Specifies which metrics to publish for each app. |
