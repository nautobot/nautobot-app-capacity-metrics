# Using the App

This document describes common use-cases and scenarios for this App.

## General Usage

Configure your Prometheus server to collect the application metrics at `/api/plugins/capacity-metrics/app-metrics/`

```yaml
# Sample prometheus configuration
scrape_configs:
  - job_name: 'nautobot_app'
    scrape_interval: 120s
    metrics_path: /api/plugins/capacity-metrics/app-metrics
    static_configs:
      - targets: ['nautobot']
```

### Queue System Metrics Endpoint

In addition to the default Nautobot system metrics which are exposed at `/metrics` which are largely centered around the Django system on which Nautobot is based this app provides some additional system metrics around the queuing system Nautobot uses to communicate with the Nautobot worker services.

## Use-cases and common workflows

### Add your own metrics

This app supports some options to generate and publish your own application metrics behind the same endpoint.

#### Option 1 - Register function(s) via nautobot_config.py

It's possible to create your own function to generate some metrics and register it to the app in the nautobot_config.py.
Here is an example where the custom function are centralized in a `metrics.py` file, located next to the main `nautobot_config.py`.

```python
# metrics.py
from prometheus_client.core import GaugeMetricFamily

def metric_prefix_utilization():
    """Report prefix utilization as a metric per container."""
    from ipam.models import Prefix  # pylint: disable=import-outside-toplevel

    containers = Prefix.objects.filter(status="container").all()
    g = GaugeMetricFamily(
        "nautobot_prefix_utilization", "percentage of utilization per container prefix", labels=["prefix", "role", "site"]
    )

    for container in containers:

        site = "none"
        role = "none"
        if container.role:
            role = container.role.slug

        if container.site:
            site = container.site.slug

        g.add_metric(
            [str(container.prefix), site, role], container.get_utilization(),
        )

    yield g
```

The new function can be imported in the `nautobot_config.py` file and registered with the app.

```python
# nautobot_config.py
from nautobot.metrics import metric_prefix_utilization
PLUGINS_CONFIG = {
    "nautobot_capacity_metrics": {
      "app_metrics": {
        "extras": [
          metric_prefix_utilization
        ]
      }
    }
},
```

#### Option 2 - Registry for third party apps

Any app can include its own metrics to improve the visibility and/or the troubleshooting of the app itself.
Third party apps can register their own function(s) using the `ready()` function as part of their `NautobotAppConfig` class.

```python
# my_app/__init__.py
from nautobot_capacity_metrics import register_metric_func
from nautobot.metrics import metric_circuit_bandwidth

class MyAppConfig(NautobotAppConfig):
    name = "nautobot_myapp"
    verbose_name = "Demo App"
    # [ ... ]
    def ready(self):
        super().ready()
        register_metric_func(metric_circuit_bandwidth)
```

#### Option 3 - NOT AVAILABLE YET - Metrics directory

In the future it will be possible to add metrics by adding them in a predefined directory, similar to jobs.

## App Configuration Parameters

The behavior of the app_metrics feature can be controlled with the following list of settings (under `nautobot_capacity_metrics > app_metrics`):
- `gitrepositories` boolean (default **False**), publish stats about the gitrepositories (success, warning, info, failure)
- `jobs` boolean (default **False**), publish stats about the jobs (success, warning, info, failure)
- `queues` boolean (default **False**), publish stats about Worker (nbr of worker, nbr and type of job in the different queues)
- `models` nested dict, publish the count for a given object (Nbr Device, Nbr IP etc.. ). The first level must be the name of the module in lowercase (dcim, ipam etc..), the second level must be the name of the object (usually starting with a uppercase). Note that you can include models from apps by specifying the module name under the "_module" key
- `versions` nested dict, publish the versions of installed software

    ```python
    PLUGINS_CONFIG = {
      "nautobot_capacity_metrics": {
        "app_metrics": {
          "models": {
             "dcim": {"Site": True, "Rack": True, "Device": True},
             "ipam": {"IPAddress": True, "Prefix": True},
           },
           "jobs": True,
           "queues": True,
           "versions": {
             "basic": True,
             "plugins": True,
           }
         }
       }
    }
    ```

## Screenshots

![Metrics](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/capacity-metrics-screenshot-01.png "Metrics")

![Device Per Status](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/capacity-metrics-screenshot-02.png "Device Per Status")

![Rack Capacity](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/capacity-metrics-screenshot-03.png "Rack Capacity")

![Prefix Capacity](https://raw.githubusercontent.com/nautobot/nautobot-app-capacity-metrics/develop/docs/images/capacity-metrics-screenshot-04.png "Prefix Capacity")
