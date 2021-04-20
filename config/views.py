from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from cards.models import Lobby
from accounts.models import CustomUser
# Create your views here.

@login_required
def lobby_room(request, lobby_id):
    lobby = Lobby.objects.get(id=lobby_id)
    
    if lobby.host == request.user or lobby.player == None or lobby.player == request.user:
        print(lobby.host.username, "is wack, really!")
        return render(request, 'lobby.html', {'lobby': lobby})
    else:
        return HttpResponseForbidden()