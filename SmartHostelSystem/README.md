# Smart Hostel Management & Maintenance System

## Run on Windows
1. Extract the ZIP and open the `SmartHostelSystem` folder in VS Code.
2. In terminal:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python manage.py makemigrations maintenance
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
3. Open http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/

## Setup data quickly
- Log in at `/admin/` using your superuser.
- Add Branch entries: Main Campus, North Campus, South Campus, East Campus, West Campus.
- Create a staff user under Users and tick `Staff status` to allow staff dashboard access.
- To create a staff user for a particular branch, create a StaffProfile for that user and select the branch.
- Student accounts can register from `/register/`.
- Staff can sign in through `/login/`; the account must have Staff status enabled.
- Use `/admin/` to assign branches and manage records.

## Important
This is a local college-project starter. It uses SQLite and Django authentication. Before public deployment, replace the development secret key, configure production settings, and review security. The sample staff role uses Django's `is_staff` flag.
