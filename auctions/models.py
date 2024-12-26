from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class listing_model(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)
    category = models.CharField(max_length = 15)
    image_url = models.URLField(max_length = 200)
    created_at = models.DateTimeField(default=timezone.now)
    createdby = models.ForeignKey("User",on_delete=models.CASCADE, related_name="mylistings")
    is_closed = models.BooleanField(default = False)
    starting_price = models.IntegerField()
    winner = models.ForeignKey("User",on_delete=models.CASCADE, related_name="listings_won",blank = True,null = True)
    def __str__(self):
        return f"{self.title}"

class User(AbstractUser, models.Model):
    watchlist = models.ManyToManyField(listing_model, blank = True, related_name = "usersinwatchlist")

class bid_model(models.Model):
    price = models.IntegerField()
    user_bid = models.ForeignKey(User,on_delete= models.CASCADE, related_name="bidsbyuser")
    listing_bid = models.ForeignKey(listing_model, on_delete= models.CASCADE, related_name="bidsinlisting")
    def __str__(self):
        return f"Bid placed by {self.user_bid} priced {self.price} listed as {self.listing_bid}"

class comment_model(models.Model):
    content = models.CharField(max_length = 200)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "commentsbyuser")
    listing_comment = models.ForeignKey(listing_model,on_delete=models.CASCADE, related_name="commentsinlisting")
    def __str__(self):
        return f"Comment made by {self.user_comment} listed as {self.listing_comment}"