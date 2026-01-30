from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("audit_id", "created_at", "actor", "action", "target_type", "target_id")
    search_fields = ("action", "target_type", "target_id", "actor__email")
    list_filter = ("action", "target_type", "created_at")
