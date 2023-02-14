from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker


faker = Faker()
class TestSetUp(APITestCase):

    def setUp(self):
        from task.models import UserProfile 


        self.login_url = reverse('Login')
        self.user = UserProfile.objects.create_superuser(
            username='AdminTest',
            email='fakemail@admin.com',
            password='AdminMaguitodoTest',
            first_name='Admin',
            last_name='admin'
        ) 

        response = self.client.post(
            self.login_url, 
            {
                'username': 'AdminTest',
                'password': 'AdminMaguitodoTest'
            },
            format='json',
        )
        print(response.data)
        self.token = response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        return super().setUp()

    def test_asdasdasd(self):
        pass 