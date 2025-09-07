import os
import django
import random
from datetime import timedelta, date
from faker import Faker
from django.utils import timezone

# Django-Settings laden
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanmind.settings")
django.setup()

from django.contrib.auth import get_user_model
from kanban_app.models import Board, Task

fake = Faker("de_DE")
User = get_user_model()

def run():
    # --- Benutzer ---
    users = []
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password="Test1234!"
        )
        users.append(user)
    print(f"{len(users)} Benutzer erstellt.")

    # --- Boards ---
    boards = []
    for _ in range(4):
        owner = random.choice(users)
        board = Board.objects.create(
            title=fake.bs().capitalize(),
            owner=owner
        )

        # Owner als Member hinzufügen
        board.members.add(owner)

        # Zufällige weitere Mitglieder
        members = random.sample([u for u in users if u != owner], k=random.randint(1, 3))
        board.members.add(*members)

        boards.append(board)
    print(f"{len(boards)} Boards erstellt.")

    # --- Tasks ---
    STATUS_CHOICES = ["to-do", "in-progress", "review", "done"]
    PRIORITY_CHOICES = ["low", "medium", "high"]

    for board in boards:
        members_list = list(board.members.all())
        for _ in range(random.randint(3, 4)):
            task = Task.objects.create(
                board=board,
                title=fake.sentence(nb_words=4),
                description=fake.sentence(nb_words=10),
                status=random.choice(STATUS_CHOICES),
                priority=random.choice(PRIORITY_CHOICES),
                assignee=random.choice(members_list + [None]),
                reviewer=random.choice(members_list + [None]),
                due_date=date.today() + timedelta(days=random.randint(1, 60))
            )
            print(f"Task '{task.title}' für Board '{board.title}' erstellt.")

    print("Dummy-Daten erfolgreich erstellt.")

if __name__ == "__main__":
    run()
