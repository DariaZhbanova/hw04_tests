from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = {'text', 'group'}
        labels = {'text': 'Введите текст',
                  'group': 'Выберите группу'}
        # help_texts = {'text': '* Какой душе угодно, Лапочка',
        #               'group': "** А как же без нее"}
        # надо вернуть эти параметры, я их отключила только для тестирования
        # verbose_name в уроке Unittest: тестирование модели
