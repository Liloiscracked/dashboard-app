# My Dashboard App

## Overview

My Dashboard App is a web application designed to visualize telecommunications coverage and quality KPIs for signal towers. The app allows users to upload CSV files, visualize data, and compare different months.

## Features

- User Authentication (Login, Logout, Registration)
- Responsive Design
- CSV File Upload and Validation
- Coverage and Quality Data Visualization
- KPI Comparison
- Secure Data Handling

## Project Structure

```plaintext
my_dashboard_app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── dashboard/
│       ├── __init__.py
│       ├── routes.py
│       ├── utils.py
│       └── visualizations.py
├── config.py
├── run.py
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_routes.py
    ├── test_models.py
    └── test_dashboard.py
