from django.db import models

# Create your models here.
class Card(models.Model):
    attack = models.PositiveIntegerField()
    health = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    card_art = models.CharField(max_length=150)
    effects = models.CharField(max_length=150)
    level = models.PositiveIntegerField()