# QA Store 

## Introduction 

A simple online storefront regarding fashion and clothing.

## Project Structure

```
$PROJECT_ROOT/
│   # application code
├─┬ application/
│ ├── init.py
│ │   # static assets - CSS, JS, and images
│ ├── static/
│ │   # HTML templates
│ ├── templates/
│ │   # database models
│ ├── models.py
│ │   # route definitions 
│ └─┬ routes/
│   ├── init.py
│   └── routes.py
│   # application tests
├─┬ tests/
│ │   # unit tests
│ ├─┬ unit/
│ │ ├── test_customers.py
│ │ └── test_items.py
│ |   # integration tests
│ └─┬ integration/
│   └── test_orders.py
│   # main application file
├── app.py
│   # dependencies 
├── requirements.txt
├── .gitignore
└── README.md
```

## Usage
1. Create a database using MySQL
2. Create `.env` file in project_root
   ```
      DB_TYPE="..."
      DB_USER="..."
      DB_PASSWORD="..."
      DB_HOST="..."
      DB_NAME="..."
   ```
3. Install required dependencies
   ```bash
      pip install -r requirements.txt
   ```
4. Run `create.py` to create a mock db with products and items
   ```bash
      py create.py
   ```
5. ...