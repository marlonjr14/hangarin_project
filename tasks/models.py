from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
]

class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

class Task(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, default='')   # Made nullable and default empty string
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending")
    deadline = models.DateTimeField(default=timezone.now)
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)       # Keep nullable if existing nulls

    def __str__(self):
        return self.title

class SubTask(BaseModel):
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending")
    task = models.ForeignKey(
        Task, related_name="subtasks", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Note(BaseModel):
    task = models.ForeignKey(
        Task, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True, default='')       # Nullable with default to avoid issues

    def __str__(self):
        return f"Note for {self.task.title}"
