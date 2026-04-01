from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Internship, InternshipLog
from .serializers import InternshipSerializer, InternshipLogSerializer, InternshipLogReviewSerializer

class InternshipMyView(generics.RetrieveAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Internship, student=self.request.user)

class InternshipCreateView(generics.CreateAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Only admins can create internships.')
        serializer.save()

class InternshipLogListCreateView(generics.ListCreateAPIView):
    serializer_class = InternshipLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        internship_id = self.request.query_params.get('internshipId')
        if internship_id:
            internship = get_object_or_404(Internship, id=internship_id)
            user = self.request.user
            if user.role == 'student':
                if internship.student_id != user.id:
                    raise PermissionDenied('You can only view your own internship logs.')
                return InternshipLog.objects.filter(internship=internship)
            if user.role in {'teacher', 'admin'}:
                return InternshipLog.objects.filter(internship=internship)
        return InternshipLog.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied('Only students can submit logs.')
        internship = get_object_or_404(Internship, student=self.request.user)
        serializer.save(internship=internship)

class InternshipLogReviewView(generics.UpdateAPIView):
    serializer_class = InternshipLogReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InternshipLog.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.role != 'teacher':
            raise PermissionDenied('Only teachers can review logs.')
        log = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            log.feedback = serializer.validated_data['feedback']
            from django.utils import timezone
            log.reviewed_at = timezone.now()
            log.save()
            return Response(InternshipLogSerializer(log).data)
        return Response(serializer.errors, status=400)
