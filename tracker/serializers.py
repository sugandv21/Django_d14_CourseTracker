from rest_framework import serializers
from .models import Course, Instructor

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'email', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    # nested read-only instructor representation
    instructor = InstructorSerializer(read_only=True)
    # writable by id when creating/updating
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), source='instructor', write_only=True
    )
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'instructor_id',
            'lessons_count', 'total_lessons', 'published_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'instructor', 'total_lessons']

    def get_total_lessons(self, obj):
        # For now total_lessons mirrors lessons_count; change if you add Lesson model later
        return obj.lessons_count

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Course title must not be empty.")
        return value
