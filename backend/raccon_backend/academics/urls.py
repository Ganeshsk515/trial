from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssignmentListCreateView.as_view(), name='assignment-list'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('<int:assignment_id>/submissions/', views.SubmissionListView.as_view(), name='submission-list'),
    path('submissions/', views.SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/grade/', views.SubmissionGradeView.as_view(), name='submission-grade'),
    path('assignments/', views.AssignmentReportsView.as_view(), name='assignment-reports'),
]