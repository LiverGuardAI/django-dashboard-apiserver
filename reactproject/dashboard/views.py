from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Patients
from .serializers import PatientSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password


class PatientListView(generics.ListCreateAPIView):
    """환자 목록 조회 및 생성"""
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """환자 상세 조회, 수정, 삭제"""
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'
