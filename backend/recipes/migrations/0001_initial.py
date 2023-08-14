# Generated by Django 2.2.19 on 2023-08-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название Тэга')),
                ('color', models.CharField(max_length=7, verbose_name='Цвет в hex формате')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
