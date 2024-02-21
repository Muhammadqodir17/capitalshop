# Generated by Django 5.0.2 on 2024-02-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(1, 'MEN'), (2, 'WOMEN'), (3, 'BABY')], default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
