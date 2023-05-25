from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User, Teacher, Class, Subject, Student
from .serializer import TeacherSerializer, UserSerializer, ClassSerializer, SubjectSerializer, ClassSerializerWithSubject, ClassSerializerWithStudents,StudentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .custom_permission import IsAdminUser, IsTeacherUser, IsAdminOrTeacherUser


# classes with subjects
class AllClasses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrTeacherUser]

    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializerWithSubject(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# classes with subjects
class AllClassesWithStudent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrTeacherUser]

    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializerWithStudents(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# classes with  teacher id
class TeacherClassView(APIView):
    def get(self, request, teacher_id):
        if teacher_id is None:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        teacher = Teacher.objects.get(pk=teacher_id)
        classes = teacher.class_set.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#get and add student
class StudentAddView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# admin login
class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(
            username=username, user_type='admin').first()
        if user and user.check_password(password) and user.user_type == 'admin':
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# teacher register
class TeacherRegistrationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_teacher(self, teacher_id):
        t = Teacher.objects.get(pk=teacher_id)
        if t is None:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        return t



    def post(self, request):
        user_data = request.data.get('user')
        qualification = request.data.get('qualification')

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            teacher = Teacher.objects.create(
                user=user, qualification=qualification)
            teacher_serializer = TeacherSerializer(teacher)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

    def delete(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        if teacher:
            teacher.delete()
            return Response({'message': 'Teacher deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(
            teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllTeachers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        teachers = Teacher.objects.all()
        serialized_teachers = TeacherSerializer(teachers, many=True)
        return Response(serialized_teachers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# Teachers Functions


class TeacherLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(
            username=username, user_type='teacher').first()
        if user and user.user_type == 'teacher':
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Admin Apis
class ClassAddView(APIView):
    permission_classes = [IsAdminUser]

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            class_obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectAddView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        class_id = request.data.get('class_id')
        name = request.data.get('name')

        class_obj = Class.objects.filter(id=class_id).first()
        if class_obj is None:
            return Response({'message': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

        subject = Subject.objects.create(name=name, class_field=class_obj)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubjectUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, subject_id):
        name = request.data.get('name')

        subject = Subject.objects.filter(id=subject_id).first()
        if subject is None:
            return Response({'message': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        subject.name = name
        subject.save()
        serializer = SubjectSerializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, subject_id):

        subject = Subject.objects.get(id=subject_id)
        if subject is None:
            Response({'message': 'Subject not found'},
                     status=status.HTTP_404_NOT_FOUND)
        subject.delete()
        return Response({'message': 'Subject deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AssignClassToTeacher(APIView):
    def post(self, request):
        teacher_id = request.data.get('teacher_id')
        class_id = request.data.get('class_id')

        teacher = Teacher.objects.get(user=teacher_id)
        if teacher is None:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        class_obj = Class.objects.get(id=class_id)
        if class_obj is None:
            return Response({'message': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

        class_obj.teachers.add(teacher)
        class_obj.save()

        return Response({'message': 'Class assigned to teacher successfully'}, status=status.HTTP_200_OK)


class TeacherClassStudentsView(APIView):
    def get(self, request):
        # teacher = request.user.teacher
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectListView(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
