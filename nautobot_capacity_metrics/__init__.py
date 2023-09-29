"""Plugin declaration for nautobot_capacity_metrics."""

__version__ = "1.1.1"

from nautobot.extras.plugins import PluginConfig

# Registry of functions that can generate additional application metrics
# All functions in the registry should take no argument and return an Iterator (or list) of prometheus Metric Object
# The Registry can be populated from the configuration file or using register_metric_func()
__REGISTRY__ = []


def register_metric_func(func):
    """Register an additional function to generate application metrics.

    Args:
        func: python function, taking no argument that return a list of Prometheus Metric Object
    """
    if not callable(func):
        raise TypeError(
            f"Trying to register a {type(func)} into the application metric registry, only function (callable) are supporter"
        )

    __REGISTRY__.append(func)


class MetricsExtConfig(PluginConfig):
    """Plugin configuration for the nautobot_capacity_metrics plugin."""

    name = "nautobot_capacity_metrics"
    verbose_name = "Data, Metrics, and Monitoring Prometheus Endpoints"
    version = __version__
    author = "Network to Code, LLC"
    author_email = "opensource@networktocode.com"
    description = "Lightweight Nautobot App to expose additional metrics as Prometheus endpoints. Includes exposing Nautobot object data and metrics that can be collected and later viewed in Visualization tools."
    base_url = "capacity-metrics"
    required_settings = []
    min_version = "1.4.0"
    max_version = "1.9999"
    default_settings = {
        "app_metrics": {
            "models": {
                "dcim": {
                    "Site": True,
                    "Rack": True,
                    "Device": True,
                },
                "ipam": {"IPAddress": True, "Prefix": True},
            },
            "jobs": True,
            "queues": True,
            "versions": {
                "basic": False,
                "plugins": False,
            },
        }
    }
    caching_config = {}


config = MetricsExtConfig  # pylint:disable=invalid-name
