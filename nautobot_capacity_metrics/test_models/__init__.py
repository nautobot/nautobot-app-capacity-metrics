"""Plugin declaration for nautobot_capacity_metrics.test_models.

Why is this here? In order to test the plugin model count metric mechanics, a plugin metric had to be introduced.
This was put into a separate app so that it is not installed whenever this plugin is installed, rather just when tests
are ran within this plugins development environment.
"""

__version__ = "1.0.0"

from nautobot.extras.plugins import PluginConfig


class TestConfig(PluginConfig):
    """Plugin configuration for the nautobot_capacity_metrics plugin."""

    name = "nautobot_capacity_metrics.test_models"
    verbose_name = "Metrics & Monitoring Extension Test Model Plugin"
    version = __version__
    author = "Network to Code, LLC"
    author_email = "opensource@networktocode.com"
    description = "Plugin that exists solely to test nautobot_capacity_metrics, don't install.."
    base_url = "capacity-metrics-test"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.99.99"
    default_settings = {}
    caching_config = {}


config = TestConfig  # pylint:disable=invalid-name
