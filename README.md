# DriveNow — your ride, on demand.

DriveNow is a car rental app that makes it quick and easy to find, book, and start driving the right vehicle.

## Table of Contents
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Running the App](#installation--running-the-app)
- [Running Tests](#running-tests)

## Architecture
The application is built using **Python** and follows a modular architecture to separate core logic, data management, and user interaction:
- **`src/`**: Contains the core domain models (e.g., Cars, Users, Reservations) and business logic layer.
- **`main.py`**: The entry point of the application that bootstraps the logic and orchestrates the application flow.
- **Testing**: Test-Driven approach is supported by the `pytest` framework, ensuring high reliability of the core functions. Configurations are stored in `pytest.ini`.

## Prerequisites
- **Python 3.8+** installed on your system.
- **Git** (for cloning the repository).

## Installation & Running the App

It is highly recommended to use a virtual environment to avoid dependency conflicts.

### On Unix / macOS
```bash
# 1. Clone the repository
git clone https://github.com/TisOS/drivenow.git
cd drivenow

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python3 main.py
```

### On Windows
```bat
:: 1. Clone the repository
git clone https://github.com/TisOS/drivenow.git
cd drivenow

:: 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

:: 3. Install dependencies
pip install -r requirements.txt

:: 4. Run the application
python main.py
```

## Running Tests

Automated tests are written using `pytest`. Make sure your virtual environment is activated before running the tests.

### On Unix / macOS
```bash
python3 -m pytest -q
```

### On Windows
```
python -m pytest -q
```