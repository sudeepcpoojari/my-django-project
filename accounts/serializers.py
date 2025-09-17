from rest_framework import serializers
from .models import user

class createuserserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model=user
        fields=['username','email','password','role','first_name','last_name']


    
    def validate_role(self,value):
        if value not in ['teacher','parent']:
            raise serializers.ValidationError("Role must be teacher or parent.")
        return value
    

    def create(self,validated_data):
        password = validated_data.pop('password')
        user =user(**validated_data)
        user.set_password(password)
        user.save()
        return user
