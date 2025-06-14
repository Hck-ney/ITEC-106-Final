from django.contrib import admin
from .models import Student, Subject, Enrollment, Grade

# Register your models here so they appear in the Django admin interface.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'email', 'date_of_birth')
    search_fields = ('name', 'student_id', 'email')
    list_filter = ('date_of_birth',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrollment_date')
    list_filter = ('subject', 'enrollment_date')
    search_fields = ('student__name', 'subject__name')
    raw_id_fields = ('student', 'subject') # Makes it easier to select related objects

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'activity_grade', 'quiz_grade', 'exam_grade', 'total_grade')
    list_filter = ('enrollment__subject',)
    search_fields = ('enrollment__student__name', 'enrollment__subject__name')
    raw_id_fields = ('enrollment',) # Makes it easier to select related objects