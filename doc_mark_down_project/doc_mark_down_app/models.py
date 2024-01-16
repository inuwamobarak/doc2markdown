from django.db import models

class ProcessedDocument(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='processed_documents/')
    created_at = models.DateTimeField(auto_now_add=True)
