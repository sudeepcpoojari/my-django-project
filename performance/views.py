from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MarkEntrySerializer
from .serializers import ExamSerializer
from .models import Mark, Exam
from rest_framework.generics import ListCreateAPIView
from accounts.permissions import IsTeacherOrPrincipal

class MarkEntryView(APIView):
    permission_classes=[IsAuthenticated, IsTeacherOrPrincipal]

    def post(self, request):
        serializer=MarkEntrySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(entered_by=request.user)
            return Response({"message":"Marks saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamListCreateView(ListCreateAPIView):
    queryset=Exam.objects.all().order_by('-date')
    serializer_class=ExamSerializer
    permission_classes=[IsAuthenticated, IsTeacherOrPrincipal]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
# Create your views here.
