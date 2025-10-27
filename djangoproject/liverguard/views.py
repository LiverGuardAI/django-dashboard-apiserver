from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Patients
from .serializers import PatientSerializer

class TestView(APIView):
    def get(self, request):
        return Response({"message": "LiverGuard API is running!"})
# Create your views here.

# 환자 목록 조회 (GET /api/patients/)
class PatientListView(generics.ListAPIView):
    queryset = Patients.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer

# 단일 환자 조회 (GET /api/patients/<patient_id>/)
class PatientDetailView(generics.RetrieveAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'