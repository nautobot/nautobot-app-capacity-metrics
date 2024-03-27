"""Test cases for nautobot_capacity_metrics views."""

from django.test import RequestFactory
from django.urls import reverse
from nautobot.core.testing import TestCase
from nautobot.core.testing.api import APITestCase

from nautobot_capacity_metrics.api.views import AppMetricsView


class AppMetricEndpointTests(TestCase):
    """Test cases for ensuring application metric endpoint is working properly."""

    app_metric_url = reverse("plugins-api:nautobot_capacity_metrics-api:nautobot_capacity_metrics_app_view")

    def query_and_parse_metrics(self):
        response = self.client.get(self.app_metric_url)
        self.assertHttpStatus(
            response, 200, msg="/api/plugins/capacity-metrics/app-metrics should return a 200 HTTP status code."
        )
        return response.content.decode(response.charset)

    def test_metrics_extensibility(self):
        """Assert that the example metric from the example plugin shows up _exactly_ when the plugin is enabled."""
        test_metric_name = "TestModel"
        app_metrics = self.query_and_parse_metrics()
        self.assertIn(test_metric_name, app_metrics)


class AuthenticateMetricsTestCase(
    APITestCase
):  # noqa pylint: disable=too-many-ancestors,attribute-defined-outside-init
    """Test that metric authentication works."""

    def test_metrics_authentication(self):
        """Assert that if metrics require authentication, a user not logged in gets a 403."""
        self.client.logout()
        headers = {}
        response = self.client.get(
            reverse("plugins-api:nautobot_capacity_metrics-api:nautobot_capacity_metrics_app_view"), **headers
        )
        self.assertHttpStatus(
            response, 403, msg="/api/plugins/capacity-metrics/app-metrics should return a 403 HTTP status code."
        )

    def test_metrics(self):
        """Assert that if metrics don't require authentication, a user not logged in gets a 200."""
        self.factory = RequestFactory()
        self.client.logout()

        request = self.factory.get("/")
        response = AppMetricsView.as_view()(request)
        self.assertHttpStatus(
            response, 200, msg="/api/plugins/capacity-metrics/app-metrics should return a 200 HTTP status code."
        )
