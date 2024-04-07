# Generated by Django 4.2.5 on 2024-04-06 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0031_logisticscompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('OUT_FOR_DELIVERY', 'Out for Delivery'), ('DELIVERED', 'Delivered')], default='PENDING', max_length=20),
        ),
    ]
