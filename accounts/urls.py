from django.urls import path

from .views import (
    register,
    user_login,
    user_logout,
    student_dashboard,
    manager_dashboard,
    manager_bookings,
    token_details,
    manage_meals,
    edit_meal,
    delete_meal,
    use_token,
    create_meal,
    book_meal,
    cancel_booking,
)


urlpatterns = [

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'student-dashboard/',
        student_dashboard,
        name='student_dashboard'
    ),

    path(
        'manager-dashboard/',
        manager_dashboard,
        name='manager_dashboard'
    ),
    
    path(
    'manager-bookings/',
    manager_bookings,
    name='manager_bookings'
),
    
    path(
    'token-details/',
    token_details,
    name='token_details'
),
    
    path(
    'manage-meals/',
    manage_meals,
    name='manage_meals'
),
    
    path(
        'create-meal/',
        create_meal,
        name='create_meal'
    ),
    
    path(
        'edit-meal/<int:meal_id>/',
        edit_meal,
        name='edit_meal'
    ),
    
    path(
        'delete-meal/<int:meal_id>/',
        delete_meal,
        name='delete_meal'
    ),
    
    path(
    'use-token/<int:booking_id>/',
    use_token,
    name='use_token'
),

    path(
    'book-meal/<int:meal_id>/',
    book_meal,
    name='book_meal'
),
    
    path(
    'cancel-booking/<int:booking_id>/',
    cancel_booking,
    name='cancel_booking'
),
    

]