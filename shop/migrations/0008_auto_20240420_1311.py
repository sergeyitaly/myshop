# Generated by Django 3.2.12 on 2024-04-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20240420_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('name',), 'verbose_name': 'Collection', 'verbose_name_plural': 'Collections'},
        ),
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
