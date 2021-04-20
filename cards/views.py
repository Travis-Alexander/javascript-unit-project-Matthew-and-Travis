from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from chat.models import Room
from accounts.models import CustomUser
# Create your views here.
def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.owner == request.user or room.users.get(id=request.user.id):
        return render(request, 'room.html', {'room': room})
    else:
        return HttpResponseForbidden()