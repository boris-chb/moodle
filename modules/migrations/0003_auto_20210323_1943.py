# Generated by Django 3.1.5 on 2021-03-23 19:43

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('modules', '0002_auto_20210321_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='tag',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
