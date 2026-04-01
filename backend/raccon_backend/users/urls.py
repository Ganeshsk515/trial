from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    path('admin/users/', views.UserListView.as_view(), name='user-list'),
    path('admin/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-logs'),
]
