from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exam, Question, Submission, Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options', 'order']

class ExamSerializer(serializers.ModelSerializer):
    #  Embedding qustions inside the exam details
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'duration', 'course_name', 'metadata', 'questions', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'student_answer', 'is_correct']
        read_only_fields = ['is_correct']

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 
            'student', 
            'exam', 
            'submitted_at', 
            'total_score', 
            'feedback', 
            'status', 
            'answers'
            ]
        # These fields will br created/filled by the grading.service(TBD), not by the student
        read_only_fields = ['total_score', 'feedback', 'status', 'submitted_at']    
    def create(self, validated_data):
        """
        Handles creating the Submission AND the nested Answers in one go.
        """
        answers_data = validated_data.pop('answers')
        # Creating the Submission instance
        submission = Submission.objects.create(**validated_data)

        # Creating the Answers instance
        for answer_data in answers_data:
            Answer.objects.create(submission=submission, **answer_data)

        return submission
