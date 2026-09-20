from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "courses.json"

VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}


def load_courses():
    """Read courses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_courses(courses):
    """Write courses to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(courses, file, indent=2)


def find_course(courses, course_id):
    """Find a course by its numeric ID."""
    return next(
        (course for course in courses if course["id"] == course_id),
        None
    )


@app.get("/api/courses")
def get_courses():
    courses = load_courses()
    return jsonify(courses)


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course)


@app.post("/api/courses")
def create_course():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "description",
        "target_completion_date",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    if data["status"] not in VALID_STATUSES:
        return jsonify({
            "error": "Invalid status",
            "allowed_values": list(VALID_STATUSES)
        }), 400

    courses = load_courses()

    new_id = max(
        [course["id"] for course in courses],
        default=0
    ) + 1

    new_course = {
        "id": new_id,
        "name": data["name"],
        "description": data["description"],
        "target_completion_date": data["target_completion_date"],
        "status": data["status"]
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    data = request.get_json(silent=True) or {}
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    required_fields = [
        "name",
        "description",
        "target_completion_date",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    if data["status"] not in VALID_STATUSES:
        return jsonify({
            "error": "Invalid status",
            "allowed_values": list(VALID_STATUSES)
        }), 400

    course.update({
        "name": data["name"],
        "description": data["description"],
        "target_completion_date": data["target_completion_date"],
        "status": data["status"]
    })

    save_courses(courses)

    return jsonify(course)


@app.patch("/api/courses/<int:course_id>/status")
def update_course_status(course_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in VALID_STATUSES:
        return jsonify({
            "error": "Invalid status",
            "allowed_values": list(VALID_STATUSES)
        }), 400

    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    course["status"] = status
    save_courses(courses)

    return jsonify(course)


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    courses.remove(course)
    save_courses(courses)

    return jsonify({
        "message": "Course deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)