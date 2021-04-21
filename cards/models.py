from django.db import models
from django.conf import settings
# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=50, blank=True)
    attack = models.PositiveIntegerField()
    health = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    card_art = models.CharField(max_length=150)
    effects = models.CharField(max_length=150)
    level = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class Lobby(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hosted_lobby"
    )
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="joined_lobby",
        blank=True,
        null=True
    )
    win_state = models.PositiveIntegerField(blank=True, null=True) #0, host won. 1, client won. 2, draw.