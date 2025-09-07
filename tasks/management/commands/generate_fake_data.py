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

        for _ in range(options["tasks"]):
            t = Task.objects.create(
                title=fake.sentence(nb_words=5).rstrip("."),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=statuses),
                deadline=timezone.make_aware(fake.date_time_this_month()) if random.choice([True, False]) else None,
                priority=random.choice(priorities) if priorities else None,
                category=random.choice(categories) if categories else None,
            )
            for i in range(random.randint(0, 3)):
                SubTask.objects.create(
                    task=t,
                    title=fake.sentence(nb_words=3).rstrip("."),
                    status=fake.random_element(elements=statuses),
                )
            for j in range(random.randint(0, 3)):
                Note.objects.create(task=t, content=fake.paragraph(nb_sentences=2))

        self.stdout.write(self.style.SUCCESS("Fake data created"))