"""
Unit tests for tag api
"""

from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core.models import  Tag

from recipe.serialzers import TagSerializer

TAG_URL = reverse('recipe:tag-list')

def create_user(email='test12@example.com', password='test@123'):
    return get_user_model().objects.create_user(email, password)

class PublicTagApiTests(TestCase):
    """Test the publicly available"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login"""
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class privateTagsApiTests(TestCase):
    """Test authenticated requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email='royal121@example.com', password='<PASSWORD>')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Food 2')
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0],tag.id)