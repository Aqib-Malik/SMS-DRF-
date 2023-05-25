from django.urls import path
from .views import *
urlpatterns = [
    path('admin/login/', AdminLoginView.as_view(),),
    path('teacher/login/', TeacherLoginView.as_view(),),
    path('admin/logout/', AdminLogoutView.as_view(),),
    path('admin/teachers/register/', TeacherRegistrationView.as_view(), ),
    path('admin/teacher/<int:teacher_id>/',
         TeacherRegistrationView.as_view(),),

    path('admin/allteachers', AllTeachers.as_view(), ),
    path('admin/add/', ClassAddView.as_view(), ),
    path('admin/assign-class/', AssignClassToTeacher.as_view(),),

    path('admin/subjects/add/', SubjectAddView.as_view(), ),
    path('admin/subjects/update/<int:subject_id>/',
         SubjectUpdateView.as_view(), ),
    path('admin/subjects/delete/<int:subject_id>/', SubjectDeleteView.as_view(),),


    path('teachers/<int:teacher_id>/classes/', TeacherClassView.as_view()),

    path('admin/classes/', AllClasses.as_view()),

    path('admin/classes/students/', AllClassesWithStudent.as_view()),

    path('admin/students/', StudentAddView.as_view(),),

    path('admin/subjects/', SubjectListView.as_view()),






]
