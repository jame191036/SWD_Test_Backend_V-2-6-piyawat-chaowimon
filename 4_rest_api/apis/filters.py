from django_filters import FilterSet, filters

from apis.models import Classroom, Gender, School, Student, Teacher


class SchoolFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']


class ClassroomFilter(FilterSet):
    school = filters.NumberFilter(field_name='school')

    class Meta:
        model = Classroom
        fields = ['school']


class TeacherFilter(FilterSet):
    # ครู 1 คนอยู่ได้หลายห้อง จึงต้องใช้ distinct ไม่ให้ผลลัพธ์ซ้ำ
    school = filters.NumberFilter(field_name='classrooms__school', distinct=True)
    classroom = filters.NumberFilter(field_name='classrooms', distinct=True)
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.ChoiceFilter(field_name='gender', choices=Gender.choices)

    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']


class StudentFilter(FilterSet):
    school = filters.NumberFilter(field_name='classroom__school')
    classroom = filters.NumberFilter(field_name='classroom')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.ChoiceFilter(field_name='gender', choices=Gender.choices)

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']
