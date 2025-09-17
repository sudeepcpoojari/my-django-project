from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import createuserserializer
from .models import user
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication



class createTeacherParentView(CreateAPIView):
    serializer_class=createuserserializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]


    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)
