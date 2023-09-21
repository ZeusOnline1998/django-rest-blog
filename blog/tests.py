from django.test import TestCase
from .models import Post, Comment, User

# Create your tests here.
class BlogPost(TestCase):

    def setUp(self):

        Post.objects.create(title='My Title', content='Description', author=1)

    def test_this(self):
        self.assertEqual(1, 1)
