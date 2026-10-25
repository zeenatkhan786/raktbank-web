# Rakt Bank

A blood donation and availability management website.
Built with HTML, CSS, Django and SQLite3.

## Features
- Donor registration, edit, delete, search by name/city/phone, filter by blood group
- Blood group management: 8 groups with unit counts and Available / Low / Not available status
- Blood requests: submit, edit, filter, update status (Pending / Approved / Fulfilled / Rejected)
- Marking a request Fulfilled reduces stock automatically (and blocks if stock is too low)
- Responsive layout with a mobile menu
- Django admin panel for full record management

## Setup

```
pip install -r requirements.txt
python manage.py makemigrations bank
python manage.py migrate
python manage.py createsuperuser      # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Project layout

```
raktbank/        project settings and root urls
bank/            app: models, forms, views, urls, admin
templates/       base.html and bank/*.html pages
static/css/      style.css
db.sqlite3       created after migrate
```
