from django.contrib import admin
from .models import SalaryRecord

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ("record_id","user","city","industry","occupation","salary_eur","submission_date","deleted_at","batch")
    search_fields = ("record_id","user__user_id","city","industry","occupation","university","major")
    list_filter = ("city","industry","experience_category","deleted_at","batch")
