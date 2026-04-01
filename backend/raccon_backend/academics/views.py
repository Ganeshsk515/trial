from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
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
        if self.request.user.role != 'teacher':
            raise PermissionDenied('Only teachers can create assignments.')
        serializer.save(teacher=self.request.user)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects.all()

    def _ensure_teacher_owner(self, assignment):
        if self.request.user.role != 'teacher' or assignment.teacher_id != self.request.user.id:
            raise PermissionDenied('Only the teacher owner can modify this assignment.')

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        self._ensure_teacher_owner(assignment)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        self._ensure_teacher_owner(assignment)
        return super().destroy(request, *args, **kwargs)

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        assignment = get_object_or_404(Assignment, id=assignment_id)
        user = self.request.user
        if user.role == 'teacher':
            if assignment.teacher_id != user.id:
                raise PermissionDenied('You can only view submissions for your own assignments.')
            return Submission.objects.filter(assignment=assignment)
        if user.role == 'student':
            return Submission.objects.filter(assignment=assignment, student=user)
        if user.role == 'admin':
            return Submission.objects.filter(assignment=assignment)
        return Submission.objects.none()

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied('Only students can submit.')
        serializer.save(student=self.request.user)

class SubmissionGradeView(generics.UpdateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.role != 'teacher':
            raise PermissionDenied('Only teachers can grade.')
        submission = self.get_object()
        if submission.assignment.teacher_id != request.user.id:
            raise PermissionDenied('You can only grade submissions for your own assignments.')
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
