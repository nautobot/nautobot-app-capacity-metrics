"""Django urlpatterns declaration for nautobot_capacity_metrics app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter


# Uncomment the following line if you have views to import
# from nautobot_capacity_metrics import views


app_name = "nautobot_capacity_metrics"
router = NautobotUIViewSetRouter()

# Here is an example of how to register a viewset, you will want to replace views.NautobotCapacityMetricsUIViewSet with your viewset
# router.register("nautobot_capacity_metrics", views.NautobotCapacityMetricsUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_capacity_metrics/docs/index.html")), name="docs"),
]
