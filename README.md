# E-Commerce Website – Django

A modular e-commerce website developed using Django. This project provides a complete online shopping experience with user authentication, product management, shopping cart functionality, user dashboards, and an admin panel.

## Features

- User registration and login with email account activation
- Secure password hashing and password recovery via email
- Personalized user dashboard
- Change password and profile picture
- Product browsing and filtering by categories
- Product detail pages with image zoom functionality
- Latest and best-selling products
- Shopping cart management
- Purchase and checkout functionality
- Article and blog section
- Two-level nested comments and replies
- Authentication-based access control for protected pages
- Jalali calendar support
- Django Admin Panel for managing:
  - Users
  - Products
  - Product categories
  - Articles
  - Comments
  - Other website data

- Modular and maintainable project architecture
- Responsive user interface

## Technologies

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

The project follows a modular architecture to keep the code organized, maintainable, and scalable. Different parts of the application are separated into dedicated Django apps based on their functionality.

## Installation

Clone the repository:

```bash
git clone https://github.com/Raha83/eshopProject-.git
```

Navigate to the project directory:

```bash
cd eshopProject-
```

Install the required dependencies:

```bash
pip install -r req.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the project in your browser:

```text
http://127.0.0.1:8000/
```

## Admin Panel

The Django Admin Panel can be used to manage users, products, categories, articles, comments, and other website data.

## Project Status

Completed

## Author

Developed as a Django e-commerce project to practice and demonstrate backend web development, authentication, database management, and modular application architecture.
