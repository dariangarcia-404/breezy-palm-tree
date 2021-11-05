from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


@login_required
def watchlist(request):
    mwatchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": mwatchlist
    })


def listing(request, id):
    listings = Listing.objects.all().filter(id=id)
    if not listings:
        return render(request, "auctions/error.html", {
            "message": "is not a Listing."
        })
    mlisting = listings[0]
    is_watching = False
    if request.user.is_authenticated:
        is_watching = mlisting in request.user.watchlist.all()  # T or F
    message = ""
    # When we're posting.
    if request.method == "POST":
        if "bidprice" in request.POST.keys():
            bidprice = request.POST["bidprice"]
            if bidprice:
                bidprice = int(bidprice)
                if (mlisting.current_price == mlisting.starting_price and
                    bidprice < mlisting.starting_price) or \
                    (mlisting.current_price != mlisting.starting_price and
                     bidprice <= mlisting.current_price):
                    message = "Bidprice must be higher than current \
                    bid, if there is one. If there isn't one, it must \
                    be as large as the starting bid."
                else:
                    bid = Bid(bidder=request.user, listing=mlisting,
                              amount=bidprice)
                    bid.save()
                    mlisting.current_price = mlisting.max_bid()
                    mlisting.save()
        elif "comment_text" in request.POST.keys():
            comment_text = request.POST["comment_text"]
            if comment_text:
                comment = Comment(commenter=request.user, listing=mlisting,
                                  comment_text=comment_text)
                comment.save()
        elif "add_watchlist" in request.POST.keys():
            if not is_watching:
                request.user.watchlist.add(mlisting)
            else:
                request.user.watchlist.remove(mlisting)
        elif "close_listing" in request.POST.keys():
            mlisting.is_open = False
            mlisting.save()
            winner = mlisting.max_bidder()
            message = f"Listing is closed. Winner is {winner}"
    if request.user.is_authenticated:
        is_watching = mlisting in request.user.watchlist.all()  # T or F
    # Rendering the page.
    return render(request, "auctions/listing.html", {
        "winner": mlisting.max_bidder(),
        "message": message,
        "listing": mlisting,
        "is_watching": is_watching,
        "comments": mlisting.lcomments.all(),
        "is_creator": request.user == mlisting.seller  # T or F
    })


@login_required
def createlisting(request):
    message = ""
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingbid = request.POST["startingbid"]
        url = request.POST["url"]
        seller = request.user
        listing = Listing(title=title, description=description,
                          current_price=startingbid,
                          starting_price=startingbid,
                          url=url, seller=seller, is_open=True)
        listing.save()
        message = "Listing was created"
    return render(request, "auctions/createlisting.html", {
        "message": message
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


@login_required
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
