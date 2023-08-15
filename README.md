# QA Store 

## Introduction 

A simple online storefront regarding fashion and clothing.

## Tech Stack
- Back-end 
  - Flask
- Front-end
  - HTML, CSS, JS
- Unit/integration testing
  - pytest, flask-testing
- Agile and Project Management - Kanban
  - Jira
- Database integration
  - MySQL, sqlalchemy
- Versioning
  - Git/GitHub
- CI pipeline
  - Jenkins

## Project Structure

```
$PROJECT_ROOT/
│   # application code
├─┬ application/
│ ├── __init__.py
│ │   # static assets - CSS, JS, and images
│ ├── static/
│ │   # HTML templates
│ ├── templates/
│ │   # db models, forms, custom form validators
│ ├── models.py
│ │   # route definitions 
│ └─┬ routes/
│   ├── __init__.py
│   └── routes.py
│   # application tests
├─┬ tests/
│ ├── __init__.py
│ │   # unit/integration tests
│ ├── test_app.py
│   # main application file
├── app.py
│   # dependencies 
├── requirements.txt
│   # script to create mock up db
├── create.py
├── .gitignore
└── README.md
```

## Entity-Relationship Diagram (ERD)

## Risk Assessment

## Current features
- Basic 

## Open issues/bugs
A tracking system will be set up in the future
- [] 

## Future work
- [] Increase modularity
  - i.e., right now, both unit and integration testing are in the same file. 
- [] Improve documentation
- 

## Usage
1. Create a database using MySQL
   ```mysql
      CREATE DATABASE fashionable;
   ```
2. Create a `.env` file in the project root
   ```
      DB_TYPE="..."
      DB_USER="..."
      DB_PASSWORD="..."
      DB_HOST="..."
      DB_NAME="..."
   ```
3. Set up a virtual environment (Windows)
   ```bash
      py -m venv venv
      source venv/Scripts/Activate 
   ```
4. Install required dependencies
   ```bash
      pip install -r requirements.txt
   ```
5. Run `create.py` to create a mock db with products and items
   ```bash
      py create.py
   ```
6. Run `app.py` to start the application
   ```bash
      py app.py
   ```


## References
- Banner image
- Products images
- Bootstrap 
- Axios
- Flask documentation
- 