# liverguard/urls.py

# ✍️ (1/4) 'include'와 'routers'를 import 합니다.
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import (
    # 환자
    PatientListView, PatientDetailView,
    # 혈액검사
    BloodResultListView, BloodResultDetailView, LatestBloodResultView,
    # 일정
    AppointmentListView, AppointmentDetailView,
    # 혈액검사 기준
    BloodTestReferenceListView, BloodTestReferenceDetailView,
    # Auth
    DbrPatientRegisterView, DbrPatientLoginView, DbrPatientLogoutView, DbrPatientUserView, DbrPatientTokenRefreshView,
    # Dashboard
    DashboardGraphsView,
    DashboardTimeSeriesView, 
    # 약물
    # ✍️ (2/4) 기존 View 2개(ListView, DetailView)는 import 목록에서 제거합니다.
    PatientMedicationsView, MedicationViewSet, DrugSearchAPIView,
    # 복용 기록
    MedicationLogListView, MedicationLogDetailView,
    # 의료기관 (주석 유지)
    # MedicalFacilityListView, MedicalFacilityDetailView,
    # 즐겨찾기 (주석 유지)
    # FavoriteFacilityListView, FavoriteFacilityDetailView, PatientFavoriteFacilitiesView,
    # flask ai
    SurvivalPredictionAPIView,
)

# ==========================================================
# ✍️ (3/4) ViewSet을 위한 라우터 생성 및 등록
# ==========================================================
router = routers.DefaultRouter()

# 'medications'라는 URL로 MedicationViewSet을 등록합니다.
# 이 한 줄이 /medications/ [GET, POST] 와
# /medications/<pk>/ [GET, PUT, PATCH, DELETE] URL을 모두 자동 생성합니다.
router.register(r'medications', MedicationViewSet, basename='medication')

# ==========================================================


urlpatterns = [
    # Auth view
    path("auth/register/", DbrPatientRegisterView.as_view(), name="patient-register"),
    path("auth/login/", DbrPatientLoginView.as_view(), name="patient-login"),
    path("auth/logout/", DbrPatientLogoutView.as_view(), name="patient-logout"),
    path("auth/user/", DbrPatientUserView.as_view(), name="patient-user"),
    path("auth/refresh/", DbrPatientTokenRefreshView.as_view(), name="patient_token_refresh"),
    
    # ==================== Dashboard ====================
    path('dashboard/graphs/', DashboardGraphsView.as_view(), name='dashboard-graphs'),
    path('dashboard/time-series/', DashboardTimeSeriesView.as_view(), name='dashboard-time-series'),
    
    # ==================== 환자 ====================
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<uuid:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),

    # ==================== 혈액검사 결과 ====================
    path('blood-results/', BloodResultListView.as_view(), name='blood-result-list'),
    path('blood-results/latest/', LatestBloodResultView.as_view(), name='blood-result-latest'),
    path('blood-results/<int:blood_result_id>/', BloodResultDetailView.as_view(), name='blood-result-detail'),

    # ==================== 일정 ====================
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # ==================== 혈액검사 기준 ====================
    path('blood-test-references/', BloodTestReferenceListView.as_view(), name='blood-test-reference-list'),
    path('blood-test-references/<int:reference_id>/', BloodTestReferenceDetailView.as_view(), name='blood-test-reference-detail'),

    # 👈 [추가] 약물 검색 API 엔드포인트
    # ==========================================================
    path('drugs/search/', views.DrugSearchAPIView.as_view(), name='drug-search'),
    
    # (유지) 이 View는 ViewSet과 별개임 (특정 환자의 약물 조회)
    path('patients/<uuid:patient_id>/medications/', PatientMedicationsView.as_view(), name='patient-medications'),

    # ==================== 복용 기록 ====================
    path('medication-logs/', MedicationLogListView.as_view(), name='medication-log-list'),
    path('medication-logs/<int:log_id>/', MedicationLogDetailView.as_view(), name='medication-log-detail'),

    # ==================== 의료기관 ====================
    # path('medical-facilities/', MedicalFacilityListView.as_view(), name='medical-facility-list'),
    # path('medical-facilities/<int:facility_id>/', MedicalFacilityDetailView.as_view(), name='medical-facility-detail'),
    
    # ==================== 즐겨찾기 ====================
    # path('favorite-facilities/', FavoriteFacilityListView.as_view(), name='favorite-facility-list'),
    # path('favorite-facilities/<int:favorite_id>/', FavoriteFacilityDetailView.as_view(), name='favorite-facility-detail'),
    # path('patients/<uuid:patient_id>/favorite-facilities/', PatientFavoriteFacilitiesView.as_view(), name='patient-favorite-facilities'),
    
    # ==================== flask ai ====================
    path("predict-survival/", SurvivalPredictionAPIView.as_view(), name="predict_survival"),

    # ==========================================================
    # ✍️ (4/4) 라우터에 등록된 URL (medications/)을 마지막에 포함
    # ==========================================================
    path('', include(router.urls)),
]
