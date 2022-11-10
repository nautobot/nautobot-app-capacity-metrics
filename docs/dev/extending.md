# Extending the App

Extending the application is welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of features and design.

## Add your own metrics

This plugin supports some options to generate and publish your own application metrics behind the same endpoint.

### Option 1 - Register function(s) via `nautobot_config.py`

It's possible to create your own function to generate some metrics and register it to the plugin in the `nautobot_config.py`. Here is an example where the custom functions are centralized in a `metrics.py` file, located next to the main `nautobot_config.py`.

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

The new function can be imported in the `nautobot_config.py` file and registered with the plugin.

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

### Option 2 - Registry for third party plugins

Any plugin can include its own metrics to improve the visibility and/or the troubleshooting of the plugin itself.
Third party plugins can register their own function(s) using the `ready()` function as part of their `PluginConfig` class.

```python
# my_plugin/__init__.py
from nautobot_capacity_metrics import register_metric_func
from nautobot.metrics import metric_circuit_bandwidth

class MyPluginConfig(PluginConfig):
    name = "nautobot_myplugin"
    verbose_name = "Demo Plugin"
    # [ ... ]
    def ready(self):
        super().ready()
        register_metric_func(metric_circuit_bandwidth)
```

### Option 3 - `NOT AVAILABLE YET` - Metrics directory

In the future it will be possible to add metrics by adding them in a predefined directory, similar to jobs.
