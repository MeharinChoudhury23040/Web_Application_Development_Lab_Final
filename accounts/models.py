from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        MANAGER = 'MANAGER', 'Meal Manager'
        ADMIN = 'ADMIN', 'Administrator'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        return self.username


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    hall = models.CharField(
        max_length=100
    )

    room_number = models.CharField(
        max_length=20
    )

    phone = models.CharField(
        max_length=15
    )

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    menu = models.TextField()
    token_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    available_tokens = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'meal_type']
        unique_together = ['date', 'meal_type']

    def __str__(self):
        return f"{self.date} - {self.get_meal_type_display()}"


class MealBooking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('used', 'Used'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meal_bookings'
    )

    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    token_code = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.meal} - {self.token_code}"