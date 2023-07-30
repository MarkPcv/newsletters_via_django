# Mailing Service using Django

## Project Description

This project provides ability to create a basic mailing service for sending
newsletters to the list of recipients. The service is developed via Django
Framework. Each newsletter is
scheduled and sent using simple crontab. Web UI is implemented using
Bootstrap 5. Each user can register on website, but the access to functionality
will be provided only after the email verification.

**User** actions:

- Create, update, view and delete newsletter
- Create, update, view and delete client (_recipient_ )

**Manager** actions:

- View and deactivate newsletter
- View and block users

To stop newsletter user or manager has to change its status to _finished_.
Mailing logs are generated and stored automatically in <code>
./logs/logs.txt</code>

### Scheduling

Each letter can be scheduled to be sent daily, weekly, or monthly. The
scheduler runs every minute to track which letters must be sent. The time is
determined during newsletter creation. Modify "CRONJOBS" variable in
<code>settings.py</code> to suit your scheduling needs.

Do not forget to add crontab after either initialisation or modification using
command below:

```bash
python3 manage.py crontab add
```

---

### Administration

The service has admin access which can be enabled by running the command below:

```bash
python3 manage.py csu
```

If different admin credentials are needed, modify the csu.py located as:

```bash
.
└── users
    └── management
        └── commands
            └── csu.py
```

---

## Installation and Run

Activate environment and use the package manager **poetry** to install all
necessary packages:

```bash
poetry shell
poetry install
```

To establish project settings, create <code>.env</code> file in the project
root directory and fill it. Example is illustrated
in <code>.env.sample</code> file.

Create database and make migrations:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Run Django server:

```bash
python3 manage.py runserver
```

---

## Tech Stack

<img src="https://img.shields.io/badge/Django-blue?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/postgresql-blue?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/GIT-blue?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Poetry-blue?style=for-the-badge&logo=poetry&logoColor=white" />
