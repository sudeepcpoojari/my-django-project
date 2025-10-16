from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes



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
        users = user(**validated_data)
        users.set_password(password)
        users.save()
        return users


class CreateStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']

    def validate_role(self, value):
        if value != 'student':  
            raise serializers.ValidationError("Role student")
        return value

    def create(self, validated_data):   
        password = validated_data.pop('password')
        users = user(**validated_data)
        users.set_password(password)   
        users.save()
        return users

class SessionLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self,attrs):
        username=attrs.get('username')
        password=attrs.get('password')

        users=authenticate(username=username,password=password)
        if not users:
            raise serializers.ValidationError("Invalid username or password")

        if not users.is_active:
            raise serializers.ValidationError("Account disabled,contact administrator")
        return users

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
    def validate_email(self,value):
        try:
            u=user.objects.get(email=value)
        except user.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value    

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            u = user.objects.get(pk=uid)
        except (user.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("Invalid uid")

        if not default_token_generator.check_token(u, data['token']):
            raise serializers.ValidationError("Invalid or expired token")

        data['user'] = u
        return data

    def save(self):
        u = self.validated_data['user']
        new_password = self.validated_data['new_password']
        u.set_password(new_password)
        u.save()
        return u
