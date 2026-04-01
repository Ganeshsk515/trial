from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Assignment.objects.filter(teacher=user)
        elif user.role == 'student':
            return Assignment.objects.all()
        return Assignment.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role == 'teacher':
            serializer.save(teacher=self.request.user)
        else:
            return Response({'error': 'Only teachers can create assignments'}, status=403)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Assignment.objects.filter(teacher=user)
        return Assignment.objects.all()

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        assignment = get_object_or_404(Assignment, id=assignment_id)
        return Submission.objects.filter(assignment=assignment)

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'student':
            serializer.save(student=self.request.user)
        else:
            return Response({'error': 'Only students can submit'}, status=403)

class SubmissionGradeView(generics.UpdateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can grade'}, status=403)
        submission = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            submission.grade = serializer.validated_data.get('grade')
            submission.feedback = serializer.validated_data.get('feedback', '')
            submission.save()
            return Response(SubmissionSerializer(submission).data)
        return Response(serializer.errors, status=400)

class AssignmentReportsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can view reports'}, status=403)
        total_assignments = Assignment.objects.count()
        total_submissions = Submission.objects.count()
        graded_submissions = Submission.objects.filter(grade__isnull=False).count()
        average_grade = Submission.objects.filter(grade__isnull=False).aggregate(avg=models.Avg('grade'))['grade__avg']
        return Response({
            'total_assignments': total_assignments,
            'total_submissions': total_submissions,
            'graded_submissions': graded_submissions,
            'average_grade': average_grade,
        })