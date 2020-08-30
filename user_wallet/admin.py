from django.contrib import admin

# Register your models here.
from user_wallet.models import Transactions


@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'extra_feild', 'created_at', 'modified_at')
