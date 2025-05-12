# Todo_fastapi
# FastAPI Todo App with JWT Authentication

This is a simple **FastAPI** application that allows users to manage their todos. It includes user authentication with JWT tokens and CRUD operations for todos. The project uses **PostgreSQL** as the database.

## Features

- **User Signup**: Register a new user with a username and password.
- **Login**: JWT-based authentication for secure access to the API.
- **Create Todo**: Create a new todo with a deadline (time to be done).
- **Get All Todos**: Retrieve all todos for the current user.
- **Mark Todo as Completed**: Mark a todo as completed.
- **Update Todo**: Modify an existing todo.
- **Delete Todo**: Delete a specific todo.
- **Group Todos**: Group todos by completed, to be done, and time elapsed.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **PostgreSQL**: Relational database for storing user and todo data.
- **JWT (JSON Web Tokens)**: Secure user authentication.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **Pydantic**: Data validation and settings management.
- **PassLib**: For password hashing.

## Prerequisites

- **Python 3.7+**
- **PostgreSQL**: Ensure you have PostgreSQL installed and running.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fastapi-todo-app.git
cd fastapi-todo-app
