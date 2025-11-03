from django.urls import path
from .views import (
    # 환자
    PatientListView, PatientDetailView,
    # 혈액검사
    BloodResultListView, BloodResultDetailView, PatientBloodResultsView,
    # 일정
    AppointmentListView, AppointmentDetailView, PatientAppointmentsView,
    # 혈액검사 기준
    BloodTestReferenceListView, BloodTestReferenceDetailView,
    # 공지사항
    AnnouncementListView, AnnouncementDetailView, 
    DbrPatientRegisterView, DbrPatientLoginView, DbrPatientUserView, DbrPatientLogoutView,
)

urlpatterns = [
    # Auth view
    path("auth/register/", DbrPatientRegisterView.as_view(), name="patient-register"),
    path("auth/login/", DbrPatientLoginView.as_view(), name="patient-login"),
    path("auth/user/", DbrPatientUserView.as_view(), name="patient-user"),
    path("auth/logout/", DbrPatientLogoutView.as_view(), name="patient-logout"),
    
    # ==================== 환자 ====================
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<uuid:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),

    # ==================== 혈액검사 결과 ====================
    path('blood-results/', BloodResultListView.as_view(), name='blood-result-list'),
    path('blood-results/<int:blood_result_id>/', BloodResultDetailView.as_view(), name='blood-result-detail'),
    path('patients/<uuid:patient_id>/blood-results/', PatientBloodResultsView.as_view(), name='patient-blood-results'),

    # ==================== 일정 ====================
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('patients/<uuid:patient_id>/appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),

    # ==================== 혈액검사 기준 ====================
    path('blood-test-references/', BloodTestReferenceListView.as_view(), name='blood-test-reference-list'),
    path('blood-test-references/<int:reference_id>/', BloodTestReferenceDetailView.as_view(), name='blood-test-reference-detail'),

    # ==================== 공지사항 ====================
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/<int:announcements_id>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]