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