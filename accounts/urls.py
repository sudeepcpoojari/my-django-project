from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
    path('createteacherparent/',views.createTeacherParentView.as_view()),
    path("login/",csrf_exempt(views.SessionLoginView.as_view()),name="session_login"),
    path("logout/",csrf_exempt(views.SessionLogoutView.as_view()),name="session_logout"),
    path("password_reset/",views.PasswordResetRequestView.as_view(),name="password_reset"),
    path("password_reset_confirm/",views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("gettoken/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("refreshtoken/",TokenRefreshView.as_view(),name="token_refresh"),
    path("verifytoken/",TokenVerifyView.as_view(),name="token_verify")
]
