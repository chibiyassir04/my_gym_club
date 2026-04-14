from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Member, Trainer

class MemberAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin1234'
        )
        self.staff = User.objects.create_user(
            username='staff1',
            password='staff1234',
            is_staff=False
        )

        self.trainer = Trainer.objects.create(
            name='John',
            specialty='Boxing',
            phone='0612345678'
        )

        self.member = Member.objects.create(
            name='Alice',
            email='alice@gmail.com',
            phone='0611111111',
            membership_type='premium',
            is_active=True,
            trainer=self.trainer
        )

    def get_token(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password
        })
        return response.data['access']

    def test_unauthenticated_access_blocked(self):
        response = self.client.get('/api/members/')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])

    def test_admin_can_get_members(self):
        token = self.get_token('admin', 'admin1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_member(self):
        token = self.get_token('admin', 'admin1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/members/', {
            'name': 'Bob',
            'email': 'bob@gmail.com',
            'phone': '0622222222',
            'membership_type': 'basic',
            'is_active': True,
            'trainer_id': self.trainer.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Bob')

    def test_admin_can_delete_member(self):
        token = self.get_token('admin', 'admin1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/members/{self.member.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_cannot_delete_member(self):
        token = self.get_token('staff1', 'staff1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/members/{self.member.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_member(self):
        token = self.get_token('admin', 'admin1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(f'/api/members/{self.member.id}/deactivate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertFalse(self.member.is_active)