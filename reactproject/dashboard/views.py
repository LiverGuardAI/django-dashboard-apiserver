from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import DbrPatients, DbrBloodResults, DbrAppointments, DbrBloodTestReferences, Announcements
from .serializers import (
    PatientSerializer, BloodResultSerializer, AppointmentSerializer,
    BloodTestReferenceSerializer, AnnouncementSerializer, 
    DbrPatientRegisterSerializer, DbrPatientLoginSerializer,
)
from dashboard.authentication import PatientJWTAuthentication
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Auth view
# sign up view
class DbrPatientRegisterView(APIView):
    def post(self, request):
        serializer = DbrPatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            print("❌ Serializer errors:", serializer.errors)  # 🔥 여기에 실제 원인 표시
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login view
class DbrPatientLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = DbrPatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        print("❌ Login Serializer errors:", serializer.errors)  # 🔥 여기에 실제 원인 표시
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# logout view
class DbrPatientLogoutView(APIView):
    """
    JWT 로그아웃 (Refresh Token 무효화)
    """
    authentication_classes = [PatientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "refresh token이 필요합니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            # token.blacklist()  # ✅ 블랙리스트에 등록 (재사용 불가)

            return Response(
                {"message": "로그아웃되었습니다."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError:
            return Response(
                {"error": "유효하지 않은 refresh token입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
# 🔹 현재 로그인된 사용자 조회 (auth/user)
class DbrPatientUserView(APIView):
    authentication_classes = [PatientJWTAuthentication]  # ✅ 커스텀 인증
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "patient_id": str(user.patient_id),
            "user_id": user.user_id,
            "name": user.name,
            "sex": user.sex,
            "phone": user.phone,
        })

# ==================== 환자 관련 Views ====================
class PatientListView(generics.ListCreateAPIView):
    """환자 목록 조회 및 생성"""
    queryset = DbrPatients.objects.all()
    serializer_class = PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """환자 상세 조회, 수정, 삭제"""
    queryset = DbrPatients.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'


# ==================== 혈액검사 관련 Views ====================
class BloodResultListView(generics.ListCreateAPIView):
    """혈액검사 결과 목록 조회 및 생성"""
    queryset = DbrBloodResults.objects.all().select_related('patient')
    serializer_class = BloodResultSerializer


class BloodResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    """혈액검사 결과 상세 조회, 수정, 삭제"""
    queryset = DbrBloodResults.objects.all().select_related('patient')
    serializer_class = BloodResultSerializer
    lookup_field = 'blood_result_id'


class PatientBloodResultsView(generics.ListAPIView):
    """특정 환자의 혈액검사 결과 목록 조회"""
    serializer_class = BloodResultSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return DbrBloodResults.objects.filter(patient_id=patient_id).order_by('-taken_at')


# ==================== 일정 관련 Views ====================
class AppointmentListView(generics.ListCreateAPIView):
    """일정 목록 조회 및 생성"""
    queryset = DbrAppointments.objects.all().select_related('patient')
    serializer_class = AppointmentSerializer


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """일정 상세 조회, 수정, 삭제"""
    queryset = DbrAppointments.objects.all().select_related('patient')
    serializer_class = AppointmentSerializer
    lookup_field = 'appointment_id'


class PatientAppointmentsView(generics.ListAPIView):
    """특정 환자의 일정 목록 조회"""
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return DbrAppointments.objects.filter(patient_id=patient_id).order_by('appointment_date', 'appointment_time')


# ==================== 혈액검사 기준 관련 Views ====================
class BloodTestReferenceListView(generics.ListCreateAPIView):
    """혈액검사 기준 목록 조회 및 생성"""
    queryset = DbrBloodTestReferences.objects.all()
    serializer_class = BloodTestReferenceSerializer


class BloodTestReferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """혈액검사 기준 상세 조회, 수정, 삭제"""
    queryset = DbrBloodTestReferences.objects.all()
    serializer_class = BloodTestReferenceSerializer
    lookup_field = 'reference_id'


# ==================== 공지사항 관련 Views ====================
class AnnouncementListView(generics.ListCreateAPIView):
    """공지사항 목록 조회 및 생성"""
    queryset = Announcements.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """공지사항 상세 조회, 수정, 삭제"""
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    lookup_field = 'announcements_id'


