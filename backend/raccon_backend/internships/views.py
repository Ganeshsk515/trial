from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
        if self.request.user.role == 'admin':
            serializer.save()
        else:
            return Response({'error': 'Only admins can create internships'}, status=403)

class InternshipLogCreateView(generics.CreateAPIView):
    serializer_class = InternshipLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'student':
            internship = get_object_or_404(Internship, student=self.request.user)
            serializer.save(internship=internship)
        else:
            return Response({'error': 'Only students can submit logs'}, status=403)

class InternshipLogListView(generics.ListAPIView):
    serializer_class = InternshipLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        internship_id = self.request.query_params.get('internshipId')
        if internship_id:
            internship = get_object_or_404(Internship, id=internship_id)
            return InternshipLog.objects.filter(internship=internship)
        return InternshipLog.objects.none()

class InternshipLogReviewView(generics.UpdateAPIView):
    serializer_class = InternshipLogReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InternshipLog.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can review logs'}, status=403)
        log = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            log.feedback = serializer.validated_data['feedback']
            from django.utils import timezone
            log.reviewed_at = timezone.now()
            log.save()
            return Response(InternshipLogSerializer(log).data)
        return Response(serializer.errors, status=400)