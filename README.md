# User Validation Web App (Flask + SQLite)

## Run
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Sample users
| Login name | Password |
|------------|----------|
| admin      | admin123 |
| ayush      | pass@123 |

## Flow
1. User submits login name & password (POST).
2. Server looks the user up in the database.
3. Password hash matches -> success page. Otherwise -> error message on login page.
