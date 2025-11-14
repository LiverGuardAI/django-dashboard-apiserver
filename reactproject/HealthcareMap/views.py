from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from .models import Hospital, Clinic, Pharmacy, DepartmentOfTreatment
from .serializers import (
    HospitalLiteSerializer, ClinicLiteSerializer, PharmacyLiteSerializer,
    DepartmentOfTreatmentSerializer
)


class DepartmentListView(generics.ListAPIView):
    """진료과목 목록 조회"""
    queryset = DepartmentOfTreatment.objects.all()
    serializer_class = DepartmentOfTreatmentSerializer


class HealthcareSearchView(APIView):
    """병원/의원/약국 통합 검색 - 지도 마커용 (최적화)"""

    def get(self, request):
        search_query = request.query_params.get('q', '')
        facility_type = request.query_params.get('type', 'all')  # all, hospital, clinic, pharmacy
        department_code = request.query_params.get('department', None)

        # 좌표 범위 검색 (지도 경계 내만 검색) - Decimal로 변환
        try:
            min_x = Decimal(request.query_params.get('min_x')) if request.query_params.get('min_x') else None
            max_x = Decimal(request.query_params.get('max_x')) if request.query_params.get('max_x') else None
            min_y = Decimal(request.query_params.get('min_y')) if request.query_params.get('min_y') else None
            max_y = Decimal(request.query_params.get('max_y')) if request.query_params.get('max_y') else None
        except (InvalidOperation, ValueError):
            return Response({'error': '잘못된 좌표 형식입니다.'}, status=400)

        results = {}

        # 병원 검색
        if facility_type in ['all', 'hospital']:
            hospital_qs = Hospital.objects.filter(
                coordinate_x__isnull=False,
                coordinate_y__isnull=False
            )

            if search_query:
                hospital_qs = hospital_qs.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query)
                )

            if department_code:
                hospital_qs = hospital_qs.filter(departments__code=department_code)

            if all([min_x, max_x, min_y, max_y]):
                hospital_qs = hospital_qs.filter(
                    coordinate_x__gte=min_x,
                    coordinate_x__lte=max_x,
                    coordinate_y__gte=min_y,
                    coordinate_y__lte=max_y
                )

            results['hospitals'] = HospitalLiteSerializer(
                hospital_qs.distinct()[:100], many=True
            ).data

        # 의원 검색
        if facility_type in ['all', 'clinic']:
            clinic_qs = Clinic.objects.filter(
                coordinate_x__isnull=False,
                coordinate_y__isnull=False
            )

            if search_query:
                clinic_qs = clinic_qs.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query)
                )

            if department_code:
                clinic_qs = clinic_qs.filter(departments__code=department_code)

            if all([min_x, max_x, min_y, max_y]):
                clinic_qs = clinic_qs.filter(
                    coordinate_x__gte=min_x,
                    coordinate_x__lte=max_x,
                    coordinate_y__gte=min_y,
                    coordinate_y__lte=max_y
                )

            results['clinics'] = ClinicLiteSerializer(
                clinic_qs.distinct()[:100], many=True
            ).data

        # 약국 검색
        if facility_type in ['all', 'pharmacy']:
            pharmacy_qs = Pharmacy.objects.filter(
                coordinate_x__isnull=False,
                coordinate_y__isnull=False
            )

            if search_query:
                pharmacy_qs = pharmacy_qs.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query)
                )

            if all([min_x, max_x, min_y, max_y]):
                pharmacy_qs = pharmacy_qs.filter(
                    coordinate_x__gte=min_x,
                    coordinate_x__lte=max_x,
                    coordinate_y__gte=min_y,
                    coordinate_y__lte=max_y
                )

            results['pharmacies'] = PharmacyLiteSerializer(
                pharmacy_qs[:100], many=True
            ).data

        return Response(results)