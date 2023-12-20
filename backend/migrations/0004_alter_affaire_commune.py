# Generated by Django 4.2.1 on 2023-09-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_affaire_montant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaire',
            name='commune',
            field=models.CharField(choices=[('AIN TAYA', 'At'), ('BAB EZZOUAR', 'Bez'), ('BORDJ EL BAHRI', 'Beb'), ('DAR EL BEIDA', 'Deb'), ('MOHAMMADIA', 'Mda'), ('BORDJ EL KIFFAN', 'Bek'), ('DERGANA', 'Der'), ('EL HAMIZ', 'El Hamiz'), ('EL MARSA', 'El Marsa')], max_length=40, null=True),
        ),
    ]