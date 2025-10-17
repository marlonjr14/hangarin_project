# tasks/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Task, SubTask, Note, Priority, Category

class Command(BaseCommand):
    help = "Generate fake tasks, subtasks and notes"

    def add_arguments(self, parser):
        parser.add_argument("--tasks", type=int, default=50)

    def handle(self, *args, **options):
        fake = Faker()
        statuses = [c[0] for c in Task._meta.get_field("status").choices]
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        # Get current timezone-aware datetime for default
        now_aware = timezone.now()

        for _ in range(options["tasks"]):
            # Ensure deadline is never None to satisfy NOT NULL constraint
            deadline = timezone.make_aware(fake.date_time_this_month()) if random.choice([True, False]) else now_aware

            # Provide non-null priority and category or create dummy if none exist
            priority = random.choice(priorities) if priorities else None
            category = random.choice(categories) if categories else None

            # If priority or category is None but FK fields are non-nullable, create dummy or skip
            # This depends on your model definition and constraints
            # If FK fields allow null, this is safe; else adjust accordingly

            t = Task.objects.create(
                title=fake.sentence(nb_words=5).rstrip("."),
                description=fake.paragraph(nb_sentences=3) or "",  # avoid None
                status=fake.random_element(elements=statuses),
                deadline=deadline,
                priority=priority,
                category=category,
            )

            for i in range(random.randint(0, 3)):
                SubTask.objects.create(
                    task=t,
                    title=fake.sentence(nb_words=3).rstrip("."),
                    status=fake.random_element(elements=statuses),
                )

            for j in range(random.randint(0, 3)):
                Note.objects.create(task=t, content=fake.paragraph(nb_sentences=2) or "")

        self.stdout.write(self.style.SUCCESS("Fake data created"))
