# Generated by Django 5.0.2 on 2024-02-20 14:57

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.IntegerField(choices=[(1, 'MEN'), (2, 'WOMEN'), (3, 'BABY')])),
                ('image', models.ImageField(upload_to='products/')),
                ('description', ckeditor.fields.RichTextField()),
                ('price', models.PositiveIntegerField()),
                ('discount', models.IntegerField(default=0)),
                ('price_with_discount', models.FloatField(default=0)),
                ('brand', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]