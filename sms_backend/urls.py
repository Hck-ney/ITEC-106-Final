# StudentManagementSystem/sms_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, SubjectViewSet, EnrollmentViewSet, GradeViewSet
# Import TemplateView to serve index.html
from django.views.generic.base import TemplateView
# Import settings and os to get the BASE_DIR
import os
from django.conf import settings

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'grades', GradeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls), # Django admin panel
    path('api/', include(router.urls)), # Our API endpoints
    # Add a URL pattern for the root path to serve index.html
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]