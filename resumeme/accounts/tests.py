from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .models import UserProfile
import tempfile
from PIL import Image


class ProfileViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

        # Create a profile for the user
        self.profile = UserProfile.objects.get(user=self.user)

        # Set up the client
        self.client = Client()

    def create_test_image(self):
        # Create a temporary image file for testing
        image = Image.new('RGB', (100, 100), color='red')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def test_profile_view(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword123')

        # Access the profile view
        response = self.client.get(reverse('profile_view'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the user's profile is in the context
        self.assertEqual(response.context['profile'], self.profile)

    def test_profile_edit(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword123')

        # Access the profile edit view
        response = self.client.get(reverse('profile_edit'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Test updating the profile
        test_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'bio': 'This is a test bio',
            'location': 'Test City',
            'phone': '123-456-7890',
            'website': 'https://example.com',
            'job_title': 'Test Engineer',
            'company': 'Test Company',
            'email_notifications': True
        }

        response = self.client.post(reverse('profile_edit'), test_data)

        # Check that we're redirected after a successful update
        self.assertEqual(response.status_code, 302)

        # Refresh the profile from the database
        self.profile.refresh_from_db()
        self.user.refresh_from_db()

        # Check that the data was updated
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.profile.bio, 'This is a test bio')
        self.assertEqual(self.profile.location, 'Test City')

    def test_avatar_upload(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword123')

        # Create a test image
        with self.create_test_image() as img:
            # Test uploading an avatar
            response = self.client.post(
                reverse('profile_edit'),
                {
                    'first_name': self.user.first_name,
                    'last_name': self.user.last_name,
                    'email': self.user.email,
                    'avatar': img
                }
            )

        # Check that we're redirected after a successful update
        self.assertEqual(response.status_code, 302)

        # Refresh the profile from the database
        self.profile.refresh_from_db()

        # Check that the avatar was uploaded
        self.assertIsNotNone(self.profile.avatar)

    def test_public_profile_view(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword123')

        # Access the public profile view
        response = self.client.get(reverse('public_profile_view', args=['testuser']))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the user's profile is in the context
        self.assertEqual(response.context['profile'], self.profile)
        self.assertEqual(response.context['profile_user'], self.user)
        self.assertTrue(response.context['is_own_profile'])

