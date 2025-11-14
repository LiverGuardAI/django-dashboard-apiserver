from django.urls import path
from .views import HealthcareSearchView, DepartmentListView

urlpatterns = [
    # 병원/의원/약국 통합 검색 (좌표 기반)
    path('search/', HealthcareSearchView.as_view(), name='healthcare-search'),
    
    # 진료과목 목록 (필터용)
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    
    
]