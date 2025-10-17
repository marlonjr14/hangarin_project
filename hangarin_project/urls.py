from django.contrib import admin
from django.urls import path, include
from tasks.views import HomePageView
# Import HomePageView from tasks.views only

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomePageView.as_view(), name="home"),

    # Include all task-related URLs inside tasks/urls.py; remove direct task URL patterns here
    path('tasks/', include('tasks.urls')),
]
