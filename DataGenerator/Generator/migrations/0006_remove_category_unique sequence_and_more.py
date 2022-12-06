# Generated by Django 4.1.2 on 2022-12-06 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0005_alter_category_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='category',
            name='Unique Sequence',
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('sequence', 'case'), name='Unique Sequence'),
        ),
    ]
