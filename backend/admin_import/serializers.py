from rest_framework import serializers
from .models import ImportBatch

class ImportBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportBatch
        fields = ["batch_id","status","filename","rows_total","rows_success","rows_failed","created_at"]
