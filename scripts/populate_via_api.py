"""
Populate the API with many records via REST calls.

This script is updated to work with the refactored API that uses foreign key IDs.
It first creates parent entities (Faculties, Departments, Teachers),
collects their IDs, and then uses these IDs to create dependent entities
(Groups, Subjects, Sessions).
"""
import requests
from random import randint, choice
from datetime import date, timedelta
import sys

BASE_URL = "http://localhost:8000"

# --- Data for population ---
FACULTIES_DATA = ["Computer Science", "Applied Mathematics", "Physics", "History", "Philology"]
DEPARTMENTS_DATA = ["Software Engineering", "Theoretical Physics", "Ancient History", "English Literature", "Computational Maths"]
TEACHERS_DATA = ["Dr. Alan Turing", "Dr. Albert Einstein", "Dr. Marie Curie", "Dr. Herodotus", "Dr. William Shakespeare"]

# --- Helper to make requests and handle errors ---
def post_data(endpoint, payload):
    """Posts data to an endpoint and returns the JSON response."""
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"SUCCESS: POST {endpoint} with {payload} -> {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: POST {endpoint} with {payload} -> {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}", file=sys.stderr)
        return None

# --- Step 1: Create independent entities and store their IDs ---
def create_and_get_ids(endpoint, data_list):
    """Creates entities from a list of names and returns a list of their full objects."""
    created_items = []
    for name in data_list:
        payload = {"name": name}
        response_json = post_data(endpoint, payload)
        if response_json:
            created_items.append(response_json)
    return created_items

# --- Step 2: Create dependent entities ---
def create_groups(faculty_ids: list, num_groups=50):
    """Creates groups using a list of faculty IDs."""
    if not faculty_ids:
        print("ERROR: No faculty IDs provided. Cannot create groups.", file=sys.stderr)
        return []
    
    created_groups = []
    for i in range(num_groups):
        payload = {
            "code": f"G{1000 + i}",
            "course": randint(1, 5),
            "num_students": randint(15, 30),
            "faculty_id": choice(faculty_ids)
        }
        response_json = post_data("/groups/", payload)
        if response_json:
            created_groups.append(response_json)
    return created_groups

def create_subjects(department_ids: list, num_subjects=50):
    """Creates subjects using a list of department IDs."""
    if not department_ids:
        print("ERROR: No department IDs provided. Cannot create subjects.", file=sys.stderr)
        return []

    created_subjects = []
    for i in range(num_subjects):
        payload = {
            "name": f"Subject {i+1}",
            "num_hours": choice([32, 48, 64, 96]),
            "department_id": choice(department_ids),
            "extra": {
                "notes": f"This subject covers topics {i+1} and patterns {i%5+1}.",
                "tags": [f"tag{i%3+1}", f"level{i%5+1}"]
            }
        }
        response_json = post_data("/subjects/", payload)
        if response_json:
            created_subjects.append(response_json)
    return created_subjects

def create_sessions(group_ids: list, subject_ids: list, teacher_ids: list, num_sessions=200):
    """Creates sessions using lists of group, subject, and teacher IDs."""
    if not all([group_ids, subject_ids, teacher_ids]):
        print("ERROR: Missing IDs for groups, subjects, or teachers. Cannot create sessions.", file=sys.stderr)
        return

    for _ in range(num_sessions):
        payload = {
            "group_id": choice(group_ids),
            "subject_id": choice(subject_ids),
            "teacher_id": choice(teacher_ids),
            "control_type": choice(["exam","test","practical"]),
            "session_date": str(date.today() - timedelta(days=randint(0, 365)))
        }
        post_data("/sessions/", payload)

if __name__ == '__main__':
    print("--- 1. Creating Faculties ---")
    faculties = create_and_get_ids("/faculties/", FACULTIES_DATA)
    faculty_ids = [f['id'] for f in faculties]

    print("\n--- 2. Creating Departments ---")
    departments = create_and_get_ids("/departments/", DEPARTMENTS_DATA)
    department_ids = [d['id'] for d in departments]

    print("\n--- 3. Creating Teachers ---")
    teachers = create_and_get_ids("/teachers/", TEACHERS_DATA)
    teacher_ids = [t['id'] for t in teachers]

    print("\n--- 4. Creating Groups ---")
    groups = create_groups(faculty_ids, num_groups=50)
    group_ids = [g['id'] for g in groups]

    print("\n--- 5. Creating Subjects ---")
    subjects = create_subjects(department_ids, num_subjects=40)
    subject_ids = [s['id'] for s in subjects]

    print("\n--- 6. Creating Sessions ---")
    create_sessions(group_ids, subject_ids, teacher_ids, num_sessions=200)

    print("\n--- Population complete! ---")
