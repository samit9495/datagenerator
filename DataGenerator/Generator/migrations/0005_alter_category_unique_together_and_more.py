# Generated by Django 4.1.2 on 2022-12-06 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0004_alter_category_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('length', 'sequence', 'case', 'type'), name='Unique Sequence'),
        ),
    ]
