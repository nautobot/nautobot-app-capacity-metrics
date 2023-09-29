"""Test cases for nautobot_capacity_metrics views."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AppMetricEndpointTests(TestCase):
    """Test cases for ensuring application metric endpoint is working properly."""

    def test_endpoint(self):
        """Ensure the endpoint is working properly and is not protected by authentication."""
        app_metric_url = reverse("plugins-api:nautobot_capacity_metrics-api:nautobot_capacity_metrics_app_view")
        client = APIClient()
        resp = client.get(app_metric_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
