from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from manatal_code_challenge_django.serializers import UserSerializer, SchoolSerializer, StudentSerializer
from django.contrib.auth.models import User
from pages.models import School, Student

# Create your views here.
class DestroyWithPayloadMixing(object):
    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ViewSets define the view behavior.
class UserViewSet(DestroyWithPayloadMixing, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSets define the view behavior.
class SchoolViewSet(DestroyWithPayloadMixing, viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

# ViewSets define the view behavior.
class StudentViewSet(DestroyWithPayloadMixing, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer