# Generated by Django 3.1.1 on 2020-10-01 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_auto_20201001_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.CharField(choices=[('A', 'Animals'), ('B', 'Books'), ('C', 'Clothes'), ('E', 'Electronics'), ('F', 'Furniture'), ('H', 'Household Goods'), ('J', 'Jewelry'), ('M', 'Makeup'), ('S', 'Sports'), ('V', 'Vehicles')], default='A', max_length=1),
        ),
    ]