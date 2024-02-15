"""Metrics libraries for the nautobot_capacity_metrics app."""
import logging
import importlib
import platform
from collections.abc import Iterable
from copy import deepcopy

import django
from packaging import version
from django.conf import settings

from prometheus_client.core import Metric, GaugeMetricFamily

from nautobot.extras.choices import JobResultStatusChoices


logger = logging.getLogger(__name__)

nautobot_version = version.parse(settings.VERSION)

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_capacity_metrics"]["app_metrics"]


def metric_jobs(type_of_job):
    """Return Jobs results in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_job_task_stats: with jobs module, name, task name and status as labels
        Iterator[GaugeMetricFamily]
            nautobot_job_execution_status: with jobs module the name and overall status of the job
    """
    from nautobot.extras.models import JobResult  # pylint: disable=import-outside-toplevel,no-name-in-module

    git_repo_job_prefix = "nautobot.core.jobs.GitRepository"

    # Get the latest result for each job
    if type_of_job == "job":
        job_results = (
            JobResult.objects.exclude(task_name__startswith=git_repo_job_prefix)
            .order_by("name", "-date_done")
            .distinct("name")
        )
    elif type_of_job == "git_repository":
        job_results = (
            JobResult.objects.filter(task_name__startswith=git_repo_job_prefix)
            .order_by("name", "-date_done")
            .distinct("name")
        )
    else:
        raise ValueError(f"Unknown type of job {type_of_job} - choose from 'job' or 'git_repository.")

    # Each Job can have multiple jobs (tasks) with individual statistics success, warning, failure,
    # info the stats gauge exposes these
    task_stats_gauge = GaugeMetricFamily(
        f"nautobot_{type_of_job}_task_stats",
        f"Per {type_of_job.title()} task statistics",
        labels=["module", "name", "status"],
    )

    # Each job has an overall status, one status per high level job not per task, which is one of pending,
    # running, completed, errored or failed as defined in the JobResultStatusChoices class
    execution_status_gauge = GaugeMetricFamily(
        f"nautobot_{type_of_job}_execution_status",
        f"{type_of_job.title()} completion status",
        labels=["module", "status"],
    )

    for job in job_results:
        # Add metrics for the overall job status
        for status_name, _ in JobResultStatusChoices:
            if job.status == status_name:
                execution_status_gauge.add_metric([job.name, status_name], 1)
            else:
                execution_status_gauge.add_metric([job.name, status_name], 0)

    yield task_stats_gauge
    yield execution_status_gauge


def metric_models(params):
    """Return Models count in Prometheus Metric format.

    Args:
        params (dict): list of models to return organized per application

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_model_count: with model name and application name as labels
    """
    for app in params:
        app_config = deepcopy(params[app])  # Avoid changing the dictionary we are iterating over
        module = app_config.pop("_module", "nautobot")
        for model, additional_fields in app_config.items():
            try:
                models = importlib.import_module(f"{module}.{app}.models")
                model_class = getattr(models, model)
            except ModuleNotFoundError:
                logger.warning("Unable to find the python library %s.models", app)
                continue
            except AttributeError:
                logger.warning("Unable to load the module %s from the python library %s.models", model, app)
                continue

            # Prepare the queryset, prefetching any related fields that are necessary
            if not isinstance(additional_fields, list):
                additional_fields = []
            prefetch_related = [field.split("__", maxsplit=1)[0] for field in additional_fields]
            queryset = model_class.objects.prefetch_related(*prefetch_related).order_by()

            # Default without any filtering by addition fields
            gauge = GaugeMetricFamily(
                f"nautobot_model_count_{model.lower()}_total", "Nautobot model count", labels=["app"]
            )
            gauge.add_metric([app], queryset.count())
            yield gauge

            for additional_field in additional_fields:
                yield from _individual_model_metric(additional_field, app, model, queryset)


def _individual_model_metric(by_field, app, model, queryset):
    """Yield an individual metric for the metric_models generator."""
    path = by_field.split("__")
    related_model_name = path[-2]
    gauge = GaugeMetricFamily(
        f"nautobot_model_count_{model.lower()}_by_{related_model_name}_total",
        f"Nautobot {model.lower()} count per {related_model_name}",
        labels=["app", related_model_name],
    )
    related_fields = queryset.values_list(by_field, flat=True).distinct()
    for field in related_fields:
        if field is None:
            continue
        filtered_queryset = queryset.filter(**{by_field: field})
        gauge.add_metric([app, field], filtered_queryset.count())
        yield gauge


def metric_versions():
    """Return django, Nautobot, Python and app versions in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_app_versions: the versions as labels
    """
    versions = {}
    if PLUGIN_SETTINGS["versions"]["basic"]:
        versions.update(
            {"python": platform.python_version(), "django": django.get_version(), "nautobot": settings.VERSION}
        )

    # Collect app versions
    if PLUGIN_SETTINGS["versions"]["plugins"]:
        for app in settings.PLUGINS:
            try:
                app_module = importlib.import_module(app)
            except ModuleNotFoundError:
                logger.warning("Unable to find the python library %s", app)
                continue
            try:
                versions[app] = app_module.__version__
            except AttributeError:
                logger.warning("Module %s does not have __version__ defined.", app)
    gauge = GaugeMetricFamily("nautobot_app_versions", "Nautobot app versions", labels=versions.keys())
    gauge.add_metric(versions.values(), 1)
    yield gauge


def collect_extras_metric(funcs):
    """Collect Third party functions to generate additional Metrics.

    Args:
        funcs (list): list of functions to execute

    Return:
        List[GaugeMetricFamily]
            nautobot_model_count: with model name and application name as labels
    """
    for func in funcs:
        if not callable(func):
            logger.warning("Extra metric is not a function, skipping ... ")
            continue

        results = func()

        if not isinstance(results, Iterable):
            logger.warning("Extra metric didn't return a list, skipping ... ")
            continue

        for metric in results:
            if Metric not in type(metric).__bases__:
                logger.warning("Extra metric didn't return a Metric object, skipping ... ")
                continue
            yield metric
