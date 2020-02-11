from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pages.models import School, Student
import random

class SchoolTests(APITestCase):
    def test_create_School(self):
        """
        Ensure we can create a new school object.
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(School.objects.get().name, 'Triamudomsuksa')
        self.assertEqual(School.objects.get().max_student, 20)
        self.assertEqual(School.objects.get().location, 'Bangkok')

    def test_create_School_string_max_student(self):
        """
        Ensure we can create a new school object with string max_student.
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': '20', 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(School.objects.get().name, 'Triamudomsuksa')
        self.assertEqual(School.objects.get().max_student, 20)
        self.assertEqual(School.objects.get().location, 'Bangkok')

    def test_create_School_missing_param(self):
        """
        Ensure missing fields are treated
        """
        url = '/schools/'

        """Normal request"""
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """Missing name"""
        data = {'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0].code, 'required')

        """Missing max_student"""
        data = {'name': 'Triamudomsuksa', 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['max_student'][0].code, 'required')

        """Missing location"""
        data = {'name': 'Triamudomsuksa', 'max_student': 20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['location'][0].code, 'required')

    def test_create_School_param_validate(self):
        """
        Ensure out of bound values treated 
        """
        url = '/schools/'

        """Normal request"""
        data = {'name': 'A'*20, 'max_student': 20, 'location': 'A'*20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """name more than 20 character"""
        data = {'name': 'A'*21, 'max_student': 20, 'location': 'A'*20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0].code, 'max_length')
        self.assertEqual(str(response.data['name'][0]), 'Ensure this field has no more than 20 characters.')

        """location more than 100 character"""
        data = {'name': 'A'*20, 'max_student': 20, 'location': 'A'*101}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['location'][0].code, 'max_length')
        self.assertEqual(str(response.data['location'][0]), 'Ensure this field has no more than 100 characters.')

        """0 max_student"""
        data = {'name': 'A'*20, 'max_student': 0, 'location': 'A'*100}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['max_student'][0].code, 'min_value')
        self.assertEqual(str(response.data['max_student'][0]), 'Ensure this value is greater than or equal to 1.')

        """negative max_student"""
        for i in range(10):
            data = {'name': 'A'*20, 'max_student': random.randint(-100000,-1), 'location': 'A'*100}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['max_student'][0].code, 'min_value')
            self.assertEqual(str(response.data['max_student'][0]), 'Ensure this value is greater than or equal to 1.')

        """positive max_student"""
        for i in range(10):
            data = {'name': 'A'*20, 'max_student': random.randint(1,100000), 'location': 'A'*100}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_School(self):
        """
        Ensure we can edit School by PUT REQUEST
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')

        id = str(School.objects.get().id)

        url = '/schools/' + id + '/'
        data = {'name': 'Triamudomsuksa2', 'max_student': 30, 'location': 'Bangkok2'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get().name, 'Triamudomsuksa2')
        self.assertEqual(School.objects.get().max_student, 30)
        self.assertEqual(School.objects.get().location, 'Bangkok2')

    def test_put_School_missing_param(self):
        """
        Ensure missing fields are treated for PUT REQUEST
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')

        id = str(School.objects.get().id)

        url = '/schools/' + id + '/'

        """Normal request"""
        data = {'name': 'Triamudomsuksa2', 'max_student': 30, 'location': 'Bangkok2'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Missing params"""
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0].code, 'required')
        self.assertEqual(response.data['max_student'][0].code, 'required')
        self.assertEqual(response.data['location'][0].code, 'required')

    def test_patch_School(self):
        """
        Ensure we can edit School by PATCH REQUEST(without complete param)
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')

        id = str(School.objects.get().id)

        url = '/schools/' + id + '/'
        
        """One param at a time"""
        data = {'name': 'Triamudomsuksa2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get().name, 'Triamudomsuksa2')

        data = {'max_student': 80}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get().max_student, 80)

        data = {'location': 'Bangkok2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get().location, 'Bangkok2')

    def test_delete_School(self):
        """
        Ensure we can delete school object.
        """
        ids=[]
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}

        for i in range(3):
            response = self.client.post(url, data, format='json')
            ids.append(str(response.data['id']))

        self.assertEqual(School.objects.count(), 3)

        for i in range(3):
            url = '/schools/' + ids[i] + '/'
            response = self.client.delete(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(School.objects.count(), 2 - i)

    def test_get_School(self):
        """
        Ensure we can delete school object.
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}

        response = self.client.post(url, data, format='json')
        id = str(response.data['id'])

        url = '/schools/' + id + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Triamudomsuksa')
        self.assertEqual(response.data['max_student'], 20)
        self.assertEqual(response.data['location'], 'Bangkok')

    def test_get_School_bulk(self):
        """
        Ensure we can get school objects.
        """
        url = '/schools/'
        for i in range(10):
            data = {'name': 'Triamudomsuksa', 'max_student': random.randint(1,100), 'location': 'Bangkok'}
            response = self.client.post(url, data, format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(response.data['results'][0]['name'], 'Triamudomsuksa')
        self.assertEqual(response.data['results'][0]['location'], 'Bangkok')

    def test_get_School_pagination_with_order(self):
        """
        Ensure we can get school objects all with pagination and order.
        """
        url = '/schools/'
        for i in range(104):
            data = {'name': 'Triamudomsuksa'+str(i), 'max_student': random.randint(1,100), 'location': 'Bangkok'+str(i)}
            response = self.client.post(url, data, format='json')

        """ascending max_student"""
        data=[]
        response = self.client.get(url+'?ordering=max_student', format='json')
        self.assertTrue(len(response.data['results'])<=20);
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20);
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['max_student']>=data[i-1]['max_student']);

        """desending max_student"""
        data=[]
        response = self.client.get(url+'?ordering=-max_student', format='json')
        self.assertTrue(len(response.data['results'])<=20);
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20);
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['max_student']<=data[i-1]['max_student']);

    def test_get_School_filter(self):
        """
        Ensure we can filter school object by name and max_student.
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa', 'max_student': 10, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        data = {'name': 'Triamudomsuksa2', 'max_student': 10, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')
        data = {'name': 'Triamudomsuksa', 'max_student': 20, 'location': 'Bangkok'}
        response = self.client.post(url, data, format='json')

        response = self.client.get(url + '?max_student=10', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?max_student=20', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + '?name=Triamudomsuksa', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?name=Triamudomsuksa2', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + '?name=Triamudomsuksa&max_student=10', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_School_search(self):
        """
        Ensure we can search school by name or location match.
        """
        url = '/schools/'
        data = {'name': 'Triamudomsuksa dis1', 'max_student': 10, 'location': 'District 1 lampu Bangkok'}
        response = self.client.post(url, data, format='json')
        data = {'name': 'Triamudomsuksa dis2', 'max_student': 10, 'location': 'District 2 lampu'}
        response = self.client.post(url, data, format='json')
        data = {'name': 'Triamudomsuksa dis3', 'max_student': 20, 'location': 'District 3 Bangna'}
        response = self.client.post(url, data, format='json')

        response = self.client.get(url + '?search=bang', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?search=udom', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self.client.get(url + '?search=lampu', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?search=triam', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self.client.get(url + '?search=2', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
