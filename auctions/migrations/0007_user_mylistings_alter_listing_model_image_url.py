# Generated by Django 5.1.4 on 2024-12-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_model_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mylistings',
            field=models.ManyToManyField(related_name='MyUser', to='auctions.listing_model'),
        ),
        migrations.AlterField(
            model_name='listing_model',
            name='image_url',
            field=models.URLField(),
        ),
    ]
