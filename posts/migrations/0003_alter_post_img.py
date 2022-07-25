# Generated by Django 4.0.5 on 2022-07-23 13:36

from django.db import migrations, models
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to=posts.utils.post_img_url),
        ),
    ]
