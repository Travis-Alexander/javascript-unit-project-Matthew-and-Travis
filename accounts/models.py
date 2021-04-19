from django.db import models
from django.contrib.auth.models import AbstractUser
from cards.models import Card
# Create your models here.
class CustomUser(AbstractUser):
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    decks = models.ManyToManyField(Card, blank=True, symmetrical=False, related_name="decks")


