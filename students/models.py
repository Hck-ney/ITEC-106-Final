from django.db import models

# Model for Student details
class Student(models.Model):
    """
    Represents a student in the system.
    Stores basic information about each student.
    """
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50, unique=True) # Unique identifier for student
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True) # Optional date of birth

    def __str__(self):
        return f"{self.name} ({self.student_id})"

# Model for Subjects
class Subject(models.Model):
    """
    Represents a subject offered in the system.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True) # Unique code for the subject

    def __str__(self):
        return f"{self.name} ({self.code})"

# Model to link Students to Subjects (Enrollment)
class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific subject.
    This acts as a junction table between Student and Subject.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True) # Date when the enrollment was created

    class Meta:
        unique_together = ('student', 'subject') # A student can only be enrolled in a subject once

    def __str__(self):
        return f"{self.student.name} enrolled in {self.subject.name}"

# Model for Grades
class Grade(models.Model):
    """
    Stores grades for a specific enrollment (student in a subject).
    Includes grades for activities, quizzes, and exams.
    Calculates a total grade.
    """
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grades') # One-to-one with Enrollment
    activity_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    quiz_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    exam_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # You might want to add weights for a more realistic total grade calculation
    # For simplicity, we'll average them here.
    total_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate the total_grade automatically.
        """
        # Basic average calculation. You can implement more complex weighting here.
        self.total_grade = (self.activity_grade + self.quiz_grade + self.exam_grade) / 3
        super().save(*args, **kwargs) # Call the "real" save method

    def __str__(self):
        return f"Grades for {self.enrollment.student.name} in {self.enrollment.subject.name}"