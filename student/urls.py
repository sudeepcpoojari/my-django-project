from django.urls import path
from . import views
urlpatterns = [
    path('studentreg/',views.StudentRegistrationView.as_view()),
    path('isteacher/',views.IsTeacher),
    path('linkparent/',views.LinkParentToStudentView.as_view()),
    path('standards/',views.StandardListCreateView.as_view(),name='standards_list_create'),
    path('sections/',views.SectionListCreateView.as_view(),name='sections_list_create'),
    path('attendence/mark/',views.AttendenceView.as_view(),name='attendence_marking'),
    path('attendence/student/<int:student_id>/',views.StudentAttendenceView.as_view(),name='student_attendence_report'),
    path('attendence/section/<int:section_id>/',views.ClassAttendenceView.as_view(),name='section_attendence_report'),
    path('attendance-report/principal/',views.AttendanceReportPrincipalView.as_view(),name='attendance_report_principal'),
    path('attendance-report/parent/',views.AttendanceReportParentView.as_view(),name='attendance_report_parent'),
    
]