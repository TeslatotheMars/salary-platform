from io import StringIO
import csv

from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import IsAdminRole
from audit.services import log_action
from .models import ImportBatch, ImportFailureRow
from .serializers import ImportBatchSerializer
from .csv_utils import import_csv
from records.models import SalaryRecord

@api_view(["POST"])
@permission_classes([IsAdminRole])
@parser_classes([MultiPartParser, FormParser])
def create_import(request):
    f = request.FILES.get("file")
    if not f:
        return Response({"error": "MISSING_FILE"}, status=400)

    batch = ImportBatch.objects.create(admin=request.user, filename=f.name, status="RUNNING")
    log_action(request.user, "ADMIN_IMPORT", "IMPORT_BATCH", target_id=batch.batch_id, metadata={"filename": f.name})

    with transaction.atomic():
        successes, failures = import_csv(f.file, batch, request.user)

        for row_number, err, raw in failures:
            ImportFailureRow.objects.create(batch=batch, row_number=row_number, error=err[:255], raw=raw)

        batch.rows_success = successes
        batch.rows_failed = len(failures)
        batch.rows_total = successes + len(failures)

        if successes == 0 and failures:
            batch.status = "FAILED"
        elif failures:
            batch.status = "PARTIAL"
        else:
            batch.status = "SUCCESS"
        batch.save(update_fields=["rows_total","rows_success","rows_failed","status"])

    return Response({
        **ImportBatchSerializer(batch).data,
        "failure_report_url": f"/api/admin/imports/{batch.batch_id}/failures" if batch.rows_failed else None
    }, status=201)

@api_view(["GET"])
@permission_classes([IsAdminRole])
def list_imports(request):
    qs = ImportBatch.objects.all().order_by("-created_at")[:200]
    return Response({"results": ImportBatchSerializer(qs, many=True).data})

@api_view(["GET"])
@permission_classes([IsAdminRole])
def download_failures(request, batch_id: int):
    try:
        batch = ImportBatch.objects.get(batch_id=batch_id)
    except ImportBatch.DoesNotExist:
        return Response({"error": "NOT_FOUND"}, status=404)

    failures = ImportFailureRow.objects.filter(batch=batch).order_by("row_number")
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["row_number","error","raw_json"])
    for f in failures:
        writer.writerow([f.row_number, f.error, f.raw])

    return Response(output.getvalue(), content_type="text/csv")

@api_view(["DELETE"])
@permission_classes([IsAdminRole])
def delete_record_admin(request, record_id: int):
    try:
        rec = SalaryRecord.objects.get(record_id=record_id, deleted_at__isnull=True)
    except SalaryRecord.DoesNotExist:
        return Response({"error": "NOT_FOUND"}, status=404)

    rec.deleted_at = timezone.now()
    rec.save(update_fields=["deleted_at"])
    log_action(request.user, "ADMIN_DELETE_RECORD", "SALARY_RECORD", target_id=record_id)
    return Response(status=204)

@api_view(["DELETE"])
@permission_classes([IsAdminRole])
def delete_batch(request, batch_id: int):
    try:
        batch = ImportBatch.objects.get(batch_id=batch_id)
    except ImportBatch.DoesNotExist:
        return Response({"error": "NOT_FOUND"}, status=404)

    SalaryRecord.objects.filter(batch=batch, deleted_at__isnull=True).update(deleted_at=timezone.now())
    batch.delete()
    log_action(request.user, "ADMIN_DELETE_BATCH", "IMPORT_BATCH", target_id=batch_id)
    return Response(status=204)
