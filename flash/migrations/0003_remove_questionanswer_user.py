# Generated by Django 4.1.7 on 2023-03-10 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flash', '0002_questionanswer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswer',
            name='user',
        ),
    ]
