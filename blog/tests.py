from django.test import TestCase
from .models import Post, Comment, User

# Create your tests here.
class BlogPost(TestCase):

    def setUp(self):
        user = User(email='kilocycl3@gmail')
        user.set_password('Hello123@')
        user.save()

        user = User.objects.get(id=1)
        Post.objects.create(title='My Title', content='Description', author=user)

    def test_this(self):
        p = Post.objects.get(title='My Title')
        self.assertEqual(p.content, 'Description')

