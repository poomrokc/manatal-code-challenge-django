from rest_framework import serializers

from django.contrib.auth.models import User
from pages.models import School, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'max_student')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'school')

    def schoolFullError(self, school):
        raise serializers.ValidationError("School " + school.name + " already has maximum number of students")

    def validate_school(self, data):
        """check if school is full"""
        method = self.context['request'].method
        school = data
        students_count = Student.objects.filter(school=school.id).count()

        """2 cases 1.creating
                   2.update with school switching"""
        if method == 'POST' and students_count >= school.max_student:
            self.schoolFullError(school)

        elif ((method == 'PUT' or method == 'PATCH')
             and school.id != self.instance.school.id
             and students_count >= school.max_student):
            self.schoolFullError(school)

        return data