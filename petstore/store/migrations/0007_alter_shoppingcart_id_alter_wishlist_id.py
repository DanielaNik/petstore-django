# Generated by Django 4.2.3 on 2023-08-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_category_coverphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
