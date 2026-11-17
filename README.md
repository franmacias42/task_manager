# Task Management Application

**Python Desktop Application — Advanced Programming Techniques**

## 1. Project Overview

Task Management Application is a desktop application developed in Python using PySide6 for the graphical user interface and SQLite for data storage.

The application allows users to create, edit, delete, and organize personal tasks. Each task has a category, priority, and status, making it easier to keep track of pending and completed work.

Tasks are stored in a local SQLite database, so the data is preserved between application sessions. The application also supports exporting tasks to CSV files using a background thread, keeping the graphical interface responsive during the export process.

This project was developed for the **Advanced Programming Techniques** course. Its main goal is to apply advanced Python concepts in a working application, including type annotations, decorators, closures, abstract classes, protocols, concurrency, and automated testing.

## 2. Main Features

The application includes the following features:

- **Add tasks:** create new tasks with a title, description, category, and priority.
- **Edit tasks:** modify the information of existing tasks.
- **Delete tasks:** remove tasks after confirmation.
- **Manage task status:** mark tasks as completed or reopen them.
- **Filter tasks:** filter tasks by status and priority, including both filters at the same time.
- **Persistent storage:** save tasks automatically in a local SQLite database.
- **CSV export:** export all stored tasks to a CSV file compatible with applications such as Microsoft Excel.
- **Background export:** use a separate thread to export tasks without blocking the user interface.

Each task contains an ID, title, description, category, priority, status, and creation date.

The available priorities are **Low, Medium, and High**, while the possible statuses are **Pending and Completed**.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| PySide6 6.12.0 | Desktop graphical interface |
| SQLite | Local database |
| threading | Background CSV export |
| csv | CSV file generation |
| logging | Execution time logging |
| unittest and doctest | Automated testing |
| Ruff | Code style and formatting checks |
| Mypy | Static type checking |

SQLite, threading, csv, logging, unittest, and doctest are part of the Python standard library.

The application was developed and tested on Windows using Python 3.11.

## 4. Installation and Usage

### Requirements

- Python 3.11
- A desktop operating system with a graphical environment compatible with PySide6
- The dependencies listed in `requirements.txt`

### Step 1: Clone the repository

```bash
git clone https://github.com/franmacias42/task_manager.git
cd task_manager
```


### Step 2: Create a virtual environment

On Windows using PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install the dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Run the application

```powershell
python main.py
```

The main application window will open. If the `tasks.db` database does not exist, it will be created automatically.

### Using the Application

The main window provides the following buttons:

- `Add Task`: create a new task.
- `Edit Task`: edit the selected task.
- `Delete Task`: delete the selected task.
- `Complete / Reopen`: change the status of a task.
- `Refresh`: reload the task list.
- `Export to CSV`: export stored tasks to a CSV file.

The status and priority dropdown menus can be used to filter the displayed tasks.

### Demo Tasks (Optional)

The application starts with an empty database when it is executed for the first time.

To make testing easier, the project includes a script called `load_demo_tasks.py`, which generates **24 example tasks**.

These tasks are divided into four categories:

- University
- Projects
- Personal
- Work

They include all three priority levels (Low, Medium, High) and both task statuses (Pending, Completed).

To load the demonstration tasks, run:

```powershell
python load_demo_tasks.py
```

Then start the application:

```powershell
python main.py
```

The example tasks can be used to test filtering, task management, and CSV export without creating tasks manually.

The script also checks existing task titles to avoid inserting duplicate demonstration tasks when executed multiple times.

## 5. Project Structure

The project is organized into separate modules for the graphical interface, data models, repositories, services, and utility functions.

```text
task_manager/
│
├── main.py
├── load_demo_tasks.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── .gitignore
│
├── app/
│   ├── models/
│   │   └── task.py
│   │
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── sqlite_repository.py
│   │   └── task_protocol.py
│   │
│   ├── services/
│   │   ├── export_service.py
│   │   └── export_signals.py
│   │
│   ├── gui/
│   │   ├── main_window.py
│   │   └── task_dialog.py
│   │
│   └── utils/
│       ├── decorators.py
│       └── filters.py
│
├── tests/
│   ├── test_repository.py
│   ├── test_export_service.py
│   ├── test_concurrency.py
│   └── test_repository_pattern.py
│
├── check_protocol.py
└── check_gui_concurrency.py
```

Some auxiliary files and `__init__.py` files are omitted from the structure above.

The main folders have the following responsibilities:

- **models:** defines the `Task` class and its attributes.
- **repositories:** manages database operations and defines abstract interfaces and protocols.
- **services:** handles CSV export and Qt signals.
- **gui:** contains the main window and the task creation/editing dialog.
- **utils:** contains decorators and filtering functions.
- **tests:** contains automated tests for the main components.

The `load_demo_tasks.py` script is provided to populate the database with example tasks.

## 6. Advanced Python Concepts

The project implements the main programming concepts covered in the Advanced Programming Techniques course.

### 6.1. PEP 8 — Code Style

The code follows Python naming and formatting conventions, using descriptive names and a modular structure.

Ruff is used to check code style and formatting.

### 6.2. PEP 484 and PEP 526 — Type Annotations

Type annotations are used throughout the project for function parameters, return values, class attributes, and data structures.

For example, the `Task` dataclass defines its attributes with explicit types:

```python
title: str
priority: TaskPriority = TaskPriority.MEDIUM
id: int | None = None
```

Type annotations are also used in the repository methods, services, and filtering functions.

Mypy is used to check type consistency.

### 6.3. Decorators

The `measure_execution_time` decorator is implemented in `app/utils/decorators.py`.

It measures the execution time of a function using `perf_counter()` and records the result using Python's logging module.

The decorator is applied to the main methods of `SQLiteTaskRepository`, allowing database operation times to be measured without repeating the same code in each method.

### 6.4. Closures

Closures are used to implement task filtering in `app/utils/filters.py`.

The `create_task_filter()` function receives the selected status and priority and returns an inner function that remembers those values.

The returned function is then used to check which tasks match the selected filters.

This filtering logic is used by the graphical interface.

### 6.5. Abstract Base Classes and Protocols

The project uses abstract classes and protocols to define the operations required for task storage.

`TaskRepository` is an abstract base class that defines the CRUD methods using `ABC` and `@abstractmethod`.

`SQLiteTaskRepository` inherits from this class and provides the SQLite implementation.

The project also defines `TaskRepositoryProtocol` using `typing.Protocol`. This allows other classes with compatible methods to be used without explicitly inheriting from the same base class.

These abstractions help separate the storage implementation from the rest of the application.

### 6.6. Concurrency

The CSV export uses `threading.Thread` to run the export operation in a background thread.

When the user starts an export, `MainWindow` creates a worker thread that calls `CSVExportService`.

After the export finishes, a Qt signal communicates the result back to the graphical interface.

This allows the user interface to remain responsive during the export process.

A manual concurrency test is included:

```powershell
python check_gui_concurrency.py
```

This script simulates a slow export and prints the thread identifiers, making it possible to verify that the export runs separately from the main GUI thread.

### 6.7. Doctest and Unittest

Automated tests are included in the `tests/` folder.

The unit tests cover:

- SQLite CRUD operations.
- Task creation, updating, and deletion.
- CSV export and exported data.
- Background export execution and result handling.
- Repository compatibility using an in-memory implementation.

Doctest examples are also included in the filtering module to verify the behavior of `create_task_filter()`.

Temporary directories and databases are used in the tests to avoid modifying the application's main database.

## 7. Repository Design Pattern (Bonus)

The project also implements the **Repository design pattern** to separate data access from the components that use the stored information.

The implementation is based on three main parts:

- **`TaskRepository`:** an abstract class that defines the required CRUD operations.
- **`SQLiteTaskRepository`:** the concrete implementation using SQLite.
- **`TaskRepositoryProtocol`:** a structural interface that allows compatible repository implementations to be used.

For example, `CSVExportService` depends on `TaskRepositoryProtocol` instead of directly depending on SQLite.

This makes it possible to use a different storage implementation without changing the export service, as long as the repository provides the required methods.

The pattern is demonstrated in `tests/test_repository_pattern.py`, which uses an `InMemoryTaskRepository` to test CSV export without a SQLite database.

This approach makes the code easier to test, maintain, and extend.

## 8. Testing and Code Quality

The project has been tested using automated tests, static analysis tools, and manual checks.

### Install Development Dependencies

```powershell
python -m pip install -r requirements-dev.txt
```

### Run Unit Tests

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

**Latest result:** 14 tests passed.

### Run Doctests

```powershell
python -m doctest -v app/utils/filters.py
```

**Latest result:** 6 doctest examples passed.

### Check Code Style with Ruff

```powershell
python -m ruff check app tests main.py load_demo_tasks.py check_protocol.py
```

### Check Formatting with Ruff

```powershell
python -m ruff format --check app tests main.py load_demo_tasks.py check_protocol.py
```

### Check Type Annotations with Mypy

```powershell
python -m mypy app tests main.py check_protocol.py
```

The latest checks completed successfully, with no Ruff linting issues or Mypy errors.

The application was also tested in a separate Python 3.11 virtual environment to verify dependency installation and execution.

A manual concurrency test confirmed that the CSV export runs in a separate thread while the graphical interface remains responsive.
