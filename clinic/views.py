from django.shortcuts import render
from clinic.serializers import doctorSerilizers,ApointmentSerilizers
from clinic.models import DoctorDb,AppointmenDb
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from datetime import time,datetime,timedelta

# Create your views here.
class doctorView(APIView):
    def get(self,request):
        qs=DoctorDb.objects.all()
        inst_serli=doctorSerilizers(qs,many=True)
        return Response(data=inst_serli.data)
    def post(self,request):
        data1=request.data
        seri_insta=doctorSerilizers(data=data1)
        if seri_insta.is_valid():
            seri_insta.save()
            return Response(data=seri_insta.data)

        else:Response(data=seri_insta.errors)

class DoctorRetriveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs=get_object_or_404(DoctorDb,id=pk)
        seri_insta=doctorSerilizers(qs)
        return Response(seri_insta.data)

    def put(self,request,pk):
        form_data=request.data
        qs=get_object_or_404(DoctorDb,id=pk)
        ser_insta=doctorSerilizers(data=form_data,instance=qs)
        if ser_insta.is_valid():
            ser_insta.save()
            return Response(data=ser_insta.data)
        else:
            return Response(data=ser_insta.errors)

    def delete(self,request,pk):
        qs=get_object_or_404(DoctorDb,id=pk)
        qs.delete()
        return Response({
            "message":"Deleted Data"
        })

class appointmentCreateView(APIView):
    def get(self,request):
        qa=AppointmenDb.objects.all()
        ser_instat=ApointmentSerilizers(qa,many=True)
        return Response(data=ser_instat.data)

    def post(self, request):
        form_data = request.data.copy()
        seri_instant = ApointmentSerilizers(data=form_data)
        
        if seri_instant.is_valid():
            appointment_datee = seri_instant.validated_data.get("appointment_date")
            doc_id = seri_instant.validated_data.get("doctor_id")
            
            last_apoi = AppointmenDb.objects.filter(
                doctor_id=doc_id,
                appointment_date=appointment_datee,
            ).order_by("-token_no").first()

            if last_apoi is None:
                form_data["token_no"] = 1
                form_data["appointment_time"] = time(10, 0)
            else:
                next_token = last_apoi.token_no + 1
                current_time = datetime.combine(appointment_datee, last_apoi.appointment_time)
                next_time = current_time + timedelta(minutes=10)

                # Lunch break skip logic (12:30 to 1:30)
                if next_time.time() == time(12, 30):
                    next_time = datetime.combine(appointment_datee, time(13, 30))

                # Check if booking time has reached 5:10 PM (17:10)
                if next_time.time() > time(17, 10):
                    return Response(data={"message": "Booking today completed"})

                form_data["token_no"] = next_token
                form_data["appointment_time"] = next_time.time()  # Extract time object

            qs = AppointmenDb.objects.create(**form_data)
            return Response(data={
                "message": "Booked Success",
                "token no": qs.token_no,
                "token date&time": str(form_data["appointment_date"]),
            })
        else:
            return Response(data=seri_instant.errors)


