from django.urls import path
from . import views

urlpatterns = [
    path('internships/my/', views.InternshipMyView.as_view(), name='internship-my'),
    path('internships/', views.InternshipCreateView.as_view(), name='internship-create'),
    path('internship-logs/', views.InternshipLogListCreateView.as_view(), name='internship-log-list-create'),
    path('internship-logs/<int:pk>/review/', views.InternshipLogReviewView.as_view(), name='internship-log-review'),
]
