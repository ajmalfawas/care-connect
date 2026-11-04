from rest_framework import serializers
from django.utils import timezone
from clinic.models import DoctorDb,AppointmenDb


class doctorSerilizers(serializers.ModelSerializer):
    
    class Meta:
          model=DoctorDb
          fields ="__all__"
          read_only_fields=["id"]

class ApointmentSerilizers(serializers.ModelSerializer):
     class Meta:
          model=AppointmenDb
          fields="__all__"
          read_only_fields=["id"]
     def validate(self,validated_data):
          phone=validated_data.get("phone")
          appointment_date=validated_data.get('appointment_date')

          if appointment_date<timezone.localdate():
               raise serializers.ValidationError("Invalid date")

          if AppointmenDb.objects.filter(

               phone=phone,appointment_date=appointment_date).exists():
               raise serializers.ValidationError('Already Booked ...')
          else:
               return validated_data

     
          

       