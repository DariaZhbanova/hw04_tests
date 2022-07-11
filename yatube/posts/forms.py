from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        # fields = {'text_title', 'text', 'pics', 'group'}
        fields = {'text', 'group'}
        labels = {
            'text_title': 'Заголовок',
            'text': 'Введите текст:',
            'group': 'Выберите группу:'
        }
