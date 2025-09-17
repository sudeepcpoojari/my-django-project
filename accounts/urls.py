from django.urls import path
from . import views
urlpatterns = [
    path('createteacherparent/',views.createTeacherParentView.as_view())
]
