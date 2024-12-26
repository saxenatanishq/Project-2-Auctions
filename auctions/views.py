from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,listing_model,bid_model,comment_model

categories = ["None","Electronics","Home","Books","Sports","Health","Toys","Fashion","Music"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = comment_model
        fields = ['content','user_comment','listing_comment']

class BidForm(forms.ModelForm):
    class Meta:
        model = bid_model
        fields = ['price','user_bid','listing_bid']

class NewListingForm(forms.ModelForm):
    class Meta:
        model = listing_model
        fields = ['title','description','category','image_url','createdby','starting_price']

def listing_page(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse(request, "Error: Form was invalid")
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "auctions/new_listing.html",{
            "form":NewListingForm(),
            "categories":categories
        })

def index(request):
    return render(request, "auctions/index.html",{
        "listings":listing_model.objects.filter(is_closed = False),
        "categories":categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_view(request, listing_id):
    listing = listing_model.objects.get(pk = listing_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        form = CommentForm(request.POST)
        form1 = BidForm(request.POST)
        if form.is_valid():
            form.save()
            n = 0
            max_bid = listing.starting_price
            for bid in bid_model.objects.filter(listing_bid = listing):
                n+=1
                if max_bid<bid.price:
                    max_bid = bid.price
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "listofusers":listing.usersinwatchlist.all(),
                "comment_form":CommentForm(),
                "bid_form":BidForm(),
                "comments":comment_model.objects.filter(listing_comment = listing),
                "bids":bid_model.objects.filter(listing_bid = listing),
                "no_of_bids":n,
                "current_bid":max_bid
            })
        elif form1.is_valid():
            max_bid = listing.starting_price
            n = 0
            for bid in bid_model.objects.filter(listing_bid = listing):
                n+=1
                if max_bid<bid.price:
                    max_bid = bid.price
            if form1.cleaned_data["price"] > max_bid:
                max_bid = form1.cleaned_data["price"]
                form1.save()
            else:
                return render(request,"auctions/listing.html",{
                    "listing":listing,
                    "listofusers":listing.usersinwatchlist.all(),
                    "comment_form":CommentForm(),
                    "bid_form":BidForm(),
                    "comments":comment_model.objects.filter(listing_comment = listing),
                    "bids":bid_model.objects.filter(listing_bid = listing),
                    "no_of_bids":n,
                    "current_bid":max_bid,
                    "bid_error": f"Please place the bid greater than the current price ({max_bid}$)"
                })
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "listofusers":listing.usersinwatchlist.all(),
                "comment_form":CommentForm(),
                "bid_form":BidForm(),
                "comments":comment_model.objects.filter(listing_comment = listing),
                "bids":bid_model.objects.filter(listing_bid = listing),
                "no_of_bids":n+1,
                "current_bid":max_bid
            })
        else:
            if listing in request.user.watchlist.all():
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)

    n = 0
    max_bid = listing.starting_price
    for bid in bid_model.objects.filter(listing_bid = listing):
        n+=1
        if max_bid<bid.price:
            max_bid = bid.price
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "listofusers":listing.usersinwatchlist.all(),
        "comment_form":CommentForm(),
        "bid_form":BidForm(),
        "comments":comment_model.objects.filter(listing_comment = listing),
        "bids":bid_model.objects.filter(listing_bid = listing),
        "no_of_bids":n,
        "current_bid":max_bid
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "listings":request.user.watchlist.all()
    })

def categoriesf(request):
    return render(request,"auctions/categories.html",{
        "categories": categories
    })

def category_name(request, category_name):
    return render(request,"auctions/category.html",{
        "category": category_name,
        "listings": listing_model.objects.filter(category = category_name,is_closed = False)
    })

def close_auction(request, listing_id):
    if request.method == "POST":
        listing = listing_model.objects.get(pk = listing_id)
        max_bid = listing.starting_price
        n = 0
        for bid in bid_model.objects.filter(listing_bid = listing):
            n+=1
            if max_bid<bid.price:
                max_bid = bid.price
                winner = bid.user_bid
        listing.is_closed = True
        listing.winner = winner
        listing.save()
        return render(request,"auctions/listing.html",{
            "listing":listing,
            "listofusers":listing.usersinwatchlist.all(),
            "comment_form":CommentForm(),
            "bid_form":BidForm(),
            "comments":comment_model.objects.filter(listing_comment = listing),
            "bids":bid_model.objects.filter(listing_bid = listing),
            "no_of_bids":n,
            "current_bid":max_bid
        })

def closed(request):
    return render(request, "auctions/closed.html",{
        "listings":listing_model.objects.filter(is_closed = True),
        "categories":categories
    })
