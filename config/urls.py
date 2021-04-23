"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import lobby_room
from accounts.views import (
    AcceptFriendRequest,
    DeclineFriendRequest,
    RemoveFriend,
    SendFriendRequest,
    UserProfile,
    UpdateDeck,
    DeckCustomization
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('lobby/<int:lobby_id>/', lobby_room, name="lobby"),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('user/<int:pk>', UserProfile.as_view(), name="user_profile"),
    path('send_friend_request/<int:userID>/', SendFriendRequest, name="send_friend_request",),
    path("accept_friend_request/<int:requestID>/", AcceptFriendRequest, name="accept_friend_request",),
    path("decline_friend_request/<int:requestID>/", DeclineFriendRequest, name="decline_friend_request",),
    path("remove_friend/<int:userID>/", RemoveFriend, name="remove_friend"),
    path("customize_deck/", DeckCustomization.as_view(), name="deck_customization"),
    path("customize_deck/save", UpdateDeck, name="deck_customization/save"),
]
