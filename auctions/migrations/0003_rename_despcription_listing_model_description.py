# Generated by Django 5.1.4 on 2024-12-21 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_model_comment_model_bid_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing_model',
            old_name='despcription',
            new_name='description',
        ),
    ]
