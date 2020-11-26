# fast-api-sample-project

Welcome to the arc dev challenge solution of Sakander Zirai arc.dev/@SuiOni 👋

Go to https://ideas-projects.herokuapp.com/api/v1 to see Swagger API Documentation for this project 👀

Backend is written in Python3 with the FastAPI Framework 🏎

More details: https://www.codementor.io/@codementorx/draft/ixvyx7tvj?utm_swu=4667

# Change log

- Refactor architecture into python sub packages
- Using SQLAlchemy models
- Using seperate crud logic for easy extensibility
- Using environment variables for enhanced security
- Use real PostgreSQL Database hosted in Heroku
- Host App itself with Heroku => changed api url
- CI/CD: Auto deployment
- Added script for linting and formatting
- DB initialisation scripts
- Using versionised endpoints "api/v1"
- Fixing potential thread unsafe code

# Folder Structure
```
├── Procfile
├── README.md
├── app
│   ├── api
│   │   ├── api_v1
│   │   │   ├── api.py
│   │   │   └── endpoints
│   │   │       ├── auth.py
│   │   │       ├── ideas.py
│   │   │       ├── index.py
│   │   │       └── users.py
│   │   └── deps.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── crud
│   │   ├── crud_idea.py
│   │   └── crud_user.py
│   ├── db
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── initial_data.py
│   ├── main.py
│   ├── models
│   │   ├── idea.py
│   │   └── user.py
│   ├── pre_start.py
│   ├── schemas
│   │   ├── token.py
│   │   └── user.py
│   └── utils.py
├── requirements.txt
└── scripts
    ├── format-imports.sh
    ├── format.sh
    └── lint.sh
```
