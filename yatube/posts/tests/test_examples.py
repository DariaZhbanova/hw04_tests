from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, User, Group


User = get_user_model()


class PostWithGroupAndPictureTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.group = Group.objects.create(
            title='Группа АББА',
            slug='test-slug',
            description='Дискрипшн',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст 1234',
            group=cls.group,
            pics='media/m1000x1000.jpg'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def assertPost(self, post, post_b):
        self.assertEqual(post.text, post_b.text)
        self.assertEqual(post.author, post_b.author)
        self.assertEqual(post.pics, post_b.pics)
        self.assertEqual(post.group, post_b.group)

    def test_index_page_show_correct_context(self):
        """При создании поста с картинкой он появляется на главной"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_page_object = response.context['page_obj'][0]
        self.assertPost(first_page_object, self.post)

    def test_group_page_show_correct_context(self):
        """При создании поста с картинкой он появляется на
        странице групп"""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': f'{ self.group.slug }'}))
        first_page_object = response.context['page_obj'][0]
        self.assertPost(first_page_object, self.post)

    def test_profile_page_show_correct_context(self):
        """При создании поста с картинкой группой он появляется в профиле"""
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': f'{ self.user.username }'}))
        first_page_object = response.context['page_obj'][0]
        self.assertPost(first_page_object, self.post)

    def test_post_detail_page_show_correct_context(self):
        """При создании поста с картинкой он появляется
        на индивидуальной странице поста"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        self.assertPost(response.context['post'], self.post)
