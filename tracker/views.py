from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q

from .models import Course, Instructor
from .serializers import CourseSerializer, InstructorSerializer

# Course API - CBV (ModelViewSet)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        qs = super().get_queryset()
        instructor_id = self.request.query_params.get('instructor_id')
        if instructor_id:
            qs = qs.filter(instructor_id=instructor_id)
        return qs


# Instructor API - FBV (list and create)
@api_view(['GET', 'POST'])
def instructors_list_create(request):
    if request.method == 'GET':
        instructors = Instructor.objects.all().order_by('-created_at')
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)

    # POST
    serializer = InstructorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Homepage - server rendered - lists courses
def home(request):
    q = request.GET.get('q', '').strip()
    if q:
        courses = Course.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).order_by('-created_at')
    else:
        courses = Course.objects.all().order_by('-created_at')
    return render(request, "tracker/home.html", {"courses": courses, "q": q})
