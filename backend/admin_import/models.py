from django.db import models
from django.conf import settings

class ImportBatch(models.Model):
    batch_id = models.BigAutoField(primary_key=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="import_batches")
    filename = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=16, default="RUNNING")  # RUNNING|SUCCESS|PARTIAL|FAILED
    rows_total = models.IntegerField(default=0)
    rows_success = models.IntegerField(default=0)
    rows_failed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ImportFailureRow(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE, related_name="failures")
    row_number = models.IntegerField()
    error = models.CharField(max_length=255)
    raw = models.JSONField(default=dict, blank=True)
