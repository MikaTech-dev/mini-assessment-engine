from django.db import models

# Create your models here.
from django.contrib.auth.models import User  # Inbuilt auth User model

class Exam(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    course_name = models.CharField(max_length=255)
    metadata = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    # Defining enums/choices
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('SA', 'Short Answer'),
    ]

    exam: Exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=3, choices=QUESTION_TYPES,
          default='MCQ'
          )   # using choices

    # Flexible storage for options (e.g. ["A", "B", "C"]) and correct answers
    options = models.JSONField(
        default=dict, blank=True, help_text="For MCQs: {'options': ['A', 'B', 'C']}")
    correct_answers = models.JSONField(default=dict, help_text="e.g. {'answer': 'B'}")
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        examObject: Exam = self.exam
        return f"{examObject} - Q{self.order}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('graded', 'Graded'),
    ]

    # Link the submission to the inbuilt User model via FK
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # Allow score and feedback to be blank (nullable) initially until graded
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"

class Answer(models.Model):
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.JSONField()
    # Optional: store individual score per question if needed later
    is_correct = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"Ans: {self.question.id} for Sub: {self.submission.id}"
