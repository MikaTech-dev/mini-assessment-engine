# from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Exam, Submission
from .serializers import ExamSerializer, SubmissionSerializer
from .services import grade_submission

class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows exams to be viewed or listed.
    READ-ONLY: Users (Students) cannot create or modify exams here.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for students to submit exams and view their submission history.
    """
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensuring users only have access to their own submission
        return Submission.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        # link submission to the actual user
        submission= serializer.save(student=self.request.user)
        grade_submission(submission)
