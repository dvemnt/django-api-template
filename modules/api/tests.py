# coding=utf-8

import json
import importlib

from django import test
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import Verification

VERSION = 'v1'
CONTENT_TYPE = 'application/json'
CONSTANTS = importlib.import_module('api.{}.constants'.format(VERSION))
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


class CompositeDocstringTestCase(test.TestCase):

    """Test case with composite docstring."""

    @classmethod
    def __new__(cls, *args, **kwargs):
        """Override create class."""
        cls = super(CompositeDocstringTestCase, cls).__new__(*args, **kwargs)
        tests = [attr for attr in dir(cls) if attr.startswith('test_')]
        for test_name in tests:
            test_method = getattr(cls, test_name)
            if cls.__doc__ not in test_method.__doc__:
                test_method.__func__.__doc__ = '{}: {}'.format(
                    cls.__doc__, test_method.__func__.__doc__
                )
        return cls


class APIClient(test.Client):

    """Test API client."""

    def post(self, path, data='',
             content_type=CONTENT_TYPE, secure=False,
             **extra):
        """Constructs an POST request."""
        if data:
            content_type = CONTENT_TYPE
            data = json.dumps(data)
        return super(APIClient, self).post(
            path, data, content_type, secure, **extra
        )

    def put(self, path, data='',
            content_type=CONTENT_TYPE, secure=False,
            **extra):
        """Constructs an PUT request."""
        if data:
            content_type = CONTENT_TYPE
            data = json.dumps(data)
        return super(APIClient, self).put(
            path, data, content_type, secure, **extra
        )

@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class RegistrationTest(CompositeDocstringTestCase):

    """Test registration"""

    url = reverse('api:{}:registration'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        payload = {}

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_email(self):
        """With wrong email."""
        payload = {
            'email': 'wrong email', 'password': 'pass',
            'name': 'Test', 'surname': 'Test'
        }

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_existing_email(self):
        """With existing email."""
        payload = {
            'email': 'test@mail.com', 'password': 'pass',
            'name': 'Test', 'surname': 'Test'
        }
        get_user_model().objects.create_user(
            email=payload['email'], password=payload['password']
        )

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success(self):
        """Success."""
        payload = {
            'email': 'test@email.com', 'password': 'pass',
            'name': 'Test', 'surname': 'Test'
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(Verification.objects.filter(user=user).exists())
        self.assertTrue(user.check_password(payload['password']))


@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class VerificationTest(CompositeDocstringTestCase):

    """Test verification"""

    url = reverse('api:{}:verification'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_code(self):
        """With wrong password."""
        payload = {}
        user = get_user_model().objects.create_user(
            'test@mail.com', password='pass'
        )
        payload['code'] = Verification.objects.create(user=user).code + 'wrong'

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        """Success."""
        payload = {'email': 'test@email.com'}
        user = get_user_model().objects.create_user(
            payload['email'], password='pass'
        )
        payload['code'] = Verification.objects.create(user=user).code

        response = self.client.post(self.url, data=payload)
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.is_active)


@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class ReverificationTest(CompositeDocstringTestCase):

    """Test reverification"""

    url = reverse('api:{}:reverification'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_not_existing_email(self):
        """With not existing email."""
        response = self.client.post(self.url, data={'email': 'test@mail.com'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        """Success."""
        payload = {'email': 'test@email.com'}
        user = get_user_model().objects.create_user(
            payload['email'], password='pass'
        )

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Verification.objects.filter(user=user).exists())


@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class RestorePasswordRequestTest(CompositeDocstringTestCase):

    """Test restore password request"""

    url = reverse('api:{}:password.restore'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_not_existing_email(self):
        """With not existing email."""
        response = self.client.post(self.url, data={'email': 'test@mail.com'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        """Success."""
        payload = {'email': 'test@email.com'}
        user = get_user_model().objects.create_user(
            payload['email'], password='pass'
        )

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Verification.objects.filter(user=user).exists())


@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class RestorePasswordChangeTest(CompositeDocstringTestCase):

    """Test restore password change"""

    url = reverse('api:{}:password.restore.change'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_code(self):
        """With wrong code."""
        payload = {'password': 'pass', 'code': 'wrong'}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        """Success."""
        payload = {'password': 'password'}
        user = get_user_model().objects.create_user(
            email='test@mail.com', password='pass'
        )
        payload['code'] = Verification.objects.create(user=user).code

        response = self.client.post(self.url, data=payload)
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password(payload['password']))


@test.override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class ChangePasswordTest(CompositeDocstringTestCase):

    """Test change password"""

    url = reverse('api:{}:password.change'.format(VERSION))

    def setUp(self):
        """Setup tests."""
        self.user = get_user_model().objects.create_user(
            email='test@email.com', password='pass', is_active=True
        )
        self.token = Token.objects.create(user=self.user).key
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_password(self):
        """With wrong current password."""
        payload = {'current_password': 'wrong', 'password': 'password'}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_success(self):
        """Success."""
        payload = {'current_password': 'pass', 'password': 'password'}

        response = self.client.post(self.url, data=payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))


class AuthenticationTest(CompositeDocstringTestCase):

    """Test authentication"""

    url = reverse('api:{}:authentication'.format(VERSION))
    client = APIClient()

    def test_without_required_data(self):
        """Without required data."""
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_not_existing_email(self):
        """With not existing email."""
        payload = {'email': 'test@email.com', 'password': 'pass'}

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_with_wrong_password(self):
        """With wrong password."""
        payload = {'email': 'test@email.com', 'password': 'pass'}
        get_user_model().objects.create_user(
            payload['email'], password=payload['password']
        )
        payload['password'] = 'wrong'

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_with_inactive_user(self):
        """With inactive user."""
        payload = {'email': 'test@email.com', 'password': 'pass'}
        get_user_model().objects.create_user(
            payload['email'], password=payload['password']
        )

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success(self):
        """Success."""
        payload = {'email': 'test@email.com', 'password': 'pass'}
        get_user_model().objects.create_user(
            payload['email'], password=payload['password'], is_active=True
        )

        response = self.client.post(self.url, data=payload)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', data)


class ProfileTest(CompositeDocstringTestCase):

    """Test profile"""

    url = reverse('api:{}:profile'.format(VERSION))

    def setUp(self):
        """Setup tests."""
        self.user = get_user_model().objects.create_user(
            email='test@email.com', password='pass', is_active=True
        )
        self.token = Token.objects.create(user=self.user).key
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_profile(self):
        """Get profile."""
        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('id', data)
        self.assertIn('email', data)
        self.assertIn('name', data)
        self.assertIn('surname', data)

    def test_update_profile(self):
        """Update profile."""
        payload = {'name': 'name', 'surname': 'surname'}

        response = self.client.put(self.url, data=payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.surname, payload['surname'])
