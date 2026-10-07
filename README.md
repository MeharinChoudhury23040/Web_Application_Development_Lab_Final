# Web_Application_Development_Lab_Final
# MBSTU Hall Meal Token Management System

A web-based meal token management system designed for hall students and meal managers of Mawlana Bhashani Science and Technology University (MBSTU).

## Project Overview

The system helps students book meal tokens online and allows meal managers to manage meals, monitor bookings, and verify meal tokens.

## Main Features

### Student
- Student registration and login
- View available meals
- Book meal tokens
- Cancel booked tokens
- View personal meal token history
- Receive a unique token code for each booking

### Meal Manager
- Manager dashboard
- Create new meals
- Edit meal information
- Manage available meal tokens
- View student bookings
- Verify/use meal tokens
- Monitor booking statistics

### Administrator
- Django admin panel
- Manage users and roles
- Manage meals
- Manage student profiles
- Manage meal bookings

## User Roles

1. Student
2. Meal Manager
3. Administrator

## Technologies Used

- Python
- Django
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Git & GitHub

## Database

The project uses SQLite during development.

Main database entities:

- User
- StudentProfile
- Meal
- MealBooking

## System Workflow

Student Registration
→ Login
→ View Available Meals
→ Book Meal
→ Generate Token
→ Meal Manager Verifies Token

## Project Structure

```text
MBSTU_Hall_Meal_Token_Management_System/
│
├── accounts/
├── config/
├── core/
├── templates/
├── manage.py
├── .gitignore
└── README.md