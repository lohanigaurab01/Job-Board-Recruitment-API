# Job Board Recruitment API

A RESTful backend for a job board and recruitment platform, built with **Django** and **Django REST Framework (DRF)**. It lets companies post jobs, candidates apply, and recruiters schedule and track interviews.

## Features

- **Accounts**: user registration and authentication with role-based access (e.g. candidate, recruiter/company)
- **Company**: company profiles managed by recruiters
- **Jobs**: create, update, list, search and filter job postings
- **Applications**: candidates apply to jobs and track the status of their applications
- **Interviews**: schedule and manage interviews for shortlisted applicants
- RESTful endpoints with a clean, modular app structure

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Framework | Django, Django REST Framework |
| Database | PostgreSQL / MySQL (SQLite for local development) |
| Auth | Token / JWT-based authentication |

## Project Structure

```
Job-Board-Recruitment-API/
├── accounts/        # User model, registration, authentication
├── company/         # Company profiles
├── jobs/            # Job postings
├── applications/    # Job applications and their status
├── interviews/      # Interview scheduling
├── config/          # Project settings, root URLs, WSGI/ASGI
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Git
- (Optional) PostgreSQL or MySQL

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/gaurablohani01/Job-Board-Recruitment-API.git
cd Job-Board-Recruitment-API

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django djangorestframework
# or, if a requirements file exists:
# pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create an admin user (optional)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables

If you use PostgreSQL/MySQL or keep secrets out of source control, create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=jobboard
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## API Overview

> Adjust the paths below to match the routes defined in `config/urls.py`.

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Auth / Accounts | `/api/accounts/` | `POST` register, `POST` login |
| Companies | `/api/companies/` | `GET`, `POST`, `PUT`, `DELETE` |
| Jobs | `/api/jobs/` | `GET`, `POST`, `PUT`, `DELETE` |
| Applications | `/api/applications/` | `GET`, `POST`, `PATCH` |
| Interviews | `/api/interviews/` | `GET`, `POST`, `PUT`, `DELETE` |

### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/jobs/ \
  -H "Authorization: Bearer <your_token>"
```

## Running Tests

```bash
python manage.py test
```



## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## Author

**Gaurab Lohani**
GitHub: [@gaurablohani01](https://github.com/gaurablohani01)

## License

This project is open source. Add a `LICENSE` file (e.g. MIT) to specify the terms.
