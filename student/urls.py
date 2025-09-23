from django.urls import path
from . import views
urlpatterns = [
    path('studentreg/',views.StudentRegistrationView.as_view()),
    path('isteacher/',views.IsTeacher),
    path('linkparent/',views.LinkParentToStudentView.as_view()),
]
