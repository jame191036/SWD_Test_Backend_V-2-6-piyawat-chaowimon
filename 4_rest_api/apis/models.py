from django.db import models


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    # ชั้นปี เช่น ม.1
    grade = models.CharField(max_length=50)
    # ทับ เช่น 2
    room = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'grade', 'room'],
                name='unique_classroom_in_school',
            ),
        ]

    def __str__(self):
        return f'{self.grade}/{self.room}'


# Teacher และ Student ไม่เก็บ School ตรง ๆ เพราะหาได้จากห้องเรียนที่สังกัด
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    classrooms = models.ManyToManyField(Classroom, related_name='teachers', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    # ลบห้องแล้วนักเรียนยังอยู่ โดยค่าห้องจะว่าง
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
