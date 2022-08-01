# Generated by Django 4.0.5 on 2022-08-01 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_alter_comment_comment_by_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_by',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.RESTRICT, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post'),
        ),
    ]
