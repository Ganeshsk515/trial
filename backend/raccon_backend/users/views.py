from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    AdminUserCreateSerializer,
    AdminUserUpdateSerializer,
    AuditLogSerializer,
)
from .models import AuditLog

User = get_user_model()
signer = TimestampSigner()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='student')
        headers = self.get_success_headers(serializer.data)
        verification_token = signer.sign(user.pk)
        return Response(
            {
                'user': UserSerializer(user).data,
                'verification_token': verification_token,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            raise ValidationError({'token': 'Verification token is required.'})
        try:
            user_id = signer.unsign(token, max_age=60 * 60 * 24 * 7)
        except SignatureExpired as exc:
            raise ValidationError({'token': 'Verification token has expired.'}) from exc
        except BadSignature as exc:
            raise ValidationError({'token': 'Invalid verification token.'}) from exc
        user = generics.get_object_or_404(User, pk=user_id)
        user.is_email_verified = True
        user.save()
        return Response({'message': 'Email verified'})

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=400)
        try:
            refresh = RefreshToken(refresh_token)
            return Response({'access': str(refresh.access_token)})
        except:
            return Response({'error': 'Invalid refresh token'}, status=400)

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminUserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can view users.')
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        status_value = self.request.query_params.get('status')
        if role:
            queryset = queryset.filter(role=role)
        if status_value == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_value == 'inactive':
            queryset = queryset.filter(is_active=False)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can create users.')
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return AdminUserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can manage users.')
        return User.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can update users.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can delete users.')
        instance.is_active = False
        instance.save(update_fields=['is_active'])

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can view audit logs.')
        return AuditLog.objects.all()
