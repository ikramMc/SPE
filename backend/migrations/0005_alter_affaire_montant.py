# Generated by Django 4.2.1 on 2023-09-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_affaire_commune'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaire',
            name='montant',
            field=models.CharField(max_length=40, null=True),
        ),
    ]