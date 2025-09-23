from django.core.management.base import BaseCommand
from accounts.models import User
import getpass

class Command(BaseCommand):
    help = 'Create an admin user via the backend'

    def handle(self, *args, **kwargs):
        self.stdout.write("Create Admin User")
        email = input("Enter admin email: ").strip()
        username = input("Enter admin username: ").strip()

        while True:
            password = getpass.getpass("Enter password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            if password == password_confirm:
                break
            else:
                self.stdout.write("Passwords do not match. Try again.")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR("Username already exists!"))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("Email already exists!"))
            return

        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role="admin"
        )

        self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created successfully!"))
        self.stdout.write(f"Email: {email}")
        self.stdout.write("Password: <hidden> (use the one you entered)")
        self.stdout.write("You can now login at /accounts/login/")
