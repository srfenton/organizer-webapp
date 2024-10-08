# Daily Task Manager Web App

This is a Bottle web application that manages daily tasks for users. The app allows users to register, log in, view their daily tasks, mark tasks as complete or incomplete, and generate new tasks for the day. The tasks are stored in an SQLite database.

## Features
- **User Registration**: Allows users to create an account.
- **User Login**: Allows users to log in and view their personalized task list.
- **Task Management**: Users can view daily tasks, mark tasks as complete or incomplete, and add or remove tasks.
- **Timezone Support**: The app supports task assignment based on the user's timezone.

## Requirements

- Python 3.x
- SQLite3
- Required Python packages (listed in `requirements.txt`):
  - Bottle
  - pytz

## Setup

### 1. Install Dependencies
First, install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database
Before running the application, you need to set up the SQLite database (`daily_list.db`) and create the necessary tables.

You can create the database and tables by running the setup script from `setup.py`:

```bash
python -c "from setup import setup_sf, regenerate_tasks_table; regenerate_tasks_table()"
```

Alternatively, you can manually create the database and tables. The required tables are `users`, `list`, and `tasks`:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task TEXT NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    date_assigned TEXT NOT NULL,
    completion_status BOOLEAN NOT NULL DEFAULT false
);
```

### 3. Run the Application

To start the Bottle application, run the following command:

```bash
python bottle_app.py
```

The application will be available at `http://localhost:8080`.

### 4. Accessing the Application
You can access the application in your web browser by navigating to `http://localhost:8080`.

## Usage

### Registration
- Visit `/registration` to create a new account.
- Provide a username and password to register.

### Login
- Visit `/login` to log in with your username and password.
- After login, you will be redirected to your personalized task list.

### Managing Tasks
- You can view your daily tasks at `/list/<user_id>?timezone=<your_timezone>`.
- (the timezone is automatically fetched from the client with JS).
- Tasks can be marked as complete or incomplete.
- You can add, remove, or regenerate tasks as needed.

## Notes

- The database and tables must be created before running the application. If the tables are not present, the application will not function correctly.
- Timezone support ensures that tasks are assigned based on the user's local time.

## License
This project is licensed under the MIT License.
```
