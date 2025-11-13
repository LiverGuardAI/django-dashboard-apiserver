# liverguard/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    DbrPatients, DbrBloodResults, DbrAppointments, DbrBloodTestReferences,
    Medication, MedicationLog,
)
from rest_framework_simplejwt.tokens import RefreshToken

# Auth serializers
# sign up serializers
class DbrPatientRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    birth_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"],
        format="%Y-%m-%d"
    )
    class Meta:
        model = DbrPatients
        fields = [
            "user_id", "password", "password2",
            "name", "birth_date", "sex", "phone"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data
    def create(self, validated_data):
        validated_data.pop("password2")
        validated_data["password"] = make_password(validated_data["password"])
        return DbrPatients.objects.create(**validated_data)

# login serializers
class DbrPatientLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_id = data.get("user_id")
        password = data.get("password")

        try:
            user = DbrPatients.objects.get(user_id=user_id)
        except DbrPatients.DoesNotExist:
            raise serializers.ValidationError({"user_id": "존재하지 않는 사용자입니다."})

        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": "비밀번호가 올바르지 않습니다."})

        # ✅ 검증 통과 시 user 객체만 전달
        data["user"] = user
        return data

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrPatients
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 응답에 포함하지 않음
        }
        

class BloodResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_id.name', read_only=True)

    class Meta:
        model = DbrBloodResults
        fields = '__all__'
        read_only_fields = ['created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_id.name', read_only=True)
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DbrAppointments
        fields = '__all__'
        read_only_fields = ['appointment_id', 'patient_id', 'created_at', 'updated_at']


class BloodTestReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrBloodTestReferences
        fields = '__all__'


# ==================== 약물 관련 Serializers ====================
class MedicationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_id.name', read_only=True)

    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ['created_at']


class MedicationLogSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.medication_name', read_only=True)
    patient_name = serializers.CharField(source='medication.patient_id.name', read_only=True)

    class Meta:
        model = MedicationLog
        fields = '__all__'
        read_only_fields = ['created_at']


# # ==================== 의료기관 관련 Serializers ====================
# class MedicalFacilitySerializer(serializers.ModelSerializer):
#     type_display = serializers.CharField(source='get_type_display', read_only=True)

#     class Meta:
#         model = MedicalFacility
#         fields = '__all__'
#         read_only_fields = ['created_at']


# class FavoriteFacilitySerializer(serializers.ModelSerializer):
#     patient_name = serializers.CharField(source='patient.name', read_only=True)
#     facility_name = serializers.CharField(source='facility.name', read_only=True)
#     facility_type = serializers.CharField(source='facility.type', read_only=True)
#     facility_address = serializers.CharField(source='facility.address', read_only=True)

#     class Meta:
#         model = FavoriteFacility
#         fields = '__all__'
#         read_only_fields = ['created_at']
