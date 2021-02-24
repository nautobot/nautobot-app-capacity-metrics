"""Django views for Prometheus metric collection and reporting."""
import time
import logging

from django.conf import settings
from django.http import HttpResponse

import prometheus_client
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily

from nautobot_capacity_metrics import __REGISTRY__
from nautobot_capacity_metrics.metrics import collect_extras_metric, metric_jobs, metric_models, metric_rq

logger = logging.getLogger(__name__)
PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_capacity_metrics"]["app_metrics"]


class AppMetricsCollector:
    """Collector class for collecting plugin and extras application metrics."""

    def collect(self):  # pylint: disable=no-self-use
        """Collect metrics for all plugins and extras."""
        start = time.time()

        if "jobs" in PLUGIN_SETTINGS and PLUGIN_SETTINGS["jobs"]:
            for metric in metric_jobs():
                yield metric

        if "models" in PLUGIN_SETTINGS:
            for metric in metric_models(PLUGIN_SETTINGS["models"]):
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


class QueueMetricsCollector:
    """Collector class for collecting django rq related metrics metrics."""

    def collect(self):  # pylint: disable=no-self-use
        """Collect metrics for all plugins and extras."""
        start = time.time()
        for metric in metric_rq():
            yield metric

        gauge = GaugeMetricFamily(
            "nautobot_rq_metrics_processing_ms", "Time in ms to generate the app metrics endpoint"
        )
        duration = time.time() - start
        gauge.add_metric([], format(duration * 1000, ".5f"))
        yield gauge


def ExportToDjangoView(request, view=""):  # pylint: disable=invalid-name
    """Exports /api/plugins/capacity-metrics/[app|rq]-metrics as a Django view."""
    registry = CollectorRegistry()
    if view == "rq-metrics":
        collector = QueueMetricsCollector()
        registry.register(collector)
    elif view == "app-metrics":
        collector = AppMetricsCollector()
        registry.register(collector)
    metrics_page = prometheus_client.generate_latest(registry)
    return HttpResponse(metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST)


def QueueMetricsView(request):  # pylint: disable=invalid-name
    """Exports /api/plugins/capacity-metrics/rq-metrics as a Django view."""
    return ExportToDjangoView(request, view="rq-metrics")


def AppMetricsView(request):  # pylint: disable=invalid-name
    """Exports /api/plugins/capacity-metrics/app-metrics as a Django view."""
    return ExportToDjangoView(request, view="app-metrics")
