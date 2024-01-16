from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.response import Response
from .models import ProcessedDocument
from .serializers import ProcessedDocumentSerializer
from .nougat_inference import process_document  # Add the inference function here

class ProcessedDocumentListCreateView(generics.ListCreateAPIView):
    queryset = ProcessedDocument.objects.all()
    serializer_class = ProcessedDocumentSerializer

    def perform_create(self, serializer):
        file_path = process_document(serializer.validated_data['pdf_file'])
        serializer.save(file_path=file_path)

class ProcessedDocumentRetrieveView(generics.RetrieveAPIView):
    queryset = ProcessedDocument.objects.all()
    serializer_class = ProcessedDocumentSerializer