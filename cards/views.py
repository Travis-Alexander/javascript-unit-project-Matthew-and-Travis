from django.shortcuts import render
from django.views.generic import CreateView
from .models import Lobby
from django.urls import reverse_lazy, reverse
# Create your views here.

class StartNewLobby(CreateView):
    template_name = "new_lobby.html"
    model = Lobby
    fields = ["player"]
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)