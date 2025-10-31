from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid


class Announcements(models.Model):
    announcements_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey('auth.User', models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'announcements'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'


class Patients(models.Model):
    SEX_CHOICES = [
        ('male', '남성'),
        ('female', '여성'),
    ]

    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    resident_number = models.CharField(max_length=13, blank=True, null=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'patients'
        verbose_name = '환자'
        verbose_name_plural = '환자'


class MedicalRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    visit_date = models.DateTimeField()
    chief_complatint = models.CharField(max_length=255, blank=True, null=True)
    subjective_note = models.TextField(blank=True, null=True)
    objective_note = models.TextField(blank=True, null=True)
    assessment = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING, db_column='patient_id')

    class Meta:
        managed = True
        db_table = 'medical_records'
        verbose_name = '진료 기록'
        verbose_name_plural = '진료 기록'


class BloodResults(models.Model):
    blood_id = models.AutoField(primary_key=True)
    ast = models.DecimalField(db_column='AST', max_digits=10, decimal_places=2, blank=True, null=True)
    alt = models.DecimalField(db_column='ALT', max_digits=10, decimal_places=2, blank=True, null=True)
    alp = models.DecimalField(db_column='ALP', max_digits=10, decimal_places=2, blank=True, null=True)
    ggt = models.DecimalField(db_column='GGT', max_digits=10, decimal_places=2, blank=True, null=True)
    bilirubin = models.DecimalField(db_column='Bilirubin', max_digits=10, decimal_places=2, blank=True, null=True)
    albumin = models.DecimalField(db_column='Albumin', max_digits=10, decimal_places=2, blank=True, null=True)
    inr = models.DecimalField(db_column='INR', max_digits=10, decimal_places=3, blank=True, null=True)
    platelet = models.DecimalField(db_column='Platelet', max_digits=10, decimal_places=2, blank=True, null=True)
    afp = models.DecimalField(db_column='AFP', max_digits=10, decimal_places=2, blank=True, null=True)
    taken_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    record = models.ForeignKey(MedicalRecords, models.DO_NOTHING, db_column='record_id')

    class Meta:
        managed = True
        db_table = 'blood_results'
        verbose_name = '혈액 검사'
        verbose_name_plural = '혈액 검사'


class MedicalDiagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    icd_code = models.CharField(max_length=10, blank=True, null=True)
    diagnosis_name = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(blank=True, null=True)
    record = models.ForeignKey(MedicalRecords, models.DO_NOTHING, db_column='record_id')

    class Meta:
        managed = True
        db_table = 'medical_diagnosis'
        verbose_name = '진단'
        verbose_name_plural = '진단'


class MedicalVitals(models.Model):
    vital_id = models.AutoField(primary_key=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bp_systolic = models.IntegerField(blank=True, null=True)
    bp_diastolic = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    resp_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    oxygen_saturation = models.IntegerField(blank=True, null=True)
    measured_at = models.DateTimeField(blank=True, null=True)
    record = models.ForeignKey(MedicalRecords, models.DO_NOTHING, db_column='record_id')

    class Meta:
        managed = True
        db_table = 'medical_vitals'
        verbose_name = '활력 징후'
        verbose_name_plural = '활력 징후'


class NursingNotes(models.Model):
    NOTE_TYPE_CHOICES = [
        ('monitoring', '모니터링'),
        ('intervention', '처치'),
        ('education', '교육'),
        ('report', '보고'),
    ]
    ABNORMAL_FLAG_CHOICES = [
        ('normal', '정상'),
        ('abnormal', '이상'),
    ]

    note_id = models.AutoField(primary_key=True)
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, blank=True, null=True)
    subjective_note = models.TextField(blank=True, null=True)
    objective_note = models.TextField(blank=True, null=True)
    assessment = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    intervention = models.TextField(blank=True, null=True)
    abnormal_flag = models.CharField(max_length=8, choices=ABNORMAL_FLAG_CHOICES, blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    record = models.ForeignKey(MedicalRecords, models.DO_NOTHING, db_column='record_id')

    class Meta:
        managed = True
        db_table = 'nursing_notes'
        verbose_name = '간호 기록'
        verbose_name_plural = '간호 기록'


class DeseaseManage(models.Model):
    desease_manage_id = models.BigAutoField(primary_key=True)
    diagnosis_date = models.DateField(blank=True, null=True)
    bclc_stage = models.CharField(max_length=10, blank=True, null=True)
    tumor_size = models.FloatField(blank=True, null=True)
    tumor_count = models.IntegerField(blank=True, null=True)
    vascular_invasion = models.BooleanField(default=False)
    child_pugh = models.CharField(max_length=1, blank=True, null=True)
    afp_initial = models.FloatField(blank=True, null=True)
    afp_current = models.FloatField(blank=True, null=True)
    treatment_type = models.CharField(max_length=50, blank=True, null=True)
    treatment_start_date = models.DateField(blank=True, null=True)
    recurrence_risk = models.CharField(max_length=10, blank=True, null=True)
    doctor = models.CharField(max_length=10, blank=True, null=True)
    hospital = models.CharField(max_length=10, blank=True, null=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING, db_column='patient_id')

    class Meta:
        managed = True
        db_table = 'desease_manage'
        verbose_name = '질병 관리'
        verbose_name_plural = '질병 관리'

