"""Django views for Prometheus metric collection and reporting."""  # pylint:  disable=too-few-public-methods

import logging
import re
import time

import prometheus_client
from django.conf import settings
from django.utils.encoding import smart_str
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework.views import APIView

from nautobot_capacity_metrics import __REGISTRY__
from nautobot_capacity_metrics.metrics import collect_extras_metric, metric_jobs, metric_models, metric_versions

logger = logging.getLogger(__name__)
PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_capacity_metrics"]["app_metrics"]


class AppMetricsCollector:
    """Collector class for collecting app and extras application metrics."""

    def collect(self):
        """Collect metrics for all apps and extras."""
        start = time.time()

        if "gitrepositories" in PLUGIN_SETTINGS and PLUGIN_SETTINGS["gitrepositories"]:
            for metric in metric_jobs(type_of_job="git_repository"):
                yield metric

        if "jobs" in PLUGIN_SETTINGS and PLUGIN_SETTINGS["jobs"]:
            for metric in metric_jobs(type_of_job="job"):
                yield metric

        if "models" in PLUGIN_SETTINGS:
            for metric in metric_models(PLUGIN_SETTINGS["models"]):
                yield metric

        if "versions" in PLUGIN_SETTINGS and (
            PLUGIN_SETTINGS["versions"]["basic"] or PLUGIN_SETTINGS["versions"]["plugins"]
        ):
            for metric in metric_versions():
                yield metric

        # --------------------------------------------------------------
        # Extras Function defined in configuration.py or the Regristry
        # # --------------------------------------------------------------
        if "extras" in PLUGIN_SETTINGS:
            for metric in collect_extras_metric(PLUGIN_SETTINGS["extras"]):
                yield metric

        for metric in collect_extras_metric(__REGISTRY__):
            yield metric

        gauge = GaugeMetricFamily(
            "nautobot_app_metrics_processing_ms", "Time in ms to generate the app metrics endpoint"
        )
        duration = time.time() - start
        gauge.add_metric([], format(duration * 1000, ".5f"))
        yield gauge


class PrometheusVersioning(AcceptHeaderVersioning):
    """Overwrite the Nautobot API Version with the prometheus API version. Otherwise Telegraf/Prometheus won't be able to poll due to a version mismatch."""

    default_version = re.findall("version=(.+);", prometheus_client.CONTENT_TYPE_LATEST)[0]


class PlainTextRenderer(BaseRenderer):
    """Render API as plain text instead of JSON."""

    media_type = "text/plain"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render the data."""
        return smart_str(data, encoding=self.charset)


class AppMetricsView(APIView):
    """App Metrics that render properly for Prometheus collection."""

    renderer_classes = [PlainTextRenderer]
    versioning_class = PrometheusVersioning
    permission_classes = [AllowAny]
    serializer_class = None

    def get(self, request):
        """Exports /api/plugins/capacity-metrics/app-metrics as a Django view."""
        registry = CollectorRegistry()
        collector = AppMetricsCollector()
        registry.register(collector)
        metrics_page = prometheus_client.generate_latest(registry)
        return Response(metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST)


class AppMetricsViewAuth(AppMetricsView):
    """Require authentication to get to /api/plugins/capacity-metrics/app-metrics."""

    permission_classes = [IsAuthenticated]
