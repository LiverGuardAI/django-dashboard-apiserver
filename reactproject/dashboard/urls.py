from django.urls import path
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
    # 약물
    MedicationListView, MedicationDetailView, PatientMedicationsView,
    # 복용 기록
    MedicationLogListView, MedicationLogDetailView,
    # 의료기관
    # MedicalFacilityListView, MedicalFacilityDetailView,
    # 즐겨찾기
    # FavoriteFacilityListView, FavoriteFacilityDetailView, PatientFavoriteFacilitiesView,
    # flask ai
    SurvivalPredictionAPIView,
)

urlpatterns = [
    # Auth view
    path("auth/register/", DbrPatientRegisterView.as_view(), name="patient-register"),
    path("auth/login/", DbrPatientLoginView.as_view(), name="patient-login"),
    path("auth/logout/", DbrPatientLogoutView.as_view(), name="patient-logout"),
    path("auth/user/", DbrPatientUserView.as_view(), name="patient-user"),
    path("auth/refresh/", DbrPatientTokenRefreshView.as_view(), name="patient_token_refresh"),
    
    # ==================== Dashboard ====================
    path('dashboard/graphs/', DashboardGraphsView.as_view(), name='dashboard-graphs'),
    
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

    # ==================== 약물 ====================
    path('medications/', MedicationListView.as_view(), name='medication-list'),
    path('medications/<int:medication_id>/', MedicationDetailView.as_view(), name='medication-detail'),
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
]
