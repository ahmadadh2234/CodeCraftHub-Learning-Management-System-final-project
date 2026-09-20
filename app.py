"""
CodeCraftHub - Course REST API

This Flask application provides CRUD operations for courses and stores
course data in a local JSON file named courses.json.

Run the application with:

    python app.py

The API will be available at:

    http://127.0.0.1:5000
"""

from datetime import datetime
from pathlib import Path
import json

from flask import Flask, jsonify, request


# Create the Flask application
app = Flask(__name__)


# Store courses.json in the same directory as this app.py file
DATA_FILE = Path(__file__).parent / "courses.json"


# The only status values accepted by the API
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}


def ensure_data_file():
    """
    Create courses.json automatically if it does not exist.

    The file starts with an empty JSON list because courses will be
    stored as a list of course objects.
    """
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file, indent=2)


def load_courses():
    """
    Read and return all courses from courses.json.

    Raises:
        OSError: If the file cannot be opened or read.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValueError: If the JSON file does not contain a list.
    """
    # Make sure the file exists before trying to read it
    ensure_data_file()

    with DATA_FILE.open("r", encoding="utf-8") as file:
        courses = json.load(file)

    # The application expects the top-level JSON value to be a list
    if not isinstance(courses, list):
        raise ValueError("courses.json must contain a JSON list")

    return courses


def save_courses(courses):
    """
    Save the list of courses to courses.json.

    Raises:
        OSError: If the file cannot be opened or written.
    """
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(courses, file, indent=2)


def get_next_course_id(courses):
    """
    Generate the next course ID.

    The first course receives ID 1. For later courses, the next ID is
    one greater than the largest existing ID.
    """
    if not courses:
        return 1

    return max(course["id"] for course in courses) + 1


def get_current_timestamp():
    """
    Return the current UTC time in ISO 8601 format.

    Example:
        2026-09-20T14:30:00+00:00
    """
    return datetime.now().astimezone().isoformat()


def validate_course_data(data):
    """
    Validate data submitted when creating or updating a course.

    Returns:
        None if the data is valid.
        A string containing an error message otherwise.
    """
    # These fields must be included in POST and PUT requests
    required_fields = {
        "name",
        "description",
        "target_date",
        "status",
    }

    # Check for missing fields
    missing_fields = required_fields - data.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        return f"Missing required field(s): {missing}"

    # Check that name and description contain useful text
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "The 'name' field is required and must not be empty"

    if not isinstance(data["description"], str) or not data["description"].strip():
        return "The 'description' field is required and must not be empty"

    # Check the status value
    if data["status"] not in VALID_STATUSES:
        return (
            "Invalid status. Status must be one of: "
            "'Not Started', 'In Progress', or 'Completed'"
        )

    # Check the date format
    target_date = data["target_date"]

    if not isinstance(target_date, str):
        return "The 'target_date' field must be a string in YYYY-MM-DD format"

    try:
        # strptime verifies both the format and whether the date is valid
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return "The 'target_date' field must use the format YYYY-MM-DD"

    return None


def find_course(courses, course_id):
    """
    Find a course by its ID.

    Returns:
        The matching course dictionary, or None if no course is found.
    """
    return next(
        (course for course in courses if course["id"] == course_id),
        None,
    )


@app.post("/api/courses")
def create_course():
    """
    Add a new course.

    Endpoint:
        POST /api/courses
    """
    # silent=True prevents Flask from raising an exception for malformed JSON
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain a valid JSON object"
        }), 400

    # Validate all required course fields
    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        courses = load_courses()

        # Build the new course object
        new_course = {
            "id": get_next_course_id(courses),
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": get_current_timestamp(),
        }

        courses.append(new_course)
        save_courses(courses)

        return jsonify(new_course), 201

    except (OSError, json.JSONDecodeError, ValueError) as error:
        return jsonify({
            "error": "Unable to read or write courses.json",
            "details": str(error),
        }), 500


@app.get("/api/courses")
def get_courses():
    """
    Get all courses.

    Endpoint:
        GET /api/courses
    """
    try:
        courses = load_courses()
        return jsonify(courses), 200

    except (OSError, json.JSONDecodeError, ValueError) as error:
        return jsonify({
            "error": "Unable to read courses.json",
            "details": str(error),
        }), 500


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """
    Get one course by its ID.

    Endpoint:
        GET /api/courses/<course_id>

    Example:
        GET /api/courses/1
    """
    try:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found"
            }), 404

        return jsonify(course), 200

    except (OSError, json.JSONDecodeError, ValueError) as error:
        return jsonify({
            "error": "Unable to read courses.json",
            "details": str(error),
        }), 500


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    """
    Update an existing course.

    PUT requests must include all required course fields.
    The ID and created_at values cannot be changed.

    Endpoint:
        PUT /api/courses/<course_id>
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain a valid JSON object"
        }), 400

    # PUT expects all editable fields to be supplied
    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found"
            }), 404

        # Update editable fields only
        course["name"] = data["name"].strip()
        course["description"] = data["description"].strip()
        course["target_date"] = data["target_date"]
        course["status"] = data["status"]

        # ID and created_at remain unchanged
        save_courses(courses)

        return jsonify(course), 200

    except (OSError, json.JSONDecodeError, ValueError) as error:
        return jsonify({
            "error": "Unable to read or write courses.json",
            "details": str(error),
        }), 500


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    """
    Delete a course by its ID.

    Endpoint:
        DELETE /api/courses/<course_id>

    Example:
        DELETE /api/courses/1
    """
    try:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found"
            }), 404

        courses.remove(course)
        save_courses(courses)

        return jsonify({
            "message": f"Course with ID {course_id} was deleted successfully"
        }), 200

    except (OSError, json.JSONDecodeError, ValueError) as error:
        return jsonify({
            "error": "Unable to read or write courses.json",
            "details": str(error),
        }), 500


@app.errorhandler(404)
def handle_not_found(error):
    """
    Return JSON instead of Flask's default HTML 404 response
    when an endpoint does not exist.
    """
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """
    Return JSON when the correct endpoint exists but the HTTP method
    is not supported.
    """
    return jsonify({
        "error": "HTTP method not allowed for this endpoint"
    }), 405


if __name__ == "__main__":
    # Create courses.json when the application starts.
    # If the file cannot be created, show a helpful message.
    try:
        ensure_data_file()
        print(f"Using course data file: {DATA_FILE}")
    except OSError as error:
        print(f"Warning: Could not create courses.json: {error}")

    # debug=True is useful while learning and developing.
    # Turn it off in production.
    app.run(debug=True)
