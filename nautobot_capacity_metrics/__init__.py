"""App declaration for nautobot_capacity_metrics."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata
from typing import Callable

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotCapacityMetricsConfig(NautobotAppConfig):
    """App configuration for the nautobot_capacity_metrics app."""

    name = "nautobot_capacity_metrics"
    verbose_name = "Metrics & Monitoring Extension App"
    version = __version__
    author = "Network to Code, LLC"
    description = "App to improve the instrumentation of Nautobot and expose additional metrics (Application Metrics, RQ Worker).."
    base_url = "capacity-metrics"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
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


config = NautobotCapacityMetricsConfig  # pylint:disable=invalid-name
