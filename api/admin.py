from django.contrib import admin

# Register your models here.
from .models import Exam, Question, Submission, Answer

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1 # Shows one empty question slot by default

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name', 'duration', 'created_at')
    inlines = [QuestionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'student_answer', 'is_correct')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'submitted_at', 'status', 'total_score')
    list_filter = ('status', 'exam')
    readonly_fields = ('submitted_at',)
    inlines = [AnswerInline]

admin.site.register(Question)
admin.site.register(Answer)
