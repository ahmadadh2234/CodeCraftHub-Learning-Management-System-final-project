# CodeCraftHub

CodeCraftHub is a beginner-friendly REST API for tracking courses that you want to learn.

The project is built with:

- Python
- Flask
- JSON file storage
- REST API principles
- `curl` for testing

Course data is stored in a local file named `courses.json`. No database, authentication, or user management is required.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Course Data Format](#course-data-format)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Learning REST API Basics](#learning-rest-api-basics)

---

## Project Overview

CodeCraftHub allows developers to track courses they want to learn.

Each course contains:

- An automatically generated ID
- A course name
- A course description
- A target completion date
- A learning status
- An automatically generated creation timestamp

The application provides a REST API that allows users to:

- Create courses
- View courses
- Update courses
- Delete courses

These operations are commonly called CRUD:

|
 Operation 
|
 HTTP Method 
|
|
---
|
---
|
|
 Create 
|
`POST`
|
|
 Read 
|
`GET`
|
|
 Update 
|
`PUT`
|
|
 Delete 
|
`DELETE`
|

---

## Features

- Create new courses
- View all courses
- View one course by ID
- Update existing courses
- Delete courses
- Automatically generate course IDs
- Automatically generate creation timestamps
- Store course data in `courses.json`
- Automatically create `courses.json` if it does not exist
- Validate required fields
- Validate course dates
- Validate course status values
- Return JSON responses
- Return helpful error messages
- Handle courses that cannot be found
- Handle invalid JSON data
- Handle file read and write errors

Valid course statuses are:

```text
Not Started
In Progress
Completed
```

---

## Requirements

Before installing CodeCraftHub, make sure you have:

- Python 3.9 or newer
- `pip`
- A terminal or command prompt
- Optional: `curl` for testing API requests

Check your Python installation:

```bash
python --version
```

On some systems, use:

```bash
python3 --version
```

Check that `pip` is installed:

```bash
pip --version
```

---

## Installation

### 1. Open the project folder

If you downloaded the project, open a terminal and navigate to the project directory:

```bash
cd codecrafthub
```

If the project is hosted in a Git repository, clone it with:

```bash
git clone https://github.com/your-username/codecrafthub.git
cd codecrafthub
```

---

### 2. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

#### macOS or Linux

```bash
python3 -m venv venv
```

#### Windows

```bash
python -m venv venv
```

---

### 3. Activate the virtual environment

#### macOS or Linux

```bash
source venv/bin/activate
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

After activation, your terminal may display `(venv)` at the beginning of the command line.

---

### 4. Install Flask

If the project contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` file, install Flask directly:

```bash
pip install Flask
```

A basic `requirements.txt` file should contain:

```text
Flask
```

---

## Running the Application

Start the Flask application with:

```bash
python app.py
```

On macOS or Linux, you may need to use:

```bash
python3 app.py
```

You should see output similar to:

```text
Using course data file: /path/to/codecrafthub/courses.json
 * Running on http://127.0.0.1:5000
```

The API is now available at:

```text
http://127.0.0.1:5000
```

Keep the terminal running while testing the API.

To stop the application, press:

```text
Ctrl+C
```

### Development mode

The application uses Flask debug mode while developing:

```python
app.run(debug=True)
```

Debug mode automatically reloads the application when code changes.

Do not use debug mode for a public production application.

---

## Course Data Format

Every course has the following fields:

|
 Field 
|
 Required 
|
 Description 
|
|
---
|
---:
|
---
|
|
`id`
|
 Automatically generated 
|
 Unique numeric course ID 
|
|
`name`
|
 Yes 
|
 Name of the course 
|
|
`description`
|
 Yes 
|
 Description of the course 
|
|
`target_date`
|
 Yes 
|
 Target date in 
`YYYY-MM-DD`
 format 
|
|
`status`
|
 Yes 
|
 Current learning status 
|
|
`created_at`
|
 Automatically generated 
|
 Course creation timestamp 
|

### Example course

```json
{
  "id": 1,
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
  "target_date": "2026-10-15",
  "status": "Not Started",
  "created_at": "2026-09-20T14:30:00+00:00"
}
```

### Valid date format

Dates must use:

```text
YYYY-MM-DD
```

Example:

```text
2026-10-15
```

Invalid examples include:

```text
10-15-2026
2026/10/15
15-10-2026
```

### Valid statuses

The status must be exactly one of these values:

```text
Not Started
In Progress
Completed
```

Status values are case-sensitive. For example, this value is invalid:

```text
completed
```

---

## API Endpoints

The base URL for all API requests is:

```text
http://127.0.0.1:5000
```

### Endpoint summary

|
 Method 
|
 Endpoint 
|
 Description 
|
|
---
|
---
|
---
|
|
`POST`
|
`/api/courses`
|
 Create a course 
|
|
`GET`
|
`/api/courses`
|
 Get all courses 
|
|
`GET`
|
`/api/courses/<id>`
|
 Get one course 
|
|
`PUT`
|
`/api/courses/<id>`
|
 Update a course 
|
|
`DELETE`
|
`/api/courses/<id>`
|
 Delete a course 
|

Replace `<id>` with an actual course ID, such as `1`.

---

## Create a Course

### Request

```text
POST /api/courses
```

### `curl` command

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
    "target_date": "2026-10-15",
    "status": "Not Started"
  }'
```

### Request body

```json
{
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
  "target_date": "2026-10-15",
  "status": "Not Started"
}
```

The `id` and `created_at` fields are generated automatically by the server.

### Successful response

Status:

```text
201 Created
```

Response:

```json
{
  "id": 1,
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
  "target_date": "2026-10-15",
  "status": "Not Started",
  "created_at": "2026-09-20T14:30:00+00:00"
}
```

The exact `created_at` value will be different.

---

## Get All Courses

### Request

```text
GET /api/courses
```

### `curl` command

```bash
curl -i http://127.0.0.1:5000/api/courses
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
[
  {
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
    "target_date": "2026-10-15",
    "status": "Not Started",
    "created_at": "2026-09-20T14:30:00+00:00"
  }
]
```

If there are no courses, the response is:

```json
[]
```

---

## Get One Course

### Request

```text
GET /api/courses/<id>
```

### `curl` command

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
  "id": 1,
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, JSON, status codes, and REST principles.",
  "target_date": "2026-10-15",
  "status": "Not Started",
  "created_at": "2026-09-20T14:30:00+00:00"
}
```

---

## Update a Course

### Request

```text
PUT /api/courses/<id>
```

A `PUT` request must include all required editable fields:

- `name`
- `description`
- `target_date`
- `status`

The `id` and `created_at` fields are not changed.

### `curl` command

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals - Updated",
    "description": "Learn REST principles, JSON, API testing, and HTTP methods.",
    "target_date": "2026-10-20",
    "status": "In Progress"
  }'
```

### Request body

```json
{
  "name": "REST API Fundamentals - Updated",
  "description": "Learn REST principles, JSON, API testing, and HTTP methods.",
  "target_date": "2026-10-20",
  "status": "In Progress"
}
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
  "id": 1,
  "name": "REST API Fundamentals - Updated",
  "description": "Learn REST principles, JSON, API testing, and HTTP methods.",
  "target_date": "2026-10-20",
  "status": "In Progress",
  "created_at": "2026-09-20T14:30:00+00:00"
}
```

---

## Delete a Course

### Request

```text
DELETE /api/courses/<id>
```

### `curl` command

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
  "message": "Course with ID 1 was deleted successfully"
}
```

---

## Error Responses

The API returns JSON error messages when a request cannot be completed.

### Missing required fields

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "Missing required field(s): description, status, target_date"
}
```

### Invalid status

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "This course uses an invalid status.",
    "target_date": "2026-12-01",
    "status": "Pending"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "Invalid status. Status must be one of: 'Not Started', 'In Progress', or 'Completed'"
}
```

### Invalid date

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "This course uses an invalid date.",
    "target_date": "12-01-2026",
    "status": "Not Started"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "The 'target_date' field must use the format YYYY-MM-DD"
}
```

### Course not found

```bash
curl -i http://127.0.0.1:5000/api/courses/9999
```

Expected status:

```text
404 Not Found
```

Example response:

```json
{
  "error": "Course with ID 9999 not found"
}
```

### Invalid JSON

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Invalid JSON",'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "Request body must contain a valid JSON object"
}
```

---

## Testing

Make sure the application is running:

```bash
python app.py
```

Then open another terminal window and run the commands below.

### 1. Create a course

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python for Beginners",
    "description": "Learn Python programming from the beginning.",
    "target_date": "2026-11-01",
    "status": "Not Started"
  }'
```

### 2. Get all courses

```bash
curl -i http://127.0.0.1:5000/api/courses
```

### 3. Get course ID 1

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

### 4. Update course ID 1

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python for Beginners",
    "description": "Learn Python programming and build small projects.",
    "target_date": "2026-11-15",
    "status": "In Progress"
  }'
```

### 5. Delete course ID 1

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

### 6. Confirm deletion

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

The final request should return:

```text
404 Not Found
```

---

## Testing with Postman

You can also test the API with [Postman](https://www.postman.com/).

1. Open Postman.
2. Select an HTTP method, such as `GET` or `POST`.
3. Enter an API URL.
4. For `POST` and `PUT` requests:
   - Select the **Body** tab.
   - Select **raw**.
   - Select **JSON**.
   - Enter a JSON request body.
5. Click **Send**.

Example URL:

```text
http://127.0.0.1:5000/api/courses
```

For `POST` and `PUT` requests, include this header:

```text
Content-Type: application/json
```

---

## Useful HTTP Status Codes

|
 Status Code 
|
 Meaning 
|
|
---:
|
---
|
|
`200`
|
 Request succeeded 
|
|
`201`
|
 Resource was created 
|
|
`400`
|
 Request contains invalid data 
|
|
`404`
|
 Endpoint or course was not found 
|
|
`405`
|
 HTTP method is not allowed 
|
|
`500`
|
 Server encountered an internal error 
|

---

## Troubleshooting

### Python command is not found

Try:

```bash
python3 --version
```

If that works, run the application with:

```bash
python3 app.py
```

On Windows, reinstall Python and make sure the option to add Python to `PATH` is selected.

---

### Flask is not installed

You may see:

```text
ModuleNotFoundError: No module named 'flask'
```

Activate your virtual environment and install Flask:

```bash
pip install Flask
```

Or install the dependencies from the requirements file:

```bash
pip install -r requirements.txt
```

---

### Port 5000 is already in use

Another application may already be using port `5000`.

Change the port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then use this base URL:

```text
http://127.0.0.1:5001
```

---

### Connection refused

Make sure Flask is running:

```bash
python app.py
```

Also check that your request uses the correct URL:

```text
http://127.0.0.1:5000/api/courses
```

---

### `courses.json` is not created

The application creates `courses.json` when it starts.

Check that:

- You are running `app.py` from the correct project directory.
- The application has permission to create files.
- The terminal does not show a file permission error.
- The disk is not full.

You can also create the file manually with:

```json
[]
```

---

### Invalid JSON error

JSON requires:

- Double quotes around property names
- Double quotes around text values
- Commas between properties
- No trailing comma after the final property

Correct JSON:

```json
{
  "name": "Python Course",
  "description": "Learn Python.",
  "target_date": "2026-10-15",
  "status": "Not Started"
}
```

Incorrect JSON:

```json
{
  'name': 'Python Course',
  'description': 'Learn Python.',
}
```

---

### Missing `Content-Type` header

When sending JSON with `POST` or `PUT`, include:

```bash
-H "Content-Type: application/json"
```

This tells Flask that the request body contains JSON.

---

### Course not found

First list all courses:

```bash
curl http://127.0.0.1:5000/api/courses
```

Then use an ID from the response:

```bash
curl http://127.0.0.1:5000/api/courses/1
```

---

### Date validation fails

Use the exact format:

```text
YYYY-MM-DD
```

Correct:

```text
2026-10-15
```

Incorrect:

```text
10/15/2026
```

---

### Status validation fails

Use one of these exact values:

```text
Not Started
In Progress
Completed
```

Status values are case-sensitive.

---

## Project Structure

The project uses a simple structure:

```text
codecrafthub/
├── app.py
├── courses.json
├── requirements.txt
└── README.md
```

### `app.py`

Contains the Flask application and API routes.

Responsibilities include:

- Starting the Flask server
- Defining API endpoints
- Validating request data
- Reading data from `courses.json`
- Writing data to `courses.json`
- Returning JSON responses
- Handling errors

### `courses.json`

Stores all course data.

Example:

```json
[
  {
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn REST APIs.",
    "target_date": "2026-10-15",
    "status": "Completed",
    "created_at": "2026-09-20T14:30:00+00:00"
  }
]
```

This file is created automatically if it does not exist.

### `requirements.txt`

Lists the Python packages required by the project.

Example:

```text
Flask
```

Install the listed packages with:

```bash
pip install -r requirements.txt
```

### `README.md`

Contains the project documentation, setup instructions, API information, testing commands, and troubleshooting tips.

---

## Learning REST API Basics

### What is an API?

An API allows programs to communicate with each other.

For CodeCraftHub, a client such as `curl`, Postman, or a web application sends requests to the Flask server. The server processes the requests and returns JSON responses.

---

### What is REST?

REST is a common style for designing web APIs.

CodeCraftHub uses:

- URLs to identify resources
- HTTP methods to describe actions
- JSON to send and receive data
- HTTP status codes to describe results

For example:

```text
GET /api/courses
```

means:

> Get the collection of courses.

This request:

```text
GET /api/courses/1
```

means:

> Get the course with ID 1.

---

### HTTP methods used by CodeCraftHub

#### `POST`

Creates a new course:

```text
POST /api/courses
```

#### `GET`

Reads course data:

```text
GET /api/courses
GET /api/courses/1
```

#### `PUT`

Updates an existing course:

```text
PUT /api/courses/1
```

#### `DELETE`

Removes a course:

```text
DELETE /api/courses/1
```

---

### Why use JSON?

JSON is a simple text format that is easy for both humans and programs to read.

Example:

```json
{
  "name": "Flask API Development",
  "status": "In Progress"
}
```

The CodeCraftHub API receives JSON requests and returns JSON responses.

---

## Limitations of JSON File Storage

Using a JSON file is useful for learning and small applications. However, it has limitations:

- The entire file is read when retrieving data.
- The entire file is rewritten when changing data.
- Multiple simultaneous requests may cause conflicts.
- It is not suitable for large applications.
- It does not provide database transactions.

For a beginner project, JSON storage is simple and effective. A larger application could later migrate to SQLite or another database.
