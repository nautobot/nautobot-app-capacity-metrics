"""Django URL patterns for nautobot_capacity_metrics app."""

from django.urls import path

from . import views

urlpatterns = [
    path("app-metrics", views.AppMetricsView, name="nautobot_capacity_metrics_app_view"),
]
