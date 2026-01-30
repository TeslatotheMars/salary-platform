from django.contrib import admin
from .models import ImportBatch, ImportFailureRow

@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_id","status","filename","rows_total","rows_success","rows_failed","created_at")
    list_filter = ("status","created_at")
    search_fields = ("filename",)

@admin.register(ImportFailureRow)
class ImportFailureRowAdmin(admin.ModelAdmin):
    list_display = ("id","batch","row_number","error")
    search_fields = ("error",)
