# Generated by Django 5.0.4 on 2024-05-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='identification_number',
            field=models.CharField(default=123, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
