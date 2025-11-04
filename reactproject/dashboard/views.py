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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Auth view
# sign up view
class DbrPatientRegisterView(APIView):
    permission_classes = [AllowAny] 
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="환자 회원가입 API",
        operation_summary="회원가입",
        tags=["Auth"],
        request_body=DbrPatientRegisterSerializer,
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                examples={
                    "application/json": {
                        "message": "회원가입이 완료되었습니다."
                    }
                }
            ),
            400: openapi.Response(
                description="입력 데이터 오류",
                examples={
                    "application/json": {
                        "password": ["비밀번호가 일치하지 않습니다."]
                    }
                }
            )
        }
    )
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

    @swagger_auto_schema(
        operation_description="환자 로그인 API - JWT 토큰 발급",
        operation_summary="로그인",
        tags=["Auth"],
        request_body=DbrPatientLoginSerializer,
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "user": {
                            "user_id": "patient123",
                            "name": "홍길동",
                            "sex": "M",
                            "phone": "010-1234-5678"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="로그인 실패",
                examples={
                    "application/json": {
                        "user_id": ["존재하지 않는 사용자입니다."],
                        "password": ["비밀번호가 올바르지 않습니다."]
                    }
                }
            )
        }
    )
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

    @swagger_auto_schema(
        operation_description="환자 로그아웃 API - Refresh Token 무효화",
        operation_summary="로그아웃",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token")
            }
        ),
        responses={
            205: openapi.Response(
                description="로그아웃 성공",
                examples={
                    "application/json": {
                        "message": "로그아웃되었습니다."
                    }
                }
            ),
            400: openapi.Response(
                description="로그아웃 실패",
                examples={
                    "application/json": {
                        "error": "refresh token이 필요합니다."
                    }
                }
            ),
            401: openapi.Response(description="인증 실패")
        },
        security=[{"Bearer": []}]
    )
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

    @swagger_auto_schema(
        operation_description="현재 로그인된 사용자 정보 조회",
        operation_summary="사용자 정보 조회",
        tags=["Auth"],
        responses={
            200: openapi.Response(
                description="사용자 정보 조회 성공",
                examples={
                    "application/json": {
                        "patient_id": "550e8400-e29b-41d4-a716-446655440000",
                        "user_id": "patient123",
                        "name": "홍길동",
                        "sex": "M",
                        "phone": "010-1234-5678"
                    }
                }
            ),
            401: openapi.Response(description="인증 실패")
        },
        security=[{"Bearer": []}]
    )
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

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 등록")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """환자 상세 조회, 수정, 삭제"""
    queryset = DbrPatients.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 상세 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 정보 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 정보 부분 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Patients"], operation_summary="환자 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ==================== 혈액검사 관련 Views ====================
class BloodResultListView(generics.ListCreateAPIView):
    """혈액검사 결과 목록 조회 및 생성"""
    queryset = DbrBloodResults.objects.all().select_related('patient')
    serializer_class = BloodResultSerializer
    authentication_classes = [PatientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 등록")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BloodResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    """혈액검사 결과 상세 조회, 수정, 삭제"""
    queryset = DbrBloodResults.objects.all().select_related('patient')
    serializer_class = BloodResultSerializer
    lookup_field = 'blood_result_id'
    authentication_classes = [PatientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 상세 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 부분 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="혈액검사 결과 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class PatientBloodResultsView(generics.ListAPIView):
    """특정 환자의 혈액검사 결과 목록 조회"""
    serializer_class = BloodResultSerializer
    authentication_classes = [PatientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Blood Results"], operation_summary="특정 환자의 혈액검사 결과 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return DbrBloodResults.objects.filter(patient_id=patient_id).order_by('-taken_at')


# ==================== 일정 관련 Views ====================
class AppointmentListView(generics.ListCreateAPIView):
    """일정 목록 조회 및 생성"""
    queryset = DbrAppointments.objects.all().select_related('patient')
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 등록")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """일정 상세 조회, 수정, 삭제"""
    queryset = DbrAppointments.objects.all().select_related('patient')
    serializer_class = AppointmentSerializer
    lookup_field = 'appointment_id'

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 상세 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 부분 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Appointments"], operation_summary="일정 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class PatientAppointmentsView(generics.ListAPIView):
    """특정 환자의 일정 목록 조회"""
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(tags=["Appointments"], operation_summary="특정 환자의 일정 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return DbrAppointments.objects.filter(patient_id=patient_id).order_by('appointment_date', 'appointment_time')


# ==================== 혈액검사 기준 관련 Views ====================
class BloodTestReferenceListView(generics.ListCreateAPIView):
    """혈액검사 기준 목록 조회 및 생성"""
    queryset = DbrBloodTestReferences.objects.all()
    serializer_class = BloodTestReferenceSerializer

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 등록")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BloodTestReferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """혈액검사 기준 상세 조회, 수정, 삭제"""
    queryset = DbrBloodTestReferences.objects.all()
    serializer_class = BloodTestReferenceSerializer
    lookup_field = 'reference_id'

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 상세 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 부분 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blood Test References"], operation_summary="혈액검사 기준 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ==================== 공지사항 관련 Views ====================
class AnnouncementListView(generics.ListCreateAPIView):
    """공지사항 목록 조회 및 생성"""
    queryset = Announcements.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 등록")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """공지사항 상세 조회, 수정, 삭제"""
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    lookup_field = 'announcements_id'

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 상세 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 부분 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Announcements"], operation_summary="공지사항 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)




# ==================== Dashboard Graph Views ====================
from .dashboard_bar import generate_risk_bar
from django.http import JsonResponse

from django.core.cache import cache
import hashlib

class DashboardGraphsView(APIView):
    """
    현재 로그인한 환자의 최신 혈액검사 결과로 4개의 그래프 생성
    """
    authentication_classes = [PatientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = request.user

            # 최신 혈액검사 결과 가져오기
            latest_result = DbrBloodResults.objects.filter(
                patient=patient
            ).order_by('-taken_at').first()

            if not latest_result:
                return Response(
                    {"error": "혈액검사 결과가 없습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 캐시 키 생성 (환자 ID + 검사 결과 ID)
            cache_key = f"graphs_{patient.patient_id}_{latest_result.blood_result_id}"

            # 캐시된 그래프 확인
            cached_graphs = cache.get(cache_key)
            if cached_graphs:
                return Response(cached_graphs, status=status.HTTP_200_OK)

            # 4개의 그래프 생성 (albumin, bilirubin, inr, platelet 순서)
            graphs = {}
            indicators = ['albumin', 'bilirubin', 'inr', 'platelet']

            for indicator in indicators:
                value = getattr(latest_result, indicator, None)

                if value is None:
                    graphs[indicator] = None
                else:
                    # base64 이미지 생성
                    img_base64 = generate_risk_bar(indicator, float(value))
                    graphs[indicator] = f"data:image/png;base64,{img_base64}"

            response_data = {
                "patient_name": patient.name,
                "test_date": latest_result.taken_at,
                "graphs": graphs
            }

            # 캐시에 저장 (1시간 동안 유지)
            cache.set(cache_key, response_data, 3600)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
