from django.urls import path
from .views import PatientListView, PatientDetailView

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<uuid:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
]