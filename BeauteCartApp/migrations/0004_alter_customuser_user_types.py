# Generated by Django 4.2.5 on 2023-11-02 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeauteCartApp', '0003_remove_product_discount_remove_product_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_types',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Customer'), (3, 'Deliveryteam'), (4, 'Seller')], default=2),
        ),
    ]
