from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('createteacherparent/',views.createTeacherParentView.as_view()),
    path("login/",csrf_exempt(views.SessionLoginView.as_view()),name="session_login"),
    path("logout/",csrf_exempt(views.SessionLogoutView.as_view()),name="session_logout"),
]
