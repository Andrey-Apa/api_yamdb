# Generated by Django 3.2 on 2023-01-29 08:44

from django.db import migrations, models
import users.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(auto_created=True, default=uuid.uuid4, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[users.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]