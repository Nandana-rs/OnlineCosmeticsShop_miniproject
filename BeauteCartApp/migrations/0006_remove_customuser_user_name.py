# Generated by Django 4.2.5 on 2023-11-02 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0005_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_name',
        ),
    ]
