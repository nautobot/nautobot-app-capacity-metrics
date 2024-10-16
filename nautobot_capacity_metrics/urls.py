"""Django urlpatterns declaration for nautobot_capacity_metrics app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_capacity_metrics/docs/index.html")), name="docs"),
]
