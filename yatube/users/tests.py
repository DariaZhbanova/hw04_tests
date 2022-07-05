from django.test import TestCase, Client


class StaticUrlTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_auth_urls(self):

        urls = ['/auth/login/',
                '/auth/logout/',
                '/auth/signup/',
                # '/auth/password_change/',
                # '/auth/password_change/done/',
                # '/auth/password_reset/',
                # '/auth/password_reset/done/',
                # '/auth/reset/done/',
                ]
        for url in urls:
            try:
                response = self.guest_client.get(url, follow=True)
            except Exception as e:
                assert False, f'''Страница `{url}` работает неправильно.
                    Ошибка: `{e}`'''
            assert response.status_code != 404, (f'Страница `{url}` не найдена,проверьте этот адрес в *urls.py*')
            # self.assertRedirects(response, (f'/auth/login/?next={url}'))
            assert response.status_code == 200, (
                f'Ошибка {response.status_code} при открытиии `{url}`. Проверьте ее view-функцию'
            )
