from rest_framework import serializers
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'teacher', 'teacher_name', 'created_at']
        read_only_fields = ['teacher', 'teacher_name', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'assignment_title', 'student', 'student_name', 'content', 'file', 'submitted_at', 'grade', 'feedback']
        read_only_fields = ['student', 'student_name', 'submitted_at', 'grade', 'feedback']

class GradeSerializer(serializers.Serializer):
    grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(required=False)
