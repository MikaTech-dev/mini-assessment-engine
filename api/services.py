def grade_submission(submission):
    """
    Modular grading service to evaluate a submission.
    Currently implements a Mock Grading Service using keyword matching.
    """
    # TODO: Implement AI integration to help grade a and provide feedback on SA (Short answer questions)
    total_questions = submission.exam.questions.count()
    correct_count = 0
    feedback_notes = []

    # Get all student answers for this submission
    answers = submission.answers.all()

    for ans in answers:
        question = ans.question
        # if question is Multiple Choice Question
        if question.question_type == 'MCQ':
            expected = question.correct_answers.get('answer')
            actual = ans.student_answer.get('choice')

            if expected == actual:
                ans.is_correct = True
                correct_count += 1
            else:
                ans.is_correct = False
                feedback_notes.append(f"Q{question.order}: Expected {expected}, got {actual}.")

        # if question is Short Answer (SA) - Keyword Matching
        elif question.question_type == 'SA':
            expected_keywords = question.correct_answers.get('keywords', [])
            student_text = ans.student_answer.get('text', '').lower()

            # Checks for how many keywords match
            matches = [word for word in expected_keywords if word.lower() in student_text]
            if len(matches) >= len(expected_keywords) * 0.666: # 66% match threshold (1 matching keyword at least...)
                ans.is_correct = True
                correct_count += 1
            else:
                ans.is_correct = False
                feedback_notes.append(f"Q{question.order}: Missed key concepts.")

        ans.save()

    # Calculate final score
    if total_questions > 0:
        submission.total_score = (correct_count / total_questions) * 100

    submission.status = 'graded' # Update status per requirement
    submission.feedback = " ".join(feedback_notes) if feedback_notes else "Excellent work!"
    submission.save()
