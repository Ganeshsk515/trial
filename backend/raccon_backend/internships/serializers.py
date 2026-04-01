from rest_framework import serializers
from .models import Internship, InternshipLog

class InternshipSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Internship
        fields = ['id', 'student', 'student_name', 'company', 'position', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['student_name', 'created_at']

class InternshipLogSerializer(serializers.ModelSerializer):
    internship_company = serializers.CharField(source='internship.company', read_only=True)

    class Meta:
        model = InternshipLog
        fields = ['id', 'internship', 'internship_company', 'week', 'content', 'submitted_at', 'feedback', 'reviewed_at']
        read_only_fields = ['internship', 'internship_company', 'submitted_at', 'feedback', 'reviewed_at']

class InternshipLogReviewSerializer(serializers.Serializer):
    feedback = serializers.CharField()
