# Generated by Django 3.1.5 on 2021-03-21 20:36

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
