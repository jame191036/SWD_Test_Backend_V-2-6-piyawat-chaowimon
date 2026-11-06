from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from apis.models import Classroom, School, Student, Teacher


class BaseTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='tester')
        self.client.force_authenticate(user=user)
        # ถ้าไม่ระบุจะได้หน้าเว็บ HTML ซึ่งเปลี่ยน status ของ DELETE จาก 204 เป็น 200
        self.client.credentials(HTTP_ACCEPT='application/json')

        self.school_a = School.objects.create(
            name='Bangkok School', abbreviation='BKK', address='Bangkok'
        )
        self.school_b = School.objects.create(
            name='Chiang Mai School', abbreviation='CNX', address='Chiang Mai'
        )

        self.room_a1 = Classroom.objects.create(school=self.school_a, grade='M.1', room='1')
        self.room_a2 = Classroom.objects.create(school=self.school_a, grade='M.1', room='2')
        self.room_b1 = Classroom.objects.create(school=self.school_b, grade='M.1', room='1')

        # teacher_1 อยู่ 2 ห้องในโรงเรียนเดียวกัน ใช้ทดสอบว่าไม่ถูกนับซ้ำ
        self.teacher_1 = Teacher.objects.create(first_name='Anan', last_name='Dee', gender='male')
        self.teacher_1.classrooms.set([self.room_a1, self.room_a2])
        self.teacher_2 = Teacher.objects.create(first_name='Bua', last_name='Dee', gender='female')
        self.teacher_2.classrooms.set([self.room_a1])
        self.teacher_3 = Teacher.objects.create(first_name='Chai', last_name='Suk', gender='male')
        self.teacher_3.classrooms.set([self.room_b1])

        self.student_1 = Student.objects.create(
            first_name='Dao', last_name='Dee', gender='female', classroom=self.room_a1
        )
        self.student_2 = Student.objects.create(
            first_name='Ek', last_name='Suk', gender='male', classroom=self.room_a1
        )
        self.student_3 = Student.objects.create(
            first_name='Fah', last_name='Dee', gender='female', classroom=self.room_a2
        )
        self.student_4 = Student.objects.create(
            first_name='Gun', last_name='Suk', gender='male', classroom=self.room_b1
        )

    def get_ids(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return sorted(item['id'] for item in response.data)


class AuthenticationTests(BaseTestCase):
    def test_login_is_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/schools/')
        self.assertEqual(response.status_code, 401)


class SchoolTests(BaseTestCase):
    def test_create(self):
        data = {'name': 'New School', 'abbreviation': 'NEW', 'address': 'Phuket'}
        response = self.client.post('/api/v1/schools/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New School')

    def test_list_filter_by_name(self):
        ids = self.get_ids('/api/v1/schools/?name=bangkok')
        self.assertEqual(ids, [self.school_a.id])

    def test_detail_counts(self):
        response = self.client.get(f'/api/v1/schools/{self.school_a.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['classroom_count'], 2)
        # teacher_1 อยู่ 2 ห้องแต่ต้องนับเป็น 1 คน
        self.assertEqual(response.data['teacher_count'], 2)
        self.assertEqual(response.data['student_count'], 3)

    def test_update(self):
        url = f'/api/v1/schools/{self.school_a.id}/'
        response = self.client.patch(url, {'name': 'Renamed'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.school_a.refresh_from_db()
        self.assertEqual(self.school_a.name, 'Renamed')

    def test_full_update(self):
        data = {'name': 'Renamed', 'abbreviation': 'RN', 'address': 'Phuket'}
        response = self.client.put(f'/api/v1/schools/{self.school_a.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.school_a.refresh_from_db()
        self.assertEqual(self.school_a.address, 'Phuket')

    def test_full_update_with_missing_field_is_rejected(self):
        url = f'/api/v1/schools/{self.school_a.id}/'
        response = self.client.put(url, {'name': 'Renamed'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_detail_of_unknown_id_returns_404(self):
        response = self.client.get('/api/v1/schools/9999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_removes_classrooms_but_keeps_people(self):
        response = self.client.delete(f'/api/v1/schools/{self.school_a.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Classroom.objects.filter(school=self.school_a.id).exists())
        self.assertEqual(Teacher.objects.count(), 3)
        self.assertEqual(Student.objects.count(), 4)


class ClassroomTests(BaseTestCase):
    def test_create(self):
        data = {'school': self.school_a.id, 'grade': 'M.2', 'room': '1'}
        response = self.client.post('/api/v1/classrooms/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_duplicate_in_same_school_is_rejected(self):
        data = {'school': self.school_a.id, 'grade': 'M.1', 'room': '1'}
        response = self.client.post('/api/v1/classrooms/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_list_filter_by_school(self):
        ids = self.get_ids(f'/api/v1/classrooms/?school={self.school_a.id}')
        self.assertEqual(ids, [self.room_a1.id, self.room_a2.id])

    def test_detail_lists_teachers_and_students(self):
        response = self.client.get(f'/api/v1/classrooms/{self.room_a1.id}/')
        self.assertEqual(response.status_code, 200)
        teacher_names = sorted(teacher['first_name'] for teacher in response.data['teachers'])
        student_names = sorted(student['first_name'] for student in response.data['students'])
        self.assertEqual(teacher_names, ['Anan', 'Bua'])
        self.assertEqual(student_names, ['Dao', 'Ek'])

    def test_update(self):
        url = f'/api/v1/classrooms/{self.room_a1.id}/'
        response = self.client.patch(url, {'room': '9'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.room_a1.refresh_from_db()
        self.assertEqual(self.room_a1.room, '9')

    def test_full_update(self):
        data = {'school': self.school_b.id, 'grade': 'M.6', 'room': '3'}
        response = self.client.put(f'/api/v1/classrooms/{self.room_a1.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.room_a1.refresh_from_db()
        self.assertEqual(self.room_a1.school, self.school_b)

    def test_update_to_duplicate_room_is_rejected(self):
        # room_a2 ใช้ทับ 2 อยู่แล้ว จึงเปลี่ยน room_a1 เป็นทับ 2 ไม่ได้
        url = f'/api/v1/classrooms/{self.room_a1.id}/'
        response = self.client.patch(url, {'room': '2'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_keeps_students_without_classroom(self):
        response = self.client.delete(f'/api/v1/classrooms/{self.room_a1.id}/')
        self.assertEqual(response.status_code, 204)
        self.student_1.refresh_from_db()
        self.assertIsNone(self.student_1.classroom)


class TeacherTests(BaseTestCase):
    def test_create_with_classrooms(self):
        data = {
            'first_name': 'New',
            'last_name': 'Teacher',
            'gender': 'other',
            'classrooms': [self.room_a1.id, self.room_b1.id],
        }
        response = self.client.post('/api/v1/teachers/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(sorted(response.data['classrooms']), [self.room_a1.id, self.room_b1.id])

    def test_create_with_invalid_gender_is_rejected(self):
        data = {'first_name': 'New', 'last_name': 'Teacher', 'gender': 'unknown'}
        response = self.client.post('/api/v1/teachers/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_filter_by_school_has_no_duplicates(self):
        ids = self.get_ids(f'/api/v1/teachers/?school={self.school_a.id}')
        self.assertEqual(ids, [self.teacher_1.id, self.teacher_2.id])

    def test_filter_by_classroom(self):
        ids = self.get_ids(f'/api/v1/teachers/?classroom={self.room_a2.id}')
        self.assertEqual(ids, [self.teacher_1.id])

    def test_filter_by_name_and_gender(self):
        self.assertEqual(self.get_ids('/api/v1/teachers/?first_name=ana'), [self.teacher_1.id])
        self.assertEqual(
            self.get_ids('/api/v1/teachers/?last_name=dee'),
            [self.teacher_1.id, self.teacher_2.id],
        )
        self.assertEqual(self.get_ids('/api/v1/teachers/?gender=female'), [self.teacher_2.id])

    def test_detail_lists_classrooms(self):
        response = self.client.get(f'/api/v1/teachers/{self.teacher_1.id}/')
        self.assertEqual(response.status_code, 200)
        rooms = sorted(classroom['room'] for classroom in response.data['classrooms'])
        self.assertEqual(rooms, ['1', '2'])

    def test_create_with_unknown_classroom_is_rejected(self):
        data = {
            'first_name': 'New',
            'last_name': 'Teacher',
            'gender': 'male',
            'classrooms': [9999],
        }
        response = self.client.post('/api/v1/teachers/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_filter_can_combine_conditions(self):
        ids = self.get_ids(f'/api/v1/teachers/?school={self.school_a.id}&gender=male')
        self.assertEqual(ids, [self.teacher_1.id])

    def test_list_query_count_stays_the_same(self):
        # 1 query ดึงครู และอีก 1 query ดึงห้องของครูทุกคน ไม่ว่าจะมีครูกี่คน
        with self.assertNumQueries(2):
            self.client.get('/api/v1/teachers/')

    def test_full_update(self):
        data = {
            'first_name': 'Anan',
            'last_name': 'Suk',
            'gender': 'male',
            'classrooms': [self.room_b1.id],
        }
        response = self.client.put(f'/api/v1/teachers/{self.teacher_1.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.teacher_1.classrooms.all()), [self.room_b1])

    def test_update_classrooms(self):
        url = f'/api/v1/teachers/{self.teacher_2.id}/'
        response = self.client.patch(url, {'classrooms': [self.room_b1.id]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.teacher_2.classrooms.all()), [self.room_b1])

    def test_delete(self):
        response = self.client.delete(f'/api/v1/teachers/{self.teacher_1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Teacher.objects.count(), 2)


class StudentTests(BaseTestCase):
    def test_create(self):
        data = {
            'first_name': 'New',
            'last_name': 'Student',
            'gender': 'female',
            'classroom': self.room_a1.id,
        }
        response = self.client.post('/api/v1/students/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['classroom'], self.room_a1.id)

    def test_filter_by_school(self):
        ids = self.get_ids(f'/api/v1/students/?school={self.school_b.id}')
        self.assertEqual(ids, [self.student_4.id])

    def test_filter_by_classroom(self):
        ids = self.get_ids(f'/api/v1/students/?classroom={self.room_a1.id}')
        self.assertEqual(ids, [self.student_1.id, self.student_2.id])

    def test_filter_by_name_and_gender(self):
        self.assertEqual(self.get_ids('/api/v1/students/?first_name=fa'), [self.student_3.id])
        self.assertEqual(
            self.get_ids('/api/v1/students/?last_name=suk'),
            [self.student_2.id, self.student_4.id],
        )
        self.assertEqual(
            self.get_ids('/api/v1/students/?gender=female'),
            [self.student_1.id, self.student_3.id],
        )

    def test_detail_shows_classroom(self):
        response = self.client.get(f'/api/v1/students/{self.student_3.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['classroom']['id'], self.room_a2.id)
        self.assertEqual(response.data['classroom']['room'], '2')

    def test_create_with_unknown_classroom_is_rejected(self):
        data = {'first_name': 'New', 'last_name': 'Student', 'gender': 'male', 'classroom': 9999}
        response = self.client.post('/api/v1/students/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_full_update(self):
        data = {
            'first_name': 'Dao',
            'last_name': 'Suk',
            'gender': 'female',
            'classroom': self.room_b1.id,
        }
        response = self.client.put(f'/api/v1/students/{self.student_1.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.student_1.refresh_from_db()
        self.assertEqual(self.student_1.last_name, 'Suk')

    def test_update_classroom(self):
        url = f'/api/v1/students/{self.student_1.id}/'
        response = self.client.patch(url, {'classroom': self.room_b1.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.student_1.refresh_from_db()
        self.assertEqual(self.student_1.classroom, self.room_b1)

    def test_delete(self):
        response = self.client.delete(f'/api/v1/students/{self.student_1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Student.objects.count(), 3)
