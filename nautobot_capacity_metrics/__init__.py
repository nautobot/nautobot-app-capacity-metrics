"""Plugin declaration for nautobot_capacity_metrics."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import NautobotAppConfig


class NautobotCapacityMetricsConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_capacity_metrics plugin."""

    name = "nautobot_capacity_metrics"
    verbose_name = "Metrics & Monitoring Extension Plugin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Plugin to improve the instrumentation of Nautobot and expose additional metrics (Application Metrics, RQ Worker).."
    base_url = "capacity-metrics"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotCapacityMetricsConfig  # pylint:disable=invalid-name
