# Generated by Django 4.2.2 on 2023-07-06 14:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_remove_news_price_news_creationtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='authorNew',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
