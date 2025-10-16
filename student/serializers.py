from rest_framework import serializers
from accounts.models import user
from .models import Student, Standard, Section, ParentStudent, Attendance


class StudentRegistrationSerializer(serializers.ModelSerializer):
    # extra fields for user creation
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    standard_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'password', 'standard_id', 'section_id']

    def validate_email(self, value):
        if user.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value

    def create(self, validated_data):
        users = user.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['name'],
            role='STUDENT'
        )

        users.set_password(validated_data['password'])
        users.save()

        standard = Standard.objects.get(id=validated_data['standard_id'])
        section = Section.objects.get(id=validated_data['section_id'])

        student = Student.objects.create(
            users=users,
            standard=standard,
            section=section,
        )
        return student


    def to_representation(self, instance):
        return {
            "student_id": instance.id,
            "name": instance.users.first_name,
            "email": instance.users.email,
            "standard": instance.standard.name if instance.standard else None,
            "section": instance.section.name if instance.section else None,
        }


class LinkParentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParentStudent
        fields = ['id', 'parent_id', 'student_id']

    def validate(self, data):
        try:
            parent = user.objects.get(id=data['parent_id'], role__iexact='parent')
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


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'standard']

class StandardSerializer(serializers.ModelSerializer):
    sections=SectionSerializer(many=True, read_only=True)
    class Meta:
        model=Standard
        fields=['id','name','sections']

class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=['id','student','date','status','marked_by']
        read_only_fields=['id','marked_by']

class AttendenceMarkSerializer(serializers.Serializer):
    student_id=serializers.IntegerField()
    date=serializers.DateField()
    status=serializers.ChoiceField(choices=[('PRESENT','Present'),('ABSENT','Absent')])


class AttendanceDailySerializer(serializers.ModelSerializer):
    student_name=serializers.CharField(read_only=True)
    standard=serializers.CharField(read_only=True)
   
    class Meta:
        model=Attendance
        fields=['student_name','standard','date','status']

class AttendanceSummarySerializer(serializers.Serializer):
    student_name=serializers.CharField()
    standard=serializers.CharField()
    section=serializers.CharField()
    total_present=serializers.IntegerField()
    total_absent=serializers.IntegerField()
    attendace_percentage=serializers.CharField()