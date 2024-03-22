# Generated by Django 5.0.3 on 2024-03-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Action', 'Action'), ('Comedy', 'Comedy')], max_length=20),
        ),
    ]