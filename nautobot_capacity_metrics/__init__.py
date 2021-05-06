"""Plugin declaration for nautobot_capacity_metrics."""

__version__ = "1.0.1"

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
    verbose_name = "Metrics & Monitoring Extension Plugin"
    version = __version__
    author = "Network to Code, LLC"
    author_email = "opensource@networktocode.com"
    description = "Plugin to improve the instrumentation of Nautobot and expose additional metrics (Application Metrics, RQ Worker)."
    base_url = "capacity-metrics"
    required_settings = []
    max_version = "1.9999"
    default_settings = {
        "app_metrics": {
            "models": {
                "nautobot.dcim": {
                    "Site": True,
                    "Rack": True,
                    "Device": True,
                },
                "nautobot.ipam": {"IPAddress": True, "Prefix": True},
            },
            "jobs": True,
            "queues": True,
        }
    }
    caching_config = {}


config = MetricsExtConfig  # pylint:disable=invalid-name
