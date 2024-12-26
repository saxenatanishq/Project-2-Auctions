from django.contrib import admin
from .models import bid_model, comment_model, listing_model, User

# Register your models here.
admin.site.register(User)
admin.site.register(listing_model)
admin.site.register(bid_model)
admin.site.register(comment_model)