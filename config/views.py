from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from cards.models import Lobby
from accounts.models import CustomUser
from django.views.generic import ListView
from django.db.models import Q


class HomeView(ListView):
    model = Lobby
    template_name = 'home.html'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            object_list = Lobby.objects.filter(Q(host=self.request.user) | Q(player=self.request.user)).distinct()
            return object_list
        else:
            return None
@login_required
def lobby_room(request, lobby_id):
    lobby = Lobby.objects.get(id=lobby_id)
    
    if lobby.host == request.user or lobby.player == None or lobby.player == request.user:
        return render(request, 'lobby.html', {'lobby': lobby})
    else:
        return HttpResponseForbidden()