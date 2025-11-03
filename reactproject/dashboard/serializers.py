# liverguard/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import DbrPatients, DbrBloodResults, DbrAppointments, DbrBloodTestReferences, Announcements


# Auth serializers
class DbrPatientRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    birth_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"],
        format="%Y-%m-%d"
    )
    class Meta:
        model = DbrPatients
        fields = [
            "id", "password", "password2",
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


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrPatients
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 응답에 포함하지 않음
        }


class BloodResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = DbrBloodResults
        fields = '__all__'
        read_only_fields = ['created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DbrAppointments
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BloodTestReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbrBloodTestReferences
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']