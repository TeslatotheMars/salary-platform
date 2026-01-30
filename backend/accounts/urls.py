from django.urls import path
from .views import register, login, refresh, me, health, TokenView

urlpatterns = [
    path("health", health),
    path("auth/register", register),
    path("auth/login", login),
    path("auth/refresh", refresh),
    # optional: JWT standard obtain pair endpoint (with custom claims)
    path("auth/token", TokenView.as_view(), name="token_obtain_pair"),
    path("me", me),
]
