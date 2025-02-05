# Generated by Django 5.0.4 on 2024-06-18 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FertilityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N', models.DecimalField(decimal_places=2, max_digits=5)),
                ('P', models.DecimalField(decimal_places=2, max_digits=5)),
                ('K', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pH', models.DecimalField(decimal_places=2, max_digits=4)),
                ('EC', models.DecimalField(decimal_places=2, max_digits=5)),
                ('OC', models.DecimalField(decimal_places=2, max_digits=5)),
                ('S', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Zn', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Fe', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Cu', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Mn', models.DecimalField(decimal_places=2, max_digits=5)),
                ('B', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
