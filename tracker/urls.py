from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, instructors_list_create, home

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', home, name='home'),                      
    path('api/', include(router.urls)),                   
    path('api/instructors/', instructors_list_create),   
]
