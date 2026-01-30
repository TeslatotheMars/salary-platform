from .models import AuditLog

def log_action(actor, action: str, target_type: str, target_id: str = "", metadata: dict | None = None):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=str(target_id) if target_id is not None else "",
        metadata=metadata or {},
    )
