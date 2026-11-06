from rest_framework.viewsets import ModelViewSet

from apis.filters import ClassroomFilter
from apis.models import Classroom
from apis.serializers import ClassroomDetailSerializer, ClassroomSerializer


class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    filterset_class = ClassroomFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClassroomDetailSerializer
        return ClassroomSerializer
