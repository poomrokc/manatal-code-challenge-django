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
class SchoolViewSet(DestroyWithPayloadMixing, viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

# ViewSets define the view behavior.
class StudentViewSet(DestroyWithPayloadMixing, viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    def get_queryset(self):
        if 'school_pk' in self.kwargs:
            return Student.objects.filter(school_id=self.kwargs['school_pk'])
        else:
            return Student.objects.all()

    def create(self, request, *args, **kwargs):
        """If is called inside school, we use data from the url(ignore passed data) else just use from the passed data"""
        if 'school_pk' in self.kwargs:
            request.data['school'] = self.kwargs['school_pk']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
