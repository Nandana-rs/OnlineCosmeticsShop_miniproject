# Generated by Django 4.2.5 on 2023-11-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0007_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Customer'), (3, 'Delivery Team'), (4, 'Seller')], default=2),
        ),
    ]
