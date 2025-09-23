from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import createuserserializer , CreateStudentSerializer
from .models import user , Classroom
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login,logout
from .serializers import SessionLoginSerializer

class createTeacherParentView(CreateAPIView):
    serializer_class=createuserserializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]


    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)


class SessionLoginView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=SessionLoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            login(request,user)
            return Response({
                "message":"Login successful",
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "role":user.role,
                }
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SessionLogoutView(APIView):
   def get(self,request,*args,**kwargs):
       logout(request)
       return Response({"message":"Logout successful"},status=status.HTTP_200_OK)