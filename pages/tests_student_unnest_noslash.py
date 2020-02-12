from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pages.models import School, Student
import random

class StudentTests(APITestCase):

    def create_School(self,num,max_student):
        """
        Ensure we can create a new school object.
        """
        ids=[]
        url = '/schools'
        data = {'name': 'Triamudomsuksa', 'max_student': max_student, 'location': 'Bangkok'}
        for i in range(num):
            response = self.client.post(url, data, format='json')
            ids.append(response.data['id'])
        return ids
        
    def test_create_Student(self):
        """
        Ensure we can create a new student object if school is valid
        """
        school_ids = self.create_School(1,20)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().first_name, 'Poompatai')
        self.assertEqual(Student.objects.get().last_name, 'Puntitpong')
        self.assertEqual(Student.objects.get().age, 20)
        self.assertEqual(Student.objects.get().nationality, 'Thailand')
        self.assertEqual(Student.objects.get().school.id, school_ids[0])

        """Invalid School"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': 'aaaa'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_Student_data_type(self):
        """
        Ensure we can create a new student object with datatype that can be convert to matching type.
        """
        school_ids = self.create_School(1,20)
        url = '/students'
        """String age"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': '20', 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().first_name, 'Poompatai')
        self.assertEqual(Student.objects.get().last_name, 'Puntitpong')
        self.assertEqual(Student.objects.get().age, 20)
        self.assertEqual(Student.objects.get().nationality, 'Thailand')
        self.assertEqual(Student.objects.get().school.id, school_ids[0])

        """Name, nationality, type number"""
        data = {'first_name':123, 'last_name': 123,'age': 20, 'nationality': 123, 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """String age but non convertable"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 'AAA', 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_Student_missing_param(self):
        """
        Ensure missing fields are treated
        """
        school_ids = self.create_School(1,20)
        url = '/students'

        """Normal request"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """Missing first_name"""
        data = {'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['first_name'][0].code, 'required')

        """Missing all"""
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['first_name'][0].code, 'required')
        self.assertEqual(response.data['last_name'][0].code, 'required')
        self.assertEqual(response.data['age'][0].code, 'required')
        self.assertEqual(response.data['nationality'][0].code, 'required')
        self.assertEqual(response.data['school'][0].code, 'required')

    def test_create_Student_param_validate(self):
        """
        Ensure out of bound values treated 
        """
        school_ids = self.create_School(1,20)
        url = '/students'

        """Normal request"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """first_name, last_name more than 20 characters and nationality more than 30 character"""
        data = {'first_name': 'A'*21, 'last_name': 'A'*21,'age': 20, 'nationality': 'A'*31, 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['first_name'][0].code, 'max_length')
        self.assertEqual(str(response.data['first_name'][0]), 'Ensure this field has no more than 20 characters.')
        self.assertEqual(response.data['last_name'][0].code, 'max_length')
        self.assertEqual(str(response.data['last_name'][0]), 'Ensure this field has no more than 20 characters.')
        self.assertEqual(response.data['nationality'][0].code, 'max_length')
        self.assertEqual(str(response.data['nationality'][0]), 'Ensure this field has no more than 30 characters.')

        """-1,0,150,151 age"""
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 0, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 150, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': -1, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['age'][0].code, 'min_value')
        self.assertEqual(str(response.data['age'][0]), 'Ensure this value is greater than or equal to 0.')

        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 151, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['age'][0].code, 'max_value')
        self.assertEqual(str(response.data['age'][0]), 'Ensure this value is less than or equal to 150.')

    def test_create_Student_full(self):
        """
        Ensure we can create a new student object if school is valid
        """
        school_ids = self.create_School(1,20)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        for i in range(20):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['school'][0].code, 'invalid')
        self.assertEqual(str(response.data['school'][0]), 'School Triamudomsuksa already has maximum number of students')

    def test_put_Student(self):
        """
        Ensure we can edit Student by PUT REQUEST, and not messing with not found id
        """
        school_ids = self.create_School(2,20)
		
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')

        id = str(Student.objects.get().id)

        url = '/students/' + id
        data = {'first_name': 'Poompatai2', 'last_name': 'Puntitpong2','age': 22, 'nationality': 'Thailand2', 'school': school_ids[1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().first_name, 'Poompatai2')
        self.assertEqual(Student.objects.get().last_name, 'Puntitpong2')
        self.assertEqual(Student.objects.get().age, 22)
        self.assertEqual(Student.objects.get().nationality, 'Thailand2')
        self.assertEqual(Student.objects.get().school.id, school_ids[1])

        """Not found id"""
        url = '/students/aaaa'
        data = {'first_name': 'Poompatai2', 'last_name': 'Puntitpong2','age': 22, 'nationality': 'Thailand2', 'school': school_ids[0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_student_full_school(self):
        """
        Ensure we can update same school for students in full school, but students from other school can't transfer in
        """
        school_ids = self.create_School(2,20)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        id=''
        for i in range(20):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            id=response.data['id']

        """FULL"""
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['school'][0].code, 'invalid')
        self.assertEqual(str(response.data['school'][0]), 'School Triamudomsuksa already has maximum number of students')

        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        url = '/students/'+id
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Other school transfer in"""
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[1]}
        response = self.client.post(url, data, format='json')
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/students/'+id
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_put_Student_missing_param(self):
        """
        Ensure missing fields are treated for PUT REQUEST
        """
        school_ids = self.create_School(2,20)

        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')

        id = str(Student.objects.get().id)

        url = '/students/' + id

        """Normal request"""
        data = {'first_name': 'Poompatai2', 'last_name': 'Puntitpong2','age': 22, 'nationality': 'Thailand2', 'school': school_ids[0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Missing params"""
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['first_name'][0].code, 'required')
        self.assertEqual(response.data['last_name'][0].code, 'required')
        self.assertEqual(response.data['age'][0].code, 'required')
        self.assertEqual(response.data['nationality'][0].code, 'required')
        self.assertEqual(response.data['school'][0].code, 'required')

    def test_patch_Student(self):
        """
        Ensure we can edit Student by PATCH REQUEST(without complete param)
        """
        school_ids = self.create_School(2,20)

        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')

        id = str(Student.objects.get().id)

        url = '/students/' + id
        
        """1-2params at a time"""
        data = {'first_name': 'Poompatai2', 'last_name': 'Puntitpong2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().first_name, 'Poompatai2')
        self.assertEqual(Student.objects.get().last_name, 'Puntitpong2')

        data = {'age': 30, 'nationality': 'Cambodia'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().age, 30)
        self.assertEqual(Student.objects.get().nationality, 'Cambodia')

        data = {'school': school_ids[1]}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().school.id, school_ids[1])

        url = '/students/aaaa'
        data = {'first_name': 'Poompatai2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_student_full_school(self):
        """
        Ensure we can update same school for students in full school, but students from other school can't transfer in
        """
        school_ids = self.create_School(2,20)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        id=''
        for i in range(20):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            id=response.data['id']

        """FULL"""
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['school'][0].code, 'invalid')
        self.assertEqual(str(response.data['school'][0]), 'School Triamudomsuksa already has maximum number of students')

        data = {'school': school_ids[0]}
        url = '/students/'+id
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Other school transfer in"""
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[1]}
        response = self.client.post(url, data, format='json')
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/students/'+id
        data = {'school': school_ids[0]}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_Student(self):
        """
        Ensure we can delete student object and not messed up on not found id
        """
        school_ids = self.create_School(2,20)
        ids=[]
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}

        for i in range(3):
            response = self.client.post(url, data, format='json')
            ids.append(str(response.data['id']))

        self.assertEqual(Student.objects.count(), 3)

        for i in range(3):
            url = '/students/' + ids[i]
            response = self.client.delete(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Student.objects.count(), 2 - i)

        url = '/students/aaaa'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_Student(self):
        """
        Ensure we can get student object and not messing not found id.
        """
        school_ids = self.create_School(2,20)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}

        response = self.client.post(url, data, format='json')
        id = str(response.data['id'])

        url = '/students/' + id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Poompatai')
        self.assertEqual(response.data['last_name'], 'Puntitpong')
        self.assertEqual(response.data['age'], 20)
        self.assertEqual(response.data['nationality'], 'Thailand')
        self.assertEqual(response.data['school'], school_ids[0])

        url = '/students/aaaa'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_Student_bulk(self):
        """
        Ensure we can get student objects.
        """
        school_ids = self.create_School(2,20)
        url = '/students'
        for i in range(10):
            data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
            response = self.client.post(url, data, format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(response.data['results'][0]['first_name'], 'Poompatai')
        self.assertEqual(response.data['results'][0]['last_name'], 'Puntitpong')
        self.assertEqual(response.data['results'][0]['age'], 20)
        self.assertEqual(response.data['results'][0]['nationality'], 'Thailand')
        self.assertEqual(response.data['results'][0]['school'], school_ids[0])

    def test_get_Student_pagination_with_order(self):
        """
        Ensure we can get student objects all with pagination and order.
        """
        school_ids = self.create_School(2,200)
        url = '/students'
        for i in range(104):
            data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': str(random.randint(0,1000))+'Thailand', 'school': school_ids[0]}
            response = self.client.post(url, data, format='json')

        """ascending age"""
        data=[]
        response = self.client.get(url+'?ordering=age', format='json')
        self.assertTrue(len(response.data['results'])<=20)
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20)
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['age']>=data[i-1]['age'])

        """desending age"""
        data=[]
        response = self.client.get(url+'?ordering=-age', format='json')
        self.assertTrue(len(response.data['results'])<=20)
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20)
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['age']<=data[i-1]['age'])

        """ascending nationality"""
        data=[]
        response = self.client.get(url+'?ordering=nationality', format='json')
        self.assertTrue(len(response.data['results'])<=20)
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20)
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['nationality']>=data[i-1]['nationality'])

        """desending nationality"""
        data=[]
        response = self.client.get(url+'?ordering=-nationality', format='json')
        self.assertTrue(len(response.data['results'])<=20)
        data += response.data['results']
        while not (response.data['next'] is None):
            self.assertTrue(len(response.data['results'])<=20)
            response = self.client.get(response.data['next'], format='json')
            data += response.data['results']
        self.assertEqual(len(data), 104)
        for i in range(1,len(data)):
            self.assertTrue(data[i]['nationality']<=data[i-1]['nationality'])


    def test_get_Student_filter(self):
        """
        Ensure we can filter Student by names,age and nationality.
        """
        school_ids = self.create_School(2,200)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        data = {'first_name': 'Robert', 'last_name': 'Puntitpong','age': 25, 'nationality': 'Cambodia', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        data = {'first_name': 'Alan', 'last_name': 'Manny','age': 20, 'nationality': 'Cambodia', 'school': school_ids[1]}
        response = self.client.post(url, data, format='json')

        response = self.client.get(url + '?first_name=Robert', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + '?first_name=Poompatai', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + '?last_name=Puntitpong', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?last_name=Manny', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + '?age=20', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?nationality=Cambodia', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url + '?first_name=Alan&age=20&nationality=Cambodia', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        """Case sensitive"""
        response = self.client.get(url + '?first_name=alan&age=20&nationality=cambodia', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_School_search(self):
        """
        Ensure we can search student by school name or all string field (first_name, last_name, nationality).
        """
        school_ids = self.create_School(2,200)
        url = '/students'
        data = {'first_name': 'Poompatai', 'last_name': 'Puntitpong','age': 20, 'nationality': 'Thailand', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        data = {'first_name': 'Robert', 'last_name': 'Puntitpong','age': 25, 'nationality': 'Cambodia', 'school': school_ids[0]}
        response = self.client.post(url, data, format='json')
        data = {'first_name': 'Alan', 'last_name': 'Manny','age': 20, 'nationality': 'Cambodia', 'school': school_ids[1]}
        response = self.client.post(url, data, format='json')

        """by school"""
        response = self.client.get(url + '?search=triam', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        """by school"""
        response = self.client.get(url + '?search=udom', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        """Nationality"""
        response = self.client.get(url + '?search=odia', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        """last_name"""
        response = self.client.get(url + '?search=titpong', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        """first_name and nationality"""
        response = self.client.get(url + '?search=lan', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
