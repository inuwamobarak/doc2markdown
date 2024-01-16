# doc_mark_down_app/urls.py
from django.urls import path
from .views import ProcessedDocumentListCreateView, ProcessedDocumentRetrieveView

urlpatterns = [
    path('processed_documents/', ProcessedDocumentListCreateView.as_view(), name='processed-document-list-create'),
    path('processed_documents/<int:pk>/', ProcessedDocumentRetrieveView.as_view(), name='processed-document-retrieve'),
]