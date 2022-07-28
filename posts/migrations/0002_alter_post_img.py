# Generated by Django 4.0.5 on 2022-07-23 11:53

from django.db import migrations, models
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.FileField(default='default.jpg', upload_to=posts.utils.post_img_url),
        ),
    ]