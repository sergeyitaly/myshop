# Generated by Django 3.2.12 on 2024-04-17 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20240414_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/collection'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brandimage',
            field=models.FileField(blank=True, null=True, upload_to='photos/svg'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/product'),
        ),
    ]
