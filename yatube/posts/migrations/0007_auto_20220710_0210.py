# Generated by Django 2.2.16 on 2022-07-09 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220710_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pics',
            field=models.ImageField(blank=True, null=True, upload_to='img_post'),
        ),
    ]
