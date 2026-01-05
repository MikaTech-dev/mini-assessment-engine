import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Exam, Question

class Command(BaseCommand):
    help = 'Seeds the database with initial test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear all existing data (Optional, comment this ssection out out if need be )
        Exam.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write('Old data cleared.')

        # Creating a studentuser for testing
        student, created = User.objects.get_or_create(username='student', email='student@test.com')
        if created:
            student.set_password('password123')
            student.save()

        # An admin/superuser for checking the panel
        admin_user, created = User.objects.get_or_create(username='admin', email='admin@test.com')
        if created:
            admin_user.set_password('admin123')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()

        # Create an Exam
        exam = Exam.objects.create(
            title='Intro to Physics',
            duration=datetime.timedelta(minutes=60), # 1 Hour
            course_name='PHY101',
            metadata='Mid-term assessment covering Newton\'s Laws.'
        )

        # Create Exam questions
        # Q1: MCQ
        Question.objects.create(
            exam=exam,
            question_text="What is the unit of Force?",
            question_type='MCQ',
            # Storing the list of options as a dictionary
            options={'options': ['Newton', 'Joule', 'Pascal', 'Watt']},
            # Stores the correct answer in the answer key
            correct_answers={'answer': 'Newton'},
            order=1
        )

        # Q2: MCQ
        Question.objects.create(
            exam=exam,
            question_text="Which law states F=ma?",
            question_type='MCQ',
            options={'options': ['1st Law', '2nd Law', '3rd Law']},
            correct_answers={'answer': '2nd Law'},
            order=2
        )

        # Q3: Short Answer (text, no options)
        Question.objects.create(
            exam=exam,
            question_text="Define 'Velocity' in one sentence.",
            question_type='SA',
            options={}, # Empty cause SA
            correct_answers={'keywords': ['speed', 'direction', 'vector']},
            order=3
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        self.stdout.write('Student Login: student / password123')
        self.stdout.write('Admin Login:   admin / admin123')
