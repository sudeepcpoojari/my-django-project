from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import StudentRegistrationSerializer, LinkParentSerializer,SectionSerializer,StandardSerializer,AttendenceSerializer,AttendenceMarkSerializer,AttendanceDailySerializer
from .models import Student,ParentStudent,Standard,Section,Attendance
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import user   
import json



class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ["teacher"]
        )


class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsTeacher]

class LinkParentToStudentView(generics.CreateAPIView):
    queryset = ParentStudent.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsTeacher]
      
class StandardListCreateView(generics.ListCreateAPIView):
    queryset=Standard.objects.all()
    serializer_class=StandardSerializer
    permission_classes=[IsTeacher]

class SectionListCreateView(generics.ListCreateAPIView):
    queryset=Section.objects.all()
    serializer_class=SectionSerializer
    permission_classes=[IsTeacher]

class AttendenceView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendenceMarkSerializer
    permission_classes = [IsAuthenticated]  # Require login (JWT)

    def post(self, request, *args, **kwargs):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)

        records = []
        marked_by_user = request.user  # user is authenticated due to permission_classes

        for item in serializer.validated_data if many else [serializer.validated_data]:
            student_id = item['student_id']
            date = item['date']
            status_ = item['status']

            try:
                student_obj = user.objects.get(id=student_id, role='STUDENT')
            except user.DoesNotExist:
                return Response(
                    {"error": f"Student with id {student_id} does not exist or is not a student."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            attendance_obj, created = Attendance.objects.update_or_create(
                student=student_obj,
                date=date,
                defaults={
                    'status': status_,
                    'marked_by': marked_by_user
                }
            )
            records.append(attendance_obj)

        return Response(
            AttendenceSerializer(records, many=True).data,
            status=status.HTTP_200_OK
        )


class StudentAttendenceView(generics.ListAPIView):
    serializer_class = AttendenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        if self.request.user.role == "STUDENT" and self.request.user.id != int(student_id):
            return Attendance.objects.none()
        return Attendance.objects.filter(student_id=student_id).order_by("-date")

class ClassAttendenceView(generics.ListAPIView):
    serializer_class = AttendenceSerializer
    permission_classes = [IsTeacher,IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs["section_id"]
        section = Section.objects.get(id=section_id)
        date = self.request.query_params.get("date")
        user_ids = [student.users.id for student in Student.objects.filter(section=section)]
        students = user.objects.filter(id__in = user_ids,role="STUDENT")

        if date:
            return Attendance.objects.filter(student__in=students,date=date)
        return Attendance.objects.filter(student__in=students).order_by("-date")


def calculate_percentage(present, total_days):
    if total_days == 0:
        return "0%"
    return f"{round((present / total_days) * 100, 2)}%"


class AttendanceReportPrincipalView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Attendance.objects.all()
        standard = request.query_params.get("standard")
        section = request.query_params.get("section")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        if standard:
            std = Standard.objects.get(name=standard)
            students = Student.objects.filter(standard=std)
            users = [student.users for student in students]
            queryset = queryset.filter(student__in=users)

        if section:
            sec = Section.objects.get(name=section)
            students = Student.objects.filter(section=sec)
            users = [student.users for student in students]
            queryset = queryset.filter(student__in=users)

        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

        summary_data = []
        student_ids = queryset.values_list("student", flat=True).distinct()
        for sid in student_ids:
            student_records = queryset.filter(student__id=sid)
            if not student_records.exists():
                continue

            user_obj = student_records.first().student
            student = Student.objects.filter(users=user_obj).first()
            if not student:
                continue

            total_days = student_records.count()
            total_present = student_records.filter(status="PRESENT").count()  
            total_absent = student_records.filter(status="ABSENT").count()    

            summary_data.append({
                "student_name": f"{student.users.first_name} {student.users.last_name}",
                "standard": student.standard.name if student.standard else "",
                "section": student.section.name if student.section else "",
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_percentage(total_present, total_days)
            })

        total_students = len(student_ids)
        total_days = queryset.values("date").distinct().count()
        overall_present = queryset.filter(status="PRESENT").count()  
        overall_percentage = calculate_percentage(overall_present, queryset.count())

        return Response({
            "summary": {
                "total_students": total_students,
                "total_days": total_days,
                "average_attendance": overall_percentage
            },
            "records": summary_data
        })

class AttendanceReportParentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        parent = request.user

        if parent.role != "parent":
            return Response({"error": "Only parents can view this report"}, status=403)

    
        linked_students = [link.student for link in ParentStudent.objects.filter(parent=parent)]

        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        data = []

        for student in linked_students:
            user = student.users  
            user_records = Attendance.objects.filter(student=user)
            if from_date and to_date:
                user_records = user_records.filter(date__range=[from_date, to_date])

            if not user_records.exists():
                continue

            total_days = user_records.count()
            total_present = user_records.filter(status__iexact="PRESENT").count()
            total_absent = user_records.filter(status__iexact="ABSENT").count()

            child_data = {
                "student_name": f"{student.users.first_name} {student.users.last_name}",  
                "standard": student.standard.name,
                "section": student.section.name,
                "summary": {
                    "total_days": total_days,
                    "present": total_present,
                    "absent": total_absent,
                    "percentage": calculate_percentage(total_present, total_days)
                },
                "records": AttendanceDailySerializer(user_records, many=True).data
            }

            data.append(child_data)

        return Response({"children": data})
