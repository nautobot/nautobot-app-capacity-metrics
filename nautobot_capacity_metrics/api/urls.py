"""Django URL patterns for nautobot_capacity_metrics app."""

from django.conf import settings
from django.urls import path

from . import views

if hasattr(settings, "METRICS_AUTHENTICATED") and settings.METRICS_AUTHENTICATED:
    urlpatterns = [
        path("app-metrics", views.AppMetricsViewAuth.as_view(), name="nautobot_capacity_metrics_app_view"),
    ]
else:
    urlpatterns = [
        path("app-metrics", views.AppMetricsView.as_view(), name="nautobot_capacity_metrics_app_view"),
    ]
