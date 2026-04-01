from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.InternshipMyView.as_view(), name='internship-my'),
    path('', views.InternshipCreateView.as_view(), name='internship-create'),
    path('logs/', views.InternshipLogCreateView.as_view(), name='internship-log-create'),
    path('logs/list/', views.InternshipLogListView.as_view(), name='internship-log-list'),
    path('logs/<int:pk>/review/', views.InternshipLogReviewView.as_view(), name='internship-log-review'),
]