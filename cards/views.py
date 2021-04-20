from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Lobby
from accounts.models import CustomUser
# Create your views here.
def chat_room(request, lobby_id):
    lobby = Lobby.objects.get(id=lobby_id)
    if lobby.host == request.user or lobby.player == None:
        return render(request, 'lobby.html', {'lobby': lobby})
    else:
        return HttpResponseForbidden()