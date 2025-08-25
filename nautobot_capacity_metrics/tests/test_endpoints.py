"""Test cases for nautobot_capacity_metrics views."""

from django.test import TestCase
from django.urls import reverse
from nautobot.extras.models import Tag
from rest_framework import status
from rest_framework.test import APIClient


class AppMetricEndpointTests(TestCase):
    """Test cases for ensuring application metric endpoint is working properly."""

    app_metric_url = reverse("plugins-api:nautobot_capacity_metrics-api:nautobot_capacity_metrics_app_view")

    def test_endpoint(self):
        """Ensure the endpoint is working properly and is not protected by authentication."""
        client = APIClient()
        resp = client.get(self.app_metric_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_model_count_metrics(self):
        """Ensure that the model count metrics work correctly."""

        Tag.objects.create(name="cap-metrics")

        resp = self.client.get(self.app_metric_url)
        if "Tag" not in resp.content.decode("utf-8"):
            self.fail("extras.Tag does not report its count.")
