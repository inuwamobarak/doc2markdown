# doc_mark_down_app/serializers.py
from rest_framework import serializers
from .models import ProcessedDocument

class ProcessedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedDocument
        fields = '__all__'