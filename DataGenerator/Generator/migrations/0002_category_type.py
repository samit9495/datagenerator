# Generated by Django 4.1.2 on 2022-11-28 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(default=False, max_length=50),
            preserve_default=False,
        ),
    ]