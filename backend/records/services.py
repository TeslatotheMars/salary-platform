from django.utils import timezone
from django.db.models.functions import ExtractYear
from django.db.models import Count
from .models import SalaryRecord

class UploadLimitReached(Exception):
    pass

def submissions_count_for_year(user_id: int, year: int) -> int:
    return SalaryRecord.objects.filter(
        user_id=user_id,
        deleted_at__isnull=True,
        submission_date__year=year,
    ).count()

def enforce_yearly_limit(user_id: int, now=None):
    now = timezone.localtime(now or timezone.now())
    year = now.year
    cnt = submissions_count_for_year(user_id, year)
    if cnt >= 2:
        raise UploadLimitReached(year)
    return year, cnt
