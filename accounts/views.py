import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import StudentRegistrationForm, MealForm
from .models import StudentProfile, Meal, MealBooking

# Create your views here.
def register(request):

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            StudentProfile.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                hall=form.cleaned_data['hall'],
                room_number=form.cleaned_data['room_number'],
                phone=form.cleaned_data['phone'],
            )

            return redirect('login')

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            if user.role == 'MANAGER':
                return redirect('manager_dashboard')

            return redirect('student_dashboard')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


def user_logout(request):

    logout(request)

    return redirect('home')


def student_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role != 'STUDENT':
        return redirect('manager_dashboard')

    meals = Meal.objects.filter(
        is_active=True
    ).order_by('date', 'meal_type')

    my_bookings = MealBooking.objects.filter(
        student=request.user
    ).select_related('meal').order_by('-booking_date')

    booked_meal_ids = my_bookings.filter(
        status='booked'
    ).values_list('meal_id', flat=True)

    return render(
        request,
        'accounts/student_dashboard.html',
        {
            'meals': meals,
            'my_bookings': my_bookings,
            'booked_meal_ids': booked_meal_ids,
        }
    )
    

def manager_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    total_meals = Meal.objects.count()

    booked_tokens = MealBooking.objects.filter(
        status='booked'
    ).count()

    cancelled_tokens = MealBooking.objects.filter(
        status='cancelled'
    ).count()

    used_tokens = MealBooking.objects.filter(
        status='used'
    ).count()

    available_tokens = sum(
        Meal.objects.values_list(
            'available_tokens',
            flat=True
        )
    )

    return render(
        request,
        'accounts/manager_dashboard.html',
        {
            'total_meals': total_meals,
            'booked_tokens': booked_tokens,
            'cancelled_tokens': cancelled_tokens,
            'used_tokens': used_tokens,
            'available_tokens': available_tokens,
        }
    )
    
def manager_bookings(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    bookings = MealBooking.objects.select_related(
        'student',
        'meal'
    ).order_by('-booking_date')

    return render(
        request,
        'accounts/manager_bookings.html',
        {
            'bookings': bookings
        }
    )
    

def token_details(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    bookings = MealBooking.objects.select_related(
        'student',
        'meal'
    ).order_by('-booking_date')

    return render(
        request,
        'accounts/token_details.html',
        {
            'bookings': bookings
        }
    )
    
def manage_meals(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    meals = Meal.objects.all().order_by(
        'date',
        'meal_type'
    )

    return render(
        request,
        'accounts/manage_meals.html',
        {
            'meals': meals
        }
    )
    
    
def edit_meal(request, meal_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':

        form = MealForm(
            request.POST,
            instance=meal
        )

        if form.is_valid():
            form.save()

            return redirect('manage_meals')

    else:

        form = MealForm(
            instance=meal
        )

    return render(
        request,
        'accounts/edit_meal.html',
        {
            'form': form,
            'meal': meal
        }
    )
    
    
def delete_meal(request, meal_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')

    meal = get_object_or_404(Meal, id=meal_id)

    has_bookings = MealBooking.objects.filter(
        meal=meal
    ).exists()

    if request.method == 'POST':

        if has_bookings:
            return redirect('manage_meals')

        meal.delete()

        return redirect('manage_meals')

    return render(
        request,
        'accounts/delete_meal.html',
        {
            'meal': meal,
            'has_bookings': has_bookings,
        }
    )


def use_token(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')
    
    if request.method not in ['GET', 'POST']:
        return redirect('manager_bookings')

    booking = get_object_or_404(
    MealBooking,
    id=booking_id
)

    if request.method == 'POST':

        if booking.status == 'booked':
            booking.status = 'used'
            booking.save()

        return redirect('manager_bookings')

    return render(
        request,
        'accounts/use_token.html',
        {
            'booking': booking
        }
    )


def create_meal(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'MANAGER':
        return redirect('student_dashboard')
    
    if request.method not in ['GET', 'POST']:
        return redirect('manager_dashboard')

    if request.method == 'POST':

        form = MealForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('manager_dashboard')

    else:

        form = MealForm()

    return render(
        request,
        'accounts/create_meal.html',
        {'form': form}
    )
    

def book_meal(request, meal_id):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('student_dashboard')

    meal = get_object_or_404(
    Meal,
    id=meal_id
)

    existing_booking = MealBooking.objects.filter(
        student=request.user,
        meal=meal,
        status='booked'
    ).first()

    if existing_booking:
        return redirect('student_dashboard')

    if meal.available_tokens <= 0:
        return redirect('student_dashboard')

    token_code = f"TOKEN-{uuid.uuid4().hex[:8].upper()}"
    MealBooking.objects.create(
        student=request.user,
        meal=meal,
        token_code=token_code
    )

    meal.available_tokens -= 1
    meal.save()

    return redirect('student_dashboard')


def cancel_booking(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('student_dashboard')

    booking = MealBooking.objects.get(
        id=booking_id,
        student=request.user
    )

    if booking.status == 'booked':

        booking.status = 'cancelled'
        booking.save()

        booking.meal.available_tokens += 1
        booking.meal.save()

    return redirect('student_dashboard')