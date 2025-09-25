from django.core.management.base import BaseCommand
from accounts.models import User
import re
import sys
import os

# Stronger email regex
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def input_password(prompt="Password: "):
    """Read password with asterisks instead of showing raw input."""
    if os.name == "nt":  # Windows
        import msvcrt
        sys.stdout.write(prompt)
        sys.stdout.flush()
        password = ""
        while True:
            ch = msvcrt.getch()
            if ch in {b"\r", b"\n"}:  # Enter
                print("")
                break
            elif ch == b"\x08":  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                try:
                    password += ch.decode("utf-8")
                    sys.stdout.write("*")
                    sys.stdout.flush()
                except UnicodeDecodeError:
                    continue
        return password
    else:  # Unix/Linux/macOS
        import termios, tty
        sys.stdout.write(prompt)
        sys.stdout.flush()
        password = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):  # Enter
                    print("")
                    break
                elif ch == "\x7f":  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    password += ch
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password


class Command(BaseCommand):
    help = "Create an admin user via the backend (email + password only)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING("=== Create Admin User ==="))

        # --- Email ---
        while True:
            email = input("Enter admin email: ").strip()
            if not email:
                self.stdout.write(self.style.ERROR("Email cannot be empty."))
                continue

            if not EMAIL_REGEX.match(email):
                self.stdout.write(self.style.ERROR("Invalid email format. Please enter a valid email address."))
                continue

            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR("Email already exists. Please try another."))
                continue
            break

        # --- Password ---
        while True:
            password = input_password("Enter password: ")
            password_confirm = input_password("Confirm password: ")

            if not password:
                self.stdout.write(self.style.ERROR("Password cannot be empty."))
                continue

            if password != password_confirm:
                self.stdout.write(self.style.ERROR("Passwords do not match. Try again."))
                continue
            break

        # --- Create Admin ---
        admin_user = User.objects.create_superuser(
            email=email,
            password=password,
            role="admin",
        )

        self.stdout.write(self.style.SUCCESS(f"\nAdmin user created successfully!"))
        self.stdout.write(self.style.HTTP_INFO(f"Email: {email}"))
        self.stdout.write(self.style.HTTP_INFO(f"Password: {'*' * len(password)}"))
        self.stdout.write(self.style.HTTP_INFO("You can now login at /accounts/login/"))
