from django.urls import path
from .views import dashboard_options, dashboard_summary, dashboard_grouped, dashboard_distribution, dashboard_compare

urlpatterns = [
    path("dashboard/options", dashboard_options),
    path("dashboard/summary", dashboard_summary),
    path("dashboard/grouped", dashboard_grouped),
    path("dashboard/distribution", dashboard_distribution),
    path("dashboard/compare", dashboard_compare),
]
