from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, FriendRequest
from cards.models import Card
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserProfile(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/user_profile.html"
    context_object_name = "profile_user"



def SendFriendRequest(request, userID):
    user = request.user
    receiver = CustomUser.objects.get(id=userID)
    friendRequest, created = FriendRequest.objects.get_or_create(
        user=user, receiver=receiver
    )
    if created:
        messages.success(request, "Friend request sent.")
        print("sent")
        return redirect(f"/user/{receiver.id}")
    else:
        messages.error(request, "Friend request already created.")
        print('stop')
        return redirect(f"/user/{receiver.id}")


def AcceptFriendRequest(request, requestID):
    friendRequest = FriendRequest.objects.get(id=requestID)
    if friendRequest.receiver == request.user:
        friendRequest.user.friends.add(friendRequest.receiver)
        friendRequest.receiver.friends.add(friendRequest.user)
        friendRequest.delete()
        messages.success(request, "Friend request accepted.")
        return redirect(f"/user/{request.user.id}")
    else:
        messages.error(request, "Friend request not accepted.")
        return redirect(f"/user/{request.user.id}")

def DeclineFriendRequest(request, requestID):
    friendRequest = FriendRequest.objects.get(id=requestID)
    if friendRequest.receiver == request.user:
        friendRequest.delete()
        messages.success(request, "Friend request declined.")
        return redirect(f"/user/{request.user.id}")
    else:
        messages.error(request, "Friend request not declined.")
        return redirect(f"/user/{request.user.id}")


def RemoveFriend(request, userID):
    user = request.user
    friend = CustomUser.objects.get(id=userID)
    user.friends.remove(friend)
    friend.friends.remove(user)
    messages.success(request, "Friend removed.")
    return redirect(f"/user/{request.user.id}")

@csrf_exempt
def UpdateDeck(request):
    user = request.user
    print(request.user)
    print(request.body.decode())
    updates = json.loads(request.body)
    for card_to_add in updates['cards_to_add']:
        print(card_to_add)
        user.decks.add(card_to_add)
        
    for card_to_remove in updates['cards_to_remove']:
        user.decks.remove(card_to_remove)
    
    return redirect(f'/customize_deck/')

class DeckCustomization(ListView):
    model = Card 
    template_name = "deck.html"
    
    def get_queryset(self):
        return Card.objects.all()
    