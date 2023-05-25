from rest_framework import serializers
from .models import User, Teacher,Class,Subject,Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'qualification']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        
        

        
        
        
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
        
# class ClassSerializerWithSubject(serializers.ModelSerializer):
#      subjects = SubjectSerializer(many=True, read_only=True, source='teachers__subject_set')

#      class Meta:
#         model = Class
#         fields = ['id', 'name', 'subjects']
        
        
class ClassSerializerWithSubject(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'subjects']

    def get_subjects(self, obj):
        subjects = obj.subject_set.all()
        serializer = SubjectSerializer(subjects, many=True)
        return serializer.data      


class ClassSerializerWithStudents(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'students']

    def get_students(self, obj):
        subjects = obj.student_set.all()
        serializer = StudentSerializer(subjects, many=True)
        return serializer.data      
        
        
        
