from django.db import models

# Create your models here.
class DoctorDb(models.Model):
    name=models.CharField(max_length=50)
    specilization=models.CharField(max_length=50)
    experience=models.CharField(max_length=50)
    hospital=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    consultingFee=models.IntegerField
    availablity=models.IntegerField

    def __str__(self):
        return self.name
         

class AppointmenDb(models.Model):
    patient_name=models.CharField(max_length=50)
    doctor_id=models.IntegerField()
    appointment_time = models.TimeField(null=True, blank=True)
    phone=models.IntegerField()
    doctor_name=models.CharField(max_length=50)
    appointment_date=models.DateField()
    token_no=models.PositiveIntegerField(editable=False,null=True)
    problem=models.TextField(max_length=50)
    status=models.CharField(max_length=50,default="Pending")
    prescription=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name