from rest_framework import serializers
from .models import Student, Subject, Enrollment, Grade

# Serializer for the Grade model
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'enrollment', 'activity_grade', 'quiz_grade', 'exam_grade', 'total_grade']
        read_only_fields = ['total_grade'] # total_grade is calculated automatically

# Serializer for the Enrollment model
class EnrollmentSerializer(serializers.ModelSerializer):
    # Nested serializer to display subject name and code within enrollment
    subject_details = serializers.SerializerMethodField(read_only=True)
    # Nested serializer for grades related to this enrollment
    grades = GradeSerializer(read_only=True) # Use read_only=True as grades are often created/updated separately

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'subject', 'enrollment_date', 'subject_details', 'grades']

    def get_subject_details(self, obj):
        """
        Returns a dictionary containing details of the enrolled subject.
        """
        return {
            'id': obj.subject.id,
            'name': obj.subject.name,
            'code': obj.subject.code
        }

# Serializer for the Student model
class StudentSerializer(serializers.ModelSerializer):
    # Nested serializer to display subjects enrolled by the student
    # Note: 'source' points to the related_name in the Enrollment model
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'student_id', 'email', 'date_of_birth', 'enrollments']

# Serializer for the Subject model
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']