from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Meal

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    first_name = forms.CharField(
        max_length=50,
        required=True
    )

    last_name = forms.CharField(
        max_length=50,
        required=True
    )

    student_id = forms.CharField(
        max_length=20,
        required=True
    )

    hall = forms.CharField(
        max_length=100,
        required=True
    )

    room_number = forms.CharField(
        max_length=20,
        required=True
    )

    phone = forms.CharField(
        max_length=15,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'student_id',
            'hall',
            'room_number',
            'phone',
            'password1',
            'password2',
        )
        
class MealForm(forms.ModelForm):

    class Meta:
        model = Meal

        fields = (
            'date',
            'meal_type',
            'menu',
            'token_price',
            'available_tokens',
            'is_active',
        )