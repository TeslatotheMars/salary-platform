from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsAuthenticatedUser
from accounts.models import Person
from audit.services import log_action

from .models import SalaryRecord
from .serializers import SalaryRecordCreateSerializer, SalaryRecordSerializer
from .services import enforce_yearly_limit, UploadLimitReached

@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def my_submissions(request):
    year = request.query_params.get("year")
    qs = SalaryRecord.objects.filter(user_id=request.user.uid, deleted_at__isnull=True).order_by("-submission_date")
    if year:
        qs = qs.filter(submission_date__year=int(year))
    data = SalaryRecordSerializer(qs[:500], many=True).data  # simple cap for MVP
    return Response({"count": len(data), "results": data})

@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def submit_record(request):
    ser = SalaryRecordCreateSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    try:
        year, cnt = enforce_yearly_limit(request.user.uid)
    except UploadLimitReached as e:
        year = int(e.args[0]) if e.args else timezone.localtime(timezone.now()).year
        return Response({
            "error": "UPLOAD_LIMIT_REACHED",
            "message": "You can submit at most 2 records per calendar year.",
            "year": year
        }, status=status.HTTP_403_FORBIDDEN)

    now = timezone.now()  # stored in UTC, displayed in localtime on frontend if desired
    record = SalaryRecord.objects.create(
        user_id=request.user.uid,
        university=ser.validated_data["university"].strip(),
        major=ser.validated_data["major"].strip(),
        industry=ser.validated_data["industry"].strip(),
        occupation=ser.validated_data["occupation"].strip(),
        experience_category=ser.validated_data["experience_category"],
        city=ser.validated_data["city"].strip(),
        salary_eur=ser.validated_data["salary_eur"],
        submission_date=now,
    )
    log_action(request.user, "SUBMIT", "SALARY_RECORD", target_id=record.record_id, metadata={"year": year})
    return Response({"record_id": record.record_id, "user_id": request.user.uid, "submission_date": record.submission_date}, status=201)

@api_view(["DELETE"])
@permission_classes([IsAuthenticatedUser])
def delete_my_record(request, record_id: int):
    try:
        record = SalaryRecord.objects.get(record_id=record_id, deleted_at__isnull=True)
    except SalaryRecord.DoesNotExist:
        return Response({"error": "NOT_FOUND"}, status=404)

    if record.user_id != request.user.uid:
        return Response({"error": "FORBIDDEN"}, status=403)

    record.deleted_at = timezone.now()
    record.save(update_fields=["deleted_at"])
    log_action(request.user, "DELETE_RECORD", "SALARY_RECORD", target_id=record_id)
    return Response(status=204)
