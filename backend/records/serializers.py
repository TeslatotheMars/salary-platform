from rest_framework import serializers
from .models import SalaryRecord, EXPERIENCE_CHOICES

class SalaryRecordCreateSerializer(serializers.Serializer):
    university = serializers.CharField(max_length=255)
    major = serializers.CharField(max_length=255)
    industry = serializers.CharField(max_length=255)
    occupation = serializers.CharField(max_length=255)
    experience_category = serializers.ChoiceField(choices=[c[0] for c in EXPERIENCE_CHOICES])
    city = serializers.CharField(max_length=128)
    salary_eur = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)

class SalaryRecordSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.user_id", read_only=True)

    class Meta:
        model = SalaryRecord
        fields = [
            "record_id","user_id","university","major","industry","occupation",
            "experience_category","city","salary_eur","submission_date"
        ]
