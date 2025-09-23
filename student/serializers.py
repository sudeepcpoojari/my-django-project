from rest_framework import serializers
from accounts.models import user
from .models import Student, Standard ,Section,ParentStudent


class StudentRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    standard_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)


    class Meta:
        model=Student
        fields = ['id', 'name', 'email', 'password', 'standard_id', 'section_id']


    def create(self, validated_data):

        users = user.objects.create(
            username = validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name= validated_data['name'],
            role='STUDENT'
        )


        standard = Standard.objects.get(id=validated_data['standard_id'])
        section = Section.objects.get(id=validated_data['section_id'])



        student=Student.objects.create(
            users=users,
            standard=standard,
            section=section,
        )
        return student
    
    def to_representation(self, instance):
        return {
            "student_id":instance.id,
            "name":instance.users.first_name,
            "email":instance.users.email,
            "standard":instance.standard.name if instance.standard else None,
            "section":instance.section.name if instance.section else None,
        }


class LinkParentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParentStudent
        fields = ['id', 'parent_id', 'student_id']

    def validate(self, data):
        try:
            parent = user.objects.get(id=data['parent_id'], role='parent')
        except user.DoesNotExist:
            raise serializers.ValidationError("Invalid parent_id or user is not a parent")

        try:
            student = Student.objects.get(id=data["student_id"])
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student_id")

        return data

    def create(self, validated_data):
        parent = user.objects.get(id=validated_data['parent_id'])
        student = Student.objects.get(id=validated_data["student_id"])
        link, created = ParentStudent.objects.get_or_create(parent=parent, student=student)
        return link

    def to_representation(self, instance):
        return {
            "link_id": instance.id,
            "student": instance.student.users.first_name,
            "parent": instance.parent.first_name,
            "message": "Parent linked to student successfully"
        }
