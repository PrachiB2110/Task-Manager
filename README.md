
# Face Authentication Todo App

A secure task management application with facial recognition authentication built using Flask, SQLAlchemy, and face_recognition library.

## Features

- User Authentication with Face Recognition
- Secure Password Hashing
- Personal Todo List Management
- CRUD Operations for Tasks
- Session Management
- Responsive Web Interface

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (local) / PostgreSQL (production)
- **Authentication**: face_recognition, Werkzeug Security
- **Computer Vision**: OpenCV (cv2)
- **Frontend**: HTML, CSS (templates)

## Installation

1. Clone the repository:
2. Create a virtual environment and activate it:
   bash
git clone [repository-url]
cd face-auth-todo-app


## API Routes

- `/` - Landing page
- `/signup/` - User registration
- `/signin/` - User login
- `/face/<id>` - Face authentication
- `/home/<user_id>` - User's todo list
- `/update/<id>` - Update task
- `/delete/<id>` - Delete task
- `/logout` - User logout

## Security Features

- Password hashing using Werkzeug Security
- Face recognition authentication
- Session management
- User-specific task isolation

## Dependencies

- Flask
- SQLAlchemy
- face_recognition
- OpenCV
- Werkzeug
- pickle
- datetime
 
