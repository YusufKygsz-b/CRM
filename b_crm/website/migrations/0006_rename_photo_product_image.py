# Generated by Django 5.0.7 on 2024-08-10 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_product_photo_alter_product_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='photo',
            new_name='image',
        ),
    ]
