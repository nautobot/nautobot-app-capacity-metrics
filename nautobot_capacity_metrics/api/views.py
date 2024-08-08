"""Django views for Prometheus metric collection and reporting."""  # pylint:  disable=too-few-public-methods

import logging
import time

import prometheus_client
from django.conf import settings
from django.http import HttpResponse
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily

from nautobot_capacity_metrics import __REGISTRY__
from nautobot_capacity_metrics.metrics import (
    collect_extras_metric,
    metric_jobs,
    metric_models,
    metric_versions,
)

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


def AppMetricsView(request):  # pylint: disable=invalid-name
    """Exports /api/plugins/capacity-metrics/app-metrics as a Django view."""
    registry = CollectorRegistry()
    collector = AppMetricsCollector()
    registry.register(collector)
    metrics_page = prometheus_client.generate_latest(registry)
    return HttpResponse(metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST)
