# EGASP Database

**Enhanced Gonococcal Antimicrobial Surveillance Program (EGASP) Database**

A Django-based data management system for encoding, managing, validating, reporting, and exporting EGASP surveillance data.

> Repository: `https://github.com/squarfie/EGASP_Data_v2.10.21.2026`

---

## Overview

The EGASP Database supports the management of surveillance records collected under the Enhanced Gonococcal Antimicrobial Surveillance Program.

The system provides tools for:

- EGASP case and CRF data management
- Antibiotic susceptibility data management
- Breakpoint and reference-table configuration
- Clinic, specimen, city, and staff reference data
- User authentication and role-based access
- Data upload and download
- Monthly EGASP reporting
- ARS Data, Summary, and MIC Summary Excel generation
- Dashboard summaries and record counts
- Administrative account management
- Password recovery/reset
- Optional Google sign-in integration

The application is built with **Python**, **Django**, and **PostgreSQL**, with support for deployment using Gunicorn/Nginx or another compatible WSGI hosting environment.

---

## Technology Stack

### Backend

- Python
- Django
- PostgreSQL
- SQLAlchemy
- pandas
- openpyxl
- psycopg2
- python-decouple

### Frontend

- HTML5
- CSS
- JavaScript
- Bootstrap / Argon Dashboard components
- AJAX where applicable

### Production / Deployment

- Gunicorn
- Nginx
- Docker / Docker Compose
- WhiteNoise for static-file support where configured

---

## Main Features

### Dashboard

The dashboard provides a quick overview of EGASP records, including:

- Total number of records
- Clinic counts
- Gender counts
- Age-group counts
- Recent records
- Search
- Pagination
- Direct access to encoding and utility functions

### CRF / EGASP Data Management

Authorized users can:

- Create EGASP records
- View records
- Edit existing records
- Search records
- Review encoded data
- Manage associated susceptibility information

### Antibiotic Susceptibility Data

The system supports antibiotic susceptibility data including:

- Disk diffusion values
- MIC values
- RIS interpretations
- Antibiotic reference codes
- Breakpoint configuration
- Antibiotic uploads

Reference tables can be maintained through the system utilities.

### Reference / Utility Data

Administrative utilities include management of:

- Antibiotics
- Breakpoints
- Clinic codes
- Specimen codes
- Cities / barangays
- ARSP laboratory staff
- Clinic staff
- Other configurable reference data used by the application

### User and Account Management

The application includes:

- Username/password authentication
- Account registration
- Password recovery/reset
- Administrative account management
- Role-based access controls
- Optional Google authentication when configured

Role permissions should be reviewed before production deployment so users only receive the access required for their work.

### Monthly Reports

The Monthly EGASP Report feature can generate an Excel workbook containing:

1. **ARS Data**
2. **Summary**
3. **MIC Summary**

The report can be generated from database records or from an uploaded Excel list containing an `ARS Data` worksheet.

Current reporting logic includes clinic summaries for:

- TLY
- PSH
- TSH

The summary workbook can include patient/sample totals, culture/Gram-stain summaries, antibiotic usage summaries, age groups, partner-history categories, and MIC summaries for supported antibiotics.

---

## Repository Structure

A simplified project structure is shown below:

```text
EGASP_DATA/
├── apps/
│   ├── authentication/
│   ├── home/
│   ├── static/
│   └── templates/
├── core/
├── media/
├── nginx/
├── staticfiles/
├── uploads/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── gunicorn-cfg.py
├── Procfile
├── runtime.txt
├── CHANGELOG.md
└── README.md
```

The exact structure may change as the project is updated.

---

# Local Development Setup

## 1. Clone the Repository

```bash
git clone https://github.com/squarfie/EGASP_Data_v2.10.21.2026.git
cd EGASP_Data_v2.10.21.2026
```

If the Django project is inside a nested project directory, enter that directory before running `manage.py`.

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv egasp
egasp\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv egasp
source egasp/bin/activate
```

After activation, the terminal should show the virtual environment name.

---

## 3. Install Dependencies

Install the project dependencies from `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Do not manually install individual packages unless a dependency is missing from `requirements.txt`.

If you add a new production dependency, update the dependency file accordingly.

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=replace-with-a-secure-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=egasp_db
DB_USER=postgres
DB_PASSWORD=replace-with-database-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Depending on the current `settings.py`, the exact variable names may differ. Match the names expected by the project configuration.

## Optional Email Configuration

Password-reset functions may require email configuration:

```env
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=example@example.com
EMAIL_HOST_PASSWORD=replace-with-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=example@example.com
```

## Optional Google Authentication

If Google authentication is enabled:

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_SECRET=your-google-client-secret
```

Never commit OAuth client secrets to Git.

---

# Database Setup

## PostgreSQL

Create a PostgreSQL database and user appropriate for your environment.

Example database:

```text
egasp_db
```

Update the `.env` file with the correct credentials.

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

Normally, committed migrations should already exist. `makemigrations` is only required when model definitions have changed.

---

## Create an Administrator Account

Create the initial Django superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

---

# Initial Reference Data

For a fresh installation, configure the reference tables required by the application.

Depending on the current version, these may include:

- Antibiotics
- Breakpoints
- Clinic codes
- Specimen codes
- Cities / barangays
- ARSP laboratory staff
- Clinic staff

Where upload utilities are available, use the supplied Excel templates to populate large reference tables.

Examples included in the project may include:

```text
Breakpoints_egasp.xlsx
AntibioticEntry_egasp.xlsx
```

Always review uploaded reference files before applying them to a production database.

---

# Run the Development Server

Start Django locally:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

For LAN testing:

```bash
python manage.py runserver 0.0.0.0:8090
```

Then access the server using the host computer's local IP address.

Example:

```text
http://192.168.1.100:8090/
```

Use Django's development server only for development/testing.

---

# Static Files

For production deployment, collect static files:

```bash
python manage.py collectstatic --noinput
```

Verify that `STATIC_ROOT`, `STATIC_URL`, and any Nginx/hosting static aliases match the deployment environment.

Uploaded files should be stored under the configured media directory and served according to the production web-server configuration.

---

# Production Deployment

The project can be deployed using a standard Django WSGI stack.

A typical deployment is:

```text
Client
   ↓
Nginx
   ↓
Gunicorn
   ↓
Django
   ↓
PostgreSQL
```

Recommended production settings include:

```env
DEBUG=False
```

and properly configured:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- HTTPS
- secure cookies
- database credentials
- static/media paths
- email settings
- OAuth settings, if enabled

Restart the application service after deploying Python/Django code changes.

Reload Nginx only when its configuration has changed.

Before reloading Nginx:

```bash
sudo nginx -t
```

If the configuration test succeeds:

```bash
sudo systemctl reload nginx
```

---

# Docker

The repository includes Docker-related files for containerized deployment.

Build the images:

```bash
docker-compose build
```

Start the services:

```bash
docker-compose up -d
```

Run migrations:

```bash
docker-compose exec web python manage.py migrate
```

Collect static files:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

View logs:

```bash
docker-compose logs -f
```

Stop the containers:

```bash
docker-compose down
```

Restart:

```bash
docker-compose restart
```

Docker configuration should be reviewed before production use to ensure credentials, volumes, networking, and persistent database storage are correctly configured.

---

# Monthly Report Workflow

The monthly reporting module supports generation of an `.xlsx` report.

## Generate from Database Records

The application can build a workbook from EGASP database records.

Generated sheets include:

```text
ARS Data
Summary
MIC Summary
```

## Generate from an Existing Excel List

An uploaded workbook should contain an `ARS Data` sheet or a compatible active worksheet.

At minimum, the uploaded list must contain the columns required by the reporting function, including:

```text
egasp_id
clinic
```

The report builder derives summary values from the uploaded records and generates the report workbook.

---

# Antibiotic Entry Relationships

Antibiotic records should remain properly linked to their corresponding EGASP record through the configured foreign-key relationship.

If legacy imported records are missing this relationship, inspect the affected records before attempting repairs.

A diagnostic query can be run from the Django shell:

```bash
python manage.py shell
```

Example:

```python
from apps.home.models import AntibioticEntry

AntibioticEntry.objects.filter(
    ab_idNumber_egasp__isnull=True
).count()
```

Do not automatically relink production records without first confirming that the identifier used for matching is unique and correct.

---

# Testing

Run the Django test suite:

```bash
python manage.py test
```

Tests should be run after changes to:

- Authentication
- Permissions
- Upload workflows
- Reporting
- Data validation
- Reference tables
- Export functions

For deployment, run tests before restarting the production application.

---

# Security

## Never Commit Secrets

The following must not be committed to a public repository:

```text
.env
database passwords
SECRET_KEY
OAuth client secrets
email passwords
private keys
production database dumps
patient-level data exports
```

Ensure `.gitignore` covers sensitive and generated files.

Example:

```gitignore
.env
.env.*
*.sqlite3
*.sql
*.dump
*.backup
__pycache__/
*.pyc
venv/
.venv/
media/
```

If a credential is accidentally committed or shared, rotate it immediately.

## Production Recommendations

- Keep Django and dependencies patched.
- Keep the operating system, PostgreSQL, Nginx, and Gunicorn updated.
- Use HTTPS.
- Disable `DEBUG`.
- Restrict administrator accounts.
- Apply least-privilege permissions.
- Validate uploaded files.
- Maintain database and media backups.
- Review server/application logs.
- Do not expose database ports publicly unless explicitly required and secured.

---

# Browser Support

Use a current version of a modern browser.

Recommended:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Brave
- Other Chromium-based browsers

If an AJAX or JavaScript function behaves unexpectedly:

1. Refresh without cached assets.
2. Check the browser developer console.
3. Inspect the Network tab for 403, 404, or 500 responses.
4. Confirm JavaScript is enabled.
5. Check CSRF/CORS and mixed-content errors.
6. Test without browser extensions.

---

# Troubleshooting

## PostgreSQL Connection Error

Check:

- PostgreSQL is running.
- `.env` credentials are correct.
- Database name and port are correct.
- The database user has access to the database.

Typical PostgreSQL port:

```text
5432
```

---

## Static Files Not Loading

Run:

```bash
python manage.py collectstatic --noinput
```

Then verify the web-server static-file configuration.

---

## Gunicorn / Application Service Fails to Start

Check the application logs.

For a systemd-based deployment:

```bash
sudo systemctl status <service-name> --no-pager
sudo journalctl -u <service-name> -n 100 --no-pager
```

To follow logs:

```bash
sudo journalctl -u <service-name> -f
```

---

## Excel Report Opens With a Repair Warning

If Microsoft Excel reports:

```text
We found a problem with some content...
```

inspect the generated workbook structure, especially Excel Table definitions and worksheets with headers but no data rows.

Do not create an Excel Table over a header-only range. Only add a table when the sheet contains at least one data row.

---

# Backups

Production deployments should maintain regular backups of:

1. PostgreSQL database
2. Uploaded/media files
3. `.env` configuration stored securely
4. Deployment configuration
5. Application source code through Git

Periodically test database restoration procedures.

---

# Updating the Project

Before updating:

```bash
git status
```

Commit or safely preserve any local changes.

Pull updates:

```bash
git pull
```

Install new dependencies if `requirements.txt` changed:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic --noinput
```

Then restart the application service.

---

# Development Notes

When adding new features:

1. Create or update tests.
2. Run the test suite.
3. Review migrations.
4. Verify role permissions.
5. Check upload/export behavior.
6. Confirm no sensitive data is staged in Git.
7. Update `CHANGELOG.md` and this README when behavior changes.

---

# Versioning

The project currently uses date-oriented version identifiers for major working builds.

Example:

```text
v2.10.22.26
```

Keep `CHANGELOG.md` updated whenever a version is released or deployed.

---

# License and Third-Party Components

This project may include third-party frontend libraries, templates, icons, and Python packages.

Retain all copyright, attribution, and license notices required by those components.

The original frontend includes Creative Tim / Argon Dashboard components; review their applicable license terms before redistribution or modification.

---

# Project Status

The EGASP Database is under active development and maintenance.

Current development areas include:

- Data validation
- User and permission management
- Reporting
- Excel import/export
- Reference-data maintenance
- UI improvements
- Production deployment and security hardening

---

## Repository

```text
https://github.com/squarfie/EGASP_Data_v2.10.21.2026
```

---

## Maintainer Notes

When deploying or handing the system to another administrator, document:

- Production domain
- Deployment directory
- Application service name
- Database name
- Backup location
- Static/media locations
- Required environment-variable names
- Email configuration
- OAuth configuration
- Administrative account ownership

Do not store passwords or secrets in this README.
