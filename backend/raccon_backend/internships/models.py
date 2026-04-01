from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Internship(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='internship')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.company}"

class InternshipLog(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='logs')
    week = models.PositiveIntegerField()
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ['internship', 'week']

    def __str__(self):
        return f"Week {self.week} - {self.internship.student.username}"