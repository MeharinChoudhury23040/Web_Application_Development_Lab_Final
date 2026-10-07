import os
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Meal


class Command(BaseCommand):
    help = "Create demo meals and an optional meal manager account"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        meals = [
            {
                "date": today,
                "meal_type": "breakfast",
                "menu": "Egg, Paratha, Dal",
                "token_price": 30,
                "available_tokens": 100,
            },
            {
                "date": today,
                "meal_type": "lunch",
                "menu": "Rice, Chicken, Dal",
                "token_price": 40,
                "available_tokens": 100,
            },
            {
                "date": today,
                "meal_type": "dinner",
                "menu": "Rice, Fish, Vegetable",
                "token_price": 40,
                "available_tokens": 100,
            },
            {
                "date": tomorrow,
                "meal_type": "breakfast",
                "menu": "Egg, Paratha, Dal",
                "token_price": 30,
                "available_tokens": 100,
            },
        ]

        for meal_data in meals:
            Meal.objects.update_or_create(
                date=meal_data["date"],
                meal_type=meal_data["meal_type"],
                defaults={
                    "menu": meal_data["menu"],
                    "token_price": meal_data["token_price"],
                    "available_tokens": meal_data["available_tokens"],
                    "is_active": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Demo meals created successfully.")
        )

        manager_username = os.environ.get("DEMO_MANAGER_USERNAME")
        manager_password = os.environ.get("DEMO_MANAGER_PASSWORD")

        if manager_username and manager_password:
            manager, created = User.objects.get_or_create(
                username=manager_username,
                defaults={
                    "role": User.Role.MANAGER,
                    "is_active": True,
                },
            )

            manager.role = User.Role.MANAGER
            manager.is_active = True
            manager.set_password(manager_password)
            manager.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Meal manager '{manager_username}' is ready."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Manager account was not created because "
                    "DEMO_MANAGER_USERNAME or DEMO_MANAGER_PASSWORD "
                    "is not configured."
                )
            )