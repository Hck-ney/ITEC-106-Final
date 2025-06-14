from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Student, Subject, Enrollment, Grade
from .serializers import StudentSerializer, SubjectSerializer, EnrollmentSerializer, GradeSerializer

# ViewSet for Student model - provides CRUD for students
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    Includes nested enrollments.
    """
    queryset = Student.objects.all().order_by('name') # Order students by name
    serializer_class = StudentSerializer

# ViewSet for Subject model - provides CRUD for subjects
class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subjects to be viewed or edited.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    """
    queryset = Subject.objects.all().order_by('name') # Order subjects by name
    serializer_class = SubjectSerializer

# ViewSet for Enrollment model - provides CRUD for student-subject enrollments
class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows enrollments to be viewed or edited.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    When creating an enrollment, ensure student_id and subject_id exist.
    """
    queryset = Enrollment.objects.all().order_by('student__name') # Order enrollments by student name
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle creating a Grade object along with the Enrollment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # This creates the Enrollment instance

        # After creating enrollment, create a corresponding Grade entry
        enrollment_instance = serializer.instance
        Grade.objects.create(enrollment=enrollment_instance) # Initialize grades with defaults

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# ViewSet for Grade model - provides CRUD for grades
class GradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grades to be viewed or edited.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    Note: Grades are typically tied to an Enrollment.
    """
    queryset = Grade.objects.all().order_by('enrollment__student__name') # Order grades by student name
    serializer_class = GradeSerializer