# Generated by Django 4.0.5 on 2022-07-28 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
