from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


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
            'email': 'test12.deb@gmail.com',
            'password': 'deb123543'
        }
        create_user(**payload)

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'name': 'NewUser',
            'email': 'test.deb@gmail.com',
            'password': 'pw'
        }

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        payload = {
            'email': 'testdeb@mail.com',
            'password': 'passwd123'
        }
        create_user(**payload)

        result = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', result.data)
        self.assertEquals(result.status_code, status.HTTP_200_OK)

    def create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials is given"""
        create_user(email='testdeb@gmail.com', password='test123433')
        payload = {
            'email': 'test.deb@gmail.com',
            'password': 'passwd123'
        }

        result = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', result.data)
        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_no_user(self):
        """Test that token is not created if user doesn't exists"""
        payload = {
            'email': 'test.deb@gmail.com',
            'password': 'passwd123'
        }

        result = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', result.data)
        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""

        result = self.client.post(TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('token', result.data)
        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)
