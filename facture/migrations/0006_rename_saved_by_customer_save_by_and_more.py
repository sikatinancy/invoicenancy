# Generated by Django 5.1 on 2025-01-16 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0005_alter_invoice_saved_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='saved_by',
            new_name='save_by',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='saved_by',
            new_name='save_by',
        ),
    ]
