from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (Public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful """
        payload = {
            'name': 'Deb Prasad Bhattrai',
            'email': 'test.deb@gmail.com',
            'password': 'deb123'
        }

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**result.data)
        self.assertTrue(user.check_password(payload['password']))
        # self.assertNotIn('password', result.data)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {
            'name': 'Deb Prasad Bhattrai',
            'email': 'test.deb@gmail.com',
            'password': 'deb123543'
        }
        create_user(**payload)

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            # 'name': 'NewUser',
            'email': 'test.deb@gmail.com',
            'password': 'pw'
        }

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
