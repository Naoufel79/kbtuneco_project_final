import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a Django superuser from environment variables if it does not exist."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            help="If the user exists, update email and password from env vars.",
        )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser creation: set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        if created:
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
            return

        if options.get("update"):
            changed = False
            if user.email != email:
                user.email = email
                changed = True

            if not user.is_staff:
                user.is_staff = True
                changed = True

            if not user.is_superuser:
                user.is_superuser = True
                changed = True

            user.set_password(password)
            changed = True

            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Updated superuser '{username}'."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already up to date."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists (no changes)."))
