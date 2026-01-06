# Mini Assessment Engine (Acad AI)

A Django-based REST API for managing exams, questions, and student submissions. 
Features automated grading with a modular design that supports both keyword matching and Generative AI (Gemini) feedback.

## Features
* **User Authentication**: Secure login/registration (Standard Django Auth).
* **Assessment Flow**: Manage Exams -> Questions (MCQ/SA) -> Submissions.
* **Automated Grading**:
    * MCQ: Exact match verification.
    * Short Answer: Keyword density analysis + Generative AI feedback.
* **Security**: Students can only view and submit their own work.

## Prerequisites
* Python 3.9+
* Google Gemini API Key (for AI powered feedback)

## Installation

1. Clone repository

    ```bash
    git clone https://github.com/MikaTech-dev/mini-assessment-engine.git```
2. cd into cloned repository
    ```bash
    cd ./mini-assessment-engine
    ```

3.  **Create and Activate Virtual Environment**
    * Windows:
        ```bash
        python -m venv .venv
        ./.venv/Scripts/activate
        ```
    * Mac/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

4. **Install dependencies**
    * Production dependencies:
        ```bash
        pip install -r ./requirements.py
        ```
    * Development dependencies``
        ```bash
        pip install -r ./dev-requirements.txt
        ```

6. **Migrate models onto database using existing migration files**
    ```bash
    python manage.py migrate
    ```

7. **Run the seeder (located @./api/management/commands/seed_db.py)**
    ```bash
    python manage.py seed_db
    ```
    * **Admin Creds:** `admin` / `admin123`
    * **Student Creds:** `student` / `password123`  
`Note: the seeder deletes all existing Users, Exams, and their related entities (due to "cascade on delete")`
<!-- or if need be, manually create a Superuser

    python manage.py createsuperuser
You could use the details in .env.example to create an admin user -->

8.  **Environment Setup**
    Create a `.env` file in the root directory:
    * Windows/Mac/Linux
        ```bash
        cp .env.example .env
        ```
    In the newly created .env file, replace "\<Your api key here>" with your actual Gemini_API_Key

9. **Run server**
    ```bash
    python manage.py runserver
    ```
    Access the API at http://127.0.0.1:8000/api/.

## API Documentation
There are two ways to view the API documentation:
1. Interactive Swagger UI:
    * Run the server and visit: http://127.0.0.1:8000/api/docs/

2. Postman Collection:
    * Import the postman_collection.json file included in this repository into Postman
    * Create a new environment and add `http://127.0.0.1:8000` as the base url

## Testing the Grading Logic
1. Log in as the seeded student (using Basic Auth).
2. Submit a POST request to /api/submissions/ with answers.
3. The system will automatically:
    * Calculate the score based on correct options/keywords.
    * Call the Gemini API to generate helpful textual feedback for Short Answer-type questions in particular