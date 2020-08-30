"""api_wallet URL Configuration

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
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from accounts.views import UserViewSet
from user_wallet.views import (WalletDetailsViewSet, AddAmountViewSet,
                               PayAmountViewSet, TransactionsViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'wallet_details', WalletDetailsViewSet,
                basename="wallet_details")
router.register(r'add_amount', AddAmountViewSet, basename="add_amount")
router.register(r'pay_amount', PayAmountViewSet, basename="pay_amount")
router.register(r'all_transactions', TransactionsViewSet,
                basename="all_transactions")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
