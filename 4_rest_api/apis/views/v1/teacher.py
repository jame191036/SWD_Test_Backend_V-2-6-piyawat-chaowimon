from rest_framework.viewsets import ModelViewSet

from apis.filters import TeacherFilter
from apis.models import Teacher
from apis.serializers import TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(ModelViewSet):
    # ป้องกัน N+1 query ตอนแสดง classrooms ในหน้า list
    queryset = Teacher.objects.prefetch_related('classrooms')
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
