# Generated by Django 4.1.2 on 2022-11-26 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('length', models.IntegerField()),
                ('sequence', models.CharField(max_length=100)),
                ('case', models.CharField(max_length=20)),
            ],
        ),
    ]
