from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import StudentRegistrationSerializer
from .models import Student


class IsTeacher(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ["teacher"]
    

class StudentRegistrationView(generics.CreateAPIView):
    queryset= Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsTeacher]