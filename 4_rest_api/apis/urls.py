from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views.v1.classroom import ClassroomViewSet
from apis.views.v1.school import SchoolViewSet
from apis.views.v1.student import StudentViewSet
from apis.views.v1.teacher import TeacherViewSet


router = DefaultRouter()
router.register('schools', SchoolViewSet)
router.register('classrooms', ClassroomViewSet)
router.register('teachers', TeacherViewSet)
router.register('students', StudentViewSet)

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
