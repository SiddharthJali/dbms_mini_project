# Generated by Django 5.0.3 on 2024-03-09 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_movie_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_poster',
            field=models.ImageField(upload_to='movie_posters/'),
        ),
    ]
