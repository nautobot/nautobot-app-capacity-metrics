"""Django URL patterns for nautobot_capacity_metrics plugin."""

from django.conf import settings
from django.urls import path
from . import views

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_capacity_metrics"]["app_metrics"]

urlpatterns = [
    path("app-metrics", views.AppMetricsView, name="nautobot_capacity_metrics_app_view"),
]
