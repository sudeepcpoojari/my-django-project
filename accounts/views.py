from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import createuserserializer,CreateStudentSerializer
from .models import user , Classroom
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import login,logout
from .serializers import SessionLoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str



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

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        u = user.objects.get(email=serializer.validated_data['email'])  
        uid = urlsafe_base64_encode(force_bytes(u.pk))                 
        token = default_token_generator.make_token(u)                 

        reset_link = f"http://example.com/reset-password-confirm/?uid={uid}&token={token}"

        return Response(
            {"message": "Password reset link has been sent to your email.", "reset_link": reset_link},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )
