# Generated by Django 4.2.5 on 2023-11-23 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_blogs_options_blogs_article_body_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='article_body',
            new_name='blog_data',
        ),
        migrations.RemoveField(
            model_name='blogs',
            name='description',
        ),
        migrations.RemoveField(
            model_name='blogs',
            name='imageurl',
        ),
    ]