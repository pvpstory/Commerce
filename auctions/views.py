from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from auctions.models import listings, watchlist,comments,bids,User

def index(request):
    return render(request, "auctions/index.html", {
        "listings": listings.objects.all(),
        "bids": bids.objects.all()
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
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST.get('starting_bit')
        category = request.POST.get('category')
        creator = request.user
        image_URL= request.POST["image_URL"]

        new_listing1 = listings.objects.create(
            title=title,
            description=description,
            starting_bit=starting_bid,
            category=category,
            creator=creator,
            image_URL=image_URL,
            current_price=starting_bid
        )
        new_listing1.save()

        new_bid = bids.objects.create(
            listing=new_listing1,
            creator=creator,
            current_bid=starting_bid

        )
        new_bid.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/new_listing.html")
def listing(request, listing_id):
    if request.method == "POST":
        listing=listings.objects.get(id=listing_id)
        listing.closed=True
        listing.save()
    if request.user.is_authenticated:
        watchlist_ = watchlist.objects.filter(user=request.user, listing=listing_id)
    else:
        watchlist_ = []
    return render(request, "auctions/listing.html",{
        "listing": listings.objects.get(id=listing_id),
        "comments": comments.objects.filter(listing=listing_id),
        "watchlist": watchlist_,
        "bid": bids.objects.get(listing=listing_id),
    })

def watchlist_view(request):
    if request.method == "POST":
        if "add_to_watchlist" in request.POST:
            listing_id = request.POST["listing_id"]

            new_watchlist = watchlist.objects.create(
                user=request.user,
                listing=listings.objects.get(id=listing_id)
            )
            new_watchlist.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        if "remove_from_watchlist" in request.POST:
            listing_id = request.POST["listing_id"]
            watchlist.objects.filter(user=request.user, listing=listing_id).delete()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        if "add_comment" in request.POST:
            listing_id = request.POST["listing_id"]
            comment = request.POST["comment"]


            new_comment = comments.objects.create(
                creator=request.user,
                listing=listings.objects.get(id=listing_id),
                comment=comment
            )
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        if "make_a_bid" in request.POST:
            listing_id = request.POST["listing_id"]
            new_bid = request.POST["new_bid"]

            bid = bids.objects.get(listing=listing_id)
            if bid.current_bid >= int(new_bid):
                return render(request,"auctions/error.html")
            listing = listings.objects.get(id=listing_id)

            listing.current_price = new_bid
            bid.current_bid = new_bid
            bid.current_winner = request.user
            listing.save()
            bid.save()
            return HttpResponseRedirect(reverse("listing",args=(listing_id,)))



    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist.objects.filter(user=request.user)
    })

def categories(request):
    return render(request,"auctions/categorogies.html",{
        "categories": listings.objects.values('category').distinct()
    })
def category(request, category):
    return render(request,"auctions/category.html",{
        "listings": listings.objects.filter(category=category),
        "category": category
    })
def my_listings(request):
    return render(request,"auctions/my_listings.html", {
        "listings": listings.objects.filter(creator=request.user)
    })
def closed_listings(request):
    return render(request, "auctions/closed.html",{
        "listings": listings.objects.filter(closed=True)
    })





