from django.urls import path
from . import views

urlpatterns = [
   path('marks/entry/', views.MarkEntryView.as_view(), name='mark_entry'),
   path('exams/', views.ExamListCreateView.as_view(), name='exam_list_create'),
       

]