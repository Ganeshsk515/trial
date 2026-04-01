from django.urls import path
from . import views

urlpatterns = [
    path('assignments/', views.AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/<int:assignment_id>/submissions/', views.SubmissionListView.as_view(), name='submission-list'),
    path('submissions/', views.SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/grade/', views.SubmissionGradeView.as_view(), name='submission-grade'),
    path('reports/assignments/', views.AssignmentReportsView.as_view(), name='assignment-reports'),
]
