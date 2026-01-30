from django.urls import path
from .views import create_import, list_imports, download_failures, delete_record_admin, delete_batch

urlpatterns = [
    path("admin/imports", create_import),
    path("admin/imports/list", list_imports),
    path("admin/imports/<int:batch_id>/failures", download_failures),
    path("admin/records/<int:record_id>", delete_record_admin),
    path("admin/imports/<int:batch_id>", delete_batch),
]
