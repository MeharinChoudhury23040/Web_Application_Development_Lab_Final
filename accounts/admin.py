from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Meal, MealBooking, StudentProfile


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    list_display = (
    'username',
    'first_name',
    'last_name',
    'email',
    'role',
    'is_active',
)
    
    list_filter = (
    'role',
    'is_active',
)
    
    search_fields = (
    'username',
    'first_name',
    'last_name',
    'email',
)

    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role',)
        }),
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'meal_type',
        'menu',
        'token_price',
        'available_tokens',
        'is_active',
    )

    list_filter = (
        'date',
        'meal_type',
        'is_active',
    )

    search_fields = (
        'menu',
    )
    
    ordering = (
    'date',
    'meal_type',
   )


@admin.register(MealBooking)
class MealBookingAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'meal',
        'token_code',
        'status',
        'booking_date',
    )

    list_filter = (
        'status',
        'booking_date',
    )

    search_fields = (
        'student__username',
        'token_code',
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'student_id',
        'hall',
        'room_number',
        'phone',
    )

    search_fields = (
        'student_id',
        'hall',
        'user__username',
    )