from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/", include("records.urls")),
    path("api/", include("dashboard.urls")),
    path("api/", include("admin_import.urls")),
]
