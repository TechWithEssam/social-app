# Generated by Django 4.1 on 2022-08-10 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_likecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
