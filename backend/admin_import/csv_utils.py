import csv
from io import TextIOWrapper
from decimal import Decimal
from django.utils import timezone

from accounts.models import Person
from records.models import SalaryRecord, EXPERIENCE_CHOICES

EXPERIENCE_SET = set([c[0] for c in EXPERIENCE_CHOICES])

REQUIRED_FIELDS = ["email","University","Major","Industry","Occupation","Experience","City","Salary","Submission_Date"]

def parse_date(s: str):
    # Accept common formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY (best-effort)
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            from datetime import datetime
            dt = datetime.strptime(s, fmt)
            return timezone.make_aware(dt)
        except Exception:
            pass
    return None

def import_csv(file_obj, batch, admin_user):
    wrapper = TextIOWrapper(file_obj, encoding="utf-8-sig")
    reader = csv.DictReader(wrapper)
    rows = list(reader)
    batch.rows_total = len(rows)
    batch.save(update_fields=["rows_total"])

    successes = 0
    failures = []

    for idx, row in enumerate(rows, start=2):  # header is row 1
        try:
            # Basic required fields
            for f in REQUIRED_FIELDS:
                if f not in row:
                    raise ValueError(f"Missing column: {f}")

            email = (row.get("email") or "").strip() or None
            uni = (row.get("University") or "").strip()
            major = (row.get("Major") or "").strip()
            industry = (row.get("Industry") or "").strip()
            occupation = (row.get("Occupation") or "").strip()
            exp = (row.get("Experience") or "").strip()
            city = (row.get("City") or "").strip()
            salary_raw = (row.get("Salary") or "").strip()
            sub_date_raw = (row.get("Submission_Date") or "").strip()

            if exp not in EXPERIENCE_SET:
                raise ValueError(f"Invalid Experience: {exp}")
            if not all([uni, major, industry, occupation, city, salary_raw]):
                raise ValueError("Empty required field")

            try:
                salary = Decimal(salary_raw)
            except Exception:
                raise ValueError(f"Invalid Salary: {salary_raw}")
            if salary <= 0:
                raise ValueError("Salary must be positive")

            sub_dt = parse_date(sub_date_raw) or timezone.now()

            # Create Person (consumes global user_id)
            person = Person.objects.create(email=email)

            SalaryRecord.objects.create(
                user=person,
                batch=batch,
                university=uni,
                major=major,
                industry=industry,
                occupation=occupation,
                experience_category=exp,
                city=city,
                salary_eur=salary,
                submission_date=sub_dt,
            )
            successes += 1
        except Exception as e:
            failures.append((idx, str(e), row))

    return successes, failures
