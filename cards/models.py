from django.db import models
from django.conf import settings
# Create your models here.
class Card(models.Model):
    attack = models.PositiveIntegerField()
    health = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    card_art = models.CharField(max_length=150)
    effects = models.CharField(max_length=150)
    level = models.PositiveIntegerField()

class Lobby(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hosted_lobby"
    )
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="joined_lobby"
    )
    win_state = models.PositiveIntegerField(blank=True) #0, host won. 1, client won. 2, draw.