# Generated by Django 4.2.4 on 2023-08-21 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_recipe_pub_date_alter_recipe_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
    ]
