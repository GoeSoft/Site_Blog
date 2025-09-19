from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Создаем тестовый пост
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Тестовое содержание',
        )

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_page_status_code(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_status_code(self):
        response = self.client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {
            'title': 'Новый пост',
            'content': 'Содержание нового поста'
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertEqual(Post.objects.count(), 2)   # был 1, стало 2

    def test_post_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_update', args=[self.post.pk]), {
            'title': 'Обновлённый заголовок',
            'content': 'Обновлённое содержание'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Обновлённый заголовок')
        self.assertEqual(response.status_code, 302)

    def test_post_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)