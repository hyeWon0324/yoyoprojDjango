from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from .models import Users

User = get_user_model()


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.nickname = "some_user"
        new_user = User.objects.create(nickname=self.nickname)

    def test_profile_created(self):
        nickname = self.nickname
        user_profile = Users.objects.filter(user__nickname=self.nickname)
        self.assertTrue(user_profile.exists())
        self.assertTrue(user_profile.count() == 1)

    def test_new_user(self):
        new_user = User.objects.create(nickname=self.nickname + "abcsd")
