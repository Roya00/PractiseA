from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "qwe@example.com"
        password = "qwe12321de"
        email1="qwqwqw21@example.com"
        user = get_user_model().objects.create_user(email=email,password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(email,str(user))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "TEde@Example.com"
        password = "qwq12@as"
        user = get_user_model().objects.create_user(email=email,password=password)
        self.assertEqual(user.email,"TEde@example.com")

    def test_new_user_invalid_email(self):
        """Test creating without email"""
        email=""
        password = "qwqwq12121q"
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email, password=password)

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(email="qwqw12@example.com", password="<PASSWORD>")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


