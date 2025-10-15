from django.views.generic.list import ListView
from .models import Task

class HomePageView(ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "tasks"