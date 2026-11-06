from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from apis.filters import SchoolFilter
from apis.models import School
from apis.serializers import SchoolDetailSerializer, SchoolSerializer


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            # การนับหลายตารางพร้อมกันทำให้แถวคูณกัน จึงต้องใช้ distinct=True
            queryset = queryset.annotate(
                classroom_count=Count('classrooms', distinct=True),
                teacher_count=Count('classrooms__teachers', distinct=True),
                student_count=Count('classrooms__students', distinct=True),
            )

        return queryset
