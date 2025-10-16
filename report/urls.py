from django.urls import path
from . import views

urlpatterns = [
    path('report-card/<int:student_id>/', views.ReportCardView.as_view(), name='report_card'),
    path('class-performance/', views.ClassPerformanceView.as_view(), name='class_performance'),
    path('toppers/', views.TopPerformersView.as_view(), name='top_performers'),
]