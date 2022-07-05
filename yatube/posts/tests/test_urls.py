from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group, User

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        example = Post.objects.create(
            author=self.user,
            text='Some user\'s authorized text')
        templates_url_names = {
            '/': 'posts/index.html',
            (f'/group/{ self.group.slug }/'): 'posts/group_list.html',
            (f'/profile/{ self.post.author.username }/'):
            'posts/profile.html',
            (f'/posts/{ example.pk }/'): 'posts/post_detail.html',
            (f'/posts/{ example.pk }/edit/'): 'posts/post_create.html',
            '/create/': 'posts/post_create.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

# Проверяем общедоступные страницы

    def test_index_url_exists_at_desired_location(self):
        """Проверка доступности адреса главной страницы."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url_exists_at_desired_location(self):
        """Проверка доступности адреса групп и их постов."""
        response = self.guest_client.get(f'/group/{ self.group.slug }/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_exists_at_desired_location(self):
        """Проверка доступности адреса профиля автора."""
        response = self.guest_client.get(
            f'/profile/{ self.post.author.username }/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_url_exists_at_desired_location(self):
        """Проверка доступности адреса инфо о посте."""
        response = self.guest_client.get(
            f'/posts/{ self.post.pk }/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_guest_url_exists_at_desired_location(self):
        """Проверка доступности адреса редактирования поста (гость)."""
        response = self.guest_client.get(f'/posts/{ self.post.pk }/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_edit_authorized_url_exists_at_desired_location(self):
        """Проверка доступности адреса редактирования поста (посетитель)."""
        response = self.authorized_client.get(f'/posts/{ self.post.pk }/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_edit_author_url_exists_at_desired_location(self):
        """Проверка доступности адреса редактирования поста (автор)."""
        example = Post.objects.create(
            author=self.user,
            text='Some user\'s authorized text')
        response = self.authorized_client.get(f'/posts/{ example.pk }/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_exists_at_desired_location(self):
        """Проверка доступности адреса создания поста и редирект."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/')
        )

    def test_unexisting_url_exists_at_desired_location(self):
        """Проверка доступности адреса несуществующей стр."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
