from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm, CategoryForm, PriorityForm, SubTaskForm, NoteForm

# Add a mixin to provide sidebar context


class SidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()
        # Example: show sample tasks
        context["tasks"] = Task.objects.all()[:5]
        context["notes"] = Note.objects.all()[:5]
        context["subtasks"] = SubTask.objects.all()[:5]
        return context


class HomePageView(SidebarContextMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_count"] = Task.objects.count()
        context["note_count"] = Note.objects.count()
        context["category_count"] = Category.objects.count()
        context["subtask_count"] = SubTask.objects.count()
        context["priority_count"] = Priority.objects.count()
        context["recent_tasks"] = Task.objects.order_by('-id')[:5]
        context["recent_notes"] = Note.objects.order_by('-id')[:5]
        return context


class TaskListView(SidebarContextMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        sort_option = self.request.GET.get("sort")

        if query:
            queryset = queryset.filter(title__icontains=query)

        if sort_option == "title_asc":
            queryset = queryset.order_by("title")
        elif sort_option == "title_desc":
            queryset = queryset.order_by("-title")
        elif sort_option == "created_asc":
            queryset = queryset.order_by("created_at")
        elif sort_option == "created_desc":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-created_at")
        return queryset


class TaskCreateView(SidebarContextMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")


class TaskUpdateView(SidebarContextMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(SidebarContextMixin, DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")


class CategoryListView(SidebarContextMixin, ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category_list.html"
    paginate_by = 10


class CategoryCreateView(SidebarContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryUpdateView(SidebarContextMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryDeleteView(SidebarContextMixin, DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("category-list")


class PriorityListView(SidebarContextMixin, ListView):
    model = Priority
    context_object_name = "priorities"
    template_name = "priority_list.html"
    paginate_by = 10


class PriorityCreateView(SidebarContextMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityUpdateView(SidebarContextMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityDeleteView(SidebarContextMixin, DeleteView):
    model = Priority
    template_name = "priority_confirm_delete.html"
    success_url = reverse_lazy("priority-list")


class SubTaskListView(SidebarContextMixin, ListView):
    model = SubTask
    context_object_name = "subtasks"
    template_name = "subtask_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = SubTask.objects.all()
        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        if q:
            queryset = queryset.filter(title__icontains=q)

        if sort == "title_asc":
            queryset = queryset.order_by("title")
        elif sort == "title_desc":
            queryset = queryset.order_by("-title")
        elif sort == "created_asc":
            queryset = queryset.order_by("created_at")
        elif sort == "created_desc":
            queryset = queryset.order_by("-created_at")

        return queryset



class SubTaskCreateView(SidebarContextMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")


class SubTaskUpdateView(SidebarContextMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")


class SubTaskDeleteView(SidebarContextMixin, DeleteView):
    model = SubTask
    template_name = "subtask_confirm_delete.html"
    success_url = reverse_lazy("subtask-list")


class NoteListView(SidebarContextMixin, ListView):
    model = Note
    context_object_name = "notes"
    template_name = "note_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Note.objects.all()
        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q))

        if sort == "title_asc":
            queryset = queryset.order_by("title")
        elif sort == "title_desc":
            queryset = queryset.order_by("-title")
        elif sort == "created_asc":
            queryset = queryset.order_by("created_at")
        elif sort == "created_desc":
            queryset = queryset.order_by("-created_at")

        return queryset


class NoteCreateView(SidebarContextMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")


class NoteUpdateView(SidebarContextMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")


class NoteDeleteView(SidebarContextMixin, DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("note-list")
