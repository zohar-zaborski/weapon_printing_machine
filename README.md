# Weapon Printing App
## Backend
### Zohar Zaborski
This project is a backend service for managing weapon customizations and printing jobs. It provides endpoints for users to authenticate, customize weapons with compatible parts, manage customizations, and send them to print.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API](#api)
- [Tests](#tests)
- [Further Elaboration](#further-improvements)
- [Output](#output)


## Features
The backend is built using FastAPI, a modern and high-performance web framework for creating APIs, leveraging SQLAlchemy as the ORM for database interactions and SQLite for lightweight, file-based data storage. Authentication is handled with OAuth2 and JWT (JSON Web Tokens) for secure token-based authentication, while bcrypt ensures secure password hashing and verification. This combination provides a robust, secure, and efficient architecture for managing application data and user authentication. 
1. **User Authentication**:
    - Secure login and registration.
    - Token-based authentication using JWT.
2. **Weapon Management**:
    - View available weapons and their compatible parts detailed.
3. **Customization Management:**:
    - Create, retrieve, update, and delete weapon customizations.
4. **Print Job Management:**:
    - Submit customizations for printing.
    - View the status of print jobs.
4. **Validation and Security:**:
    - Passwords are securely hashed.
    - Token validation for protected routes.

## Project Structure
The main components are organized as follows:


## Setup Instructions
 - Python env version that was used: `3.12.1`
1. Clone the repository(if you downloaded via zip file, skip this part):
    https://github.com/zohar-zaborski/weapon_printing_machine.git
    cd weapon_printing_machine
2. Create and activate virutal environment:
    ```bash
    # On Windows
    python -m venv env
    .\env\Scripts\activate
    # On macOS/Linux
    python3 -m venv myenv
    source env/bin/activate
    ```
2. Define Python Path(if needed):
    ```bash
    # On Windows
    $env:PYTHONPATH = "C:\path\to\your\project;$env:PYTHONPATH"
    # On macOS/Linux
    export PYTHONPATH="/path/to/your/project:$PYTHONPATH"
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Installing test dependencies:
    ```bash
    pip install -r requirements-dev.txt
    ```
    

## Usage
In the main folder, run the fastapi app:
```bash 
uvicorn app.main:app --reload
```
## API endpoints in the server:
### Authentication
`POST /auth/register` - Register a new user.
`POST /auth/token` - Authenticate a user, generate a token and login.
### Weapons
`GET /weapons/` - Retrieve a list of all weapons.
`GET /weapons/{weapons_id}` - Get Weapon.
`GET weapons/parts` - Retrieve a list of all available parts.
`GET weapons/parts/{part_id}` Get Part
### Customizations
` GET /customize` - Retrieve a list of all customizations.
`POST /customize` - Customize a weapon and send it to print jobs.
`GET /customize/{customization_id}` - Get customization.
`PUT /customize/{customization_id}` - Update customization.
`DELETE /customize/{customization_id}` - Delete Customization.
### Print jobs
`POST /print-jobs/print` - Send to print.
`GET /print-jobs/print` - Retrieve a list of all print jobs.
`GET /print-jobs/{job_id}` - Get a print job.
`PUT /print-jobs/{job_id}` - Update print job status.

## Tests
Tests in the backend app:



## Further Elaboration
- Possible Features Implementations:
    `Advanced Exceptions`: Currently, the project utilizes a simple Exceptions configuration. Future enhancements could include a more advanced and customized exceptions.
    `Adding Logging`:Managing backend with comprehensive logging can be very useful for tracking data and issues that may rise.
    `Database Integration`: The project now relies on an in-memory repository for simplicity, but future versions could incorporate a database like PostgreSQL or MongoDB. This would support persistence, scalability, and more complex query capabilities for large policy and rule datasets. 
    `More Fields`: Generating more "Real world" fields, like Unique ID of the weapon, a serial number. More fields:
                    Color, Magazine Size, etc.

## Output
- POST /Customize -send a weapon with parts to saved customized weapons list:
    ```bash
    {
  "weapon_id": 0,
  "parts": [
    0
  ]
    }
    ```
    Response:
    ```bash
    {
  "id": 0,
  "weapon_id": 0,
  "parts": [
    0
  ],
  "print_job_id": 0
    }
    ```
- Get all customizations:
    ```bash
    [
      {
        "id": 1,
        "weapon_id": 1,
        "parts": [
          4,
          1
        ],
        "print_job_id": 1
      },
      {
        "id": 2,
        "weapon_id": 2,
        "parts": [
          2,
          3
        ],
        "print_job_id": 5
      }
    ]
    ```

- Get all Weapons:
    ```bash
    [
      {
        "id": 1,
        "name": "Glock 17",
        "compatible_parts": [
          "1",
          "4",
          "7",
          "10"
        ]
      },
      {
        "id": 2,
        "name": "M4",
        "compatible_parts": [
          "2",
          "3",
          "5",
          "8",
          "11"
        ]
      },
      {
        "id": 3,
        "name": "FN Minimi",
        "compatible_parts": [
          "3",
          "6",
          "9",
          "12"
        ]
      }
    ]
    ```
- Get all parts:
    ```bash
    [
  {
    "id": 1,
    "type": "Sight",
    "name": "Mepro - MPO PRO",
    "compatible_weapons": [
      "Glock 17"
    ]
  },
  {
    "id": 2,
    "type": "Sight",
    "name": "Mepro - Hunter 4x",
    "compatible_weapons": [
      "M4"
    ]
  },
  {
    "id": 3,
    "type": "Sight",
    "name": "Mepro - MMX 3",
    "compatible_weapons": [
      "M4",
      "FN Minimi"
    ]
  },
  {
    "id": 4,
    "type": "Laser Pointer",
    "name": "Nightstick - TSM11G",
    "compatible_weapons": [
      "Glock 17"
    ]
  },...
  ]
    ```
- POST print-jobs/print - Print response:
    ```bash
    {
  "id": 0,
  "customized_weapon_id": 0,
  "status": "Pending",
  "created_at": "2024-11-18T12:48:42.371Z"
    }
    ```





