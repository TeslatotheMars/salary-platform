from django.db import models
from accounts.models import Person
from admin_import.models import ImportBatch

EXPERIENCE_CHOICES = [
    ("under 1 year", "under 1 year"),
    ("1-3 years", "1-3 years"),
    ("3-5 years", "3-5 years"),
    ("5-10 years", "5-10 years"),
    ("above 10 years", "above 10 years"),
]

class SalaryRecord(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="salary_records")
    batch = models.ForeignKey(ImportBatch, on_delete=models.SET_NULL, null=True, blank=True, related_name="records")

    university = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    experience_category = models.CharField(max_length=32, choices=EXPERIENCE_CHOICES)

    city = models.CharField(max_length=128)
    salary_eur = models.DecimalField(max_digits=12, decimal_places=2)

    submission_date = models.DateTimeField()  # server assigned
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["industry"]),
            models.Index(fields=["occupation"]),
            models.Index(fields=["major"]),
            models.Index(fields=["university"]),
            models.Index(fields=["experience_category"]),
            models.Index(fields=["salary_eur"]),
            models.Index(fields=["submission_date"]),
            models.Index(fields=["user", "submission_date"]),
            models.Index(fields=["batch"]),
        ]

    def __str__(self):
        return f"Record({self.record_id}) user={self.user_id} {self.salary_eur} EUR"
