# Generated by Django 4.2.5 on 2023-11-02 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0006_remove_customuser_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'Customer'), (3, 'Delivery Team'), (4, 'Seller')], default=2, max_length=20),
        ),
    ]
