# Generated by Django 4.2.13 on 2024-05-20 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_product_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='available',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='description',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='price',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='stock',
        ),
    ]
