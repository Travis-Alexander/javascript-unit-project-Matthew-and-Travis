from django.db import models
from django.contrib.auth.models import AbstractUser
from cards.models import Card
# Create your models here.
class CustomUser(AbstractUser):
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    decks = models.ManyToManyField(Card, blank=True, symmetrical=False, related_name="decks")
    friends = models.ManyToManyField("CustomUser", blank=True)

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return f"Sender: {self.user}, Receiver: {self.receiver}"
