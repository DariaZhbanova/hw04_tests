# Generated by Django 2.2.16 on 2022-07-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20220710_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pics',
            field=models.ImageField(blank=True, null=True, upload_to='img_post'),
        ),
        migrations.AddField(
            model_name='post',
            name='text_title',
            field=models.CharField(blank=True, help_text='Привлеките внимание читателей самым важным', max_length=200, null=True),
        ),
    ]
