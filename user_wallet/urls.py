from django.urls import path
from user_wallet.views import index


urlpatterns = [
    path('', index, name='index')
]
