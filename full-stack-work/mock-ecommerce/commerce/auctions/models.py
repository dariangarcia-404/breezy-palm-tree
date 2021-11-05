from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing')

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    current_price = models.IntegerField()
    starting_price = models.IntegerField()
    is_open = models.BooleanField()
    url = models.CharField(max_length=280)

    def max_bid(self):
        max = 0
        for lbid in self.lbids.all():
            if lbid.amount > max:
                max = lbid.amount
        if max < self.starting_price:
            return self.starting_price
        return max

    def max_bidder(self):
        max = 0
        highest_bidder = "No One"
        for lbid in self.lbids.all():
            if lbid.amount > max:
                max = lbid.amount
                highest_bidder = lbid.bidder
        return highest_bidder

    def __str__(self):
        return f"{self.title} | {self.description} | ${self.current_price}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="ubids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name="lbids")
    amount = models.IntegerField()

    def __str__(self):
        return f"Bidder: {self.bidder} | Listing: {self.listing} | \
                 Amount: ${self.amount}"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="ucomments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name="lcomments")
    comment_text = models.CharField(max_length=280)

    def __str__(self):
        return f"{self.comment_text}"
