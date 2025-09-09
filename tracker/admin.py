from django.contrib import admin
from .models import Instructor, Course

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','created_at')
    search_fields = ('name','email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','title','instructor','lessons_count','published_date','created_at')
    list_filter = ('instructor','published_date')
    search_fields = ('title','description')
