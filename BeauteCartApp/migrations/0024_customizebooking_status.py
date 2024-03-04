# Generated by Django 4.2.5 on 2024-03-01 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0023_alter_customizebooking_beautician'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizebooking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
