# Generated by Django 3.0.6 on 2020-06-15 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_auto_20200615_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedlink',
            name='shortened_link',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
