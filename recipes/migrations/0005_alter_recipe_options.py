# Generated by Django 4.2.14 on 2024-08-05 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created_on']},
        ),
    ]
