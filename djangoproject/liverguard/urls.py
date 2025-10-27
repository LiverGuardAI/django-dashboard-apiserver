from django.urls import path
from .views import TestView
from .views import PatientListView, PatientDetailView

urlpatterns = [
    path('test/', TestView.as_view()),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<uuid:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
]