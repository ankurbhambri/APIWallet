from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(verbose_name='modified', auto_now=True)

    class Meta:
        abstract = True


class WalletDetails(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_upi = models.CharField(max_length=50, null=False, default=None)
    balance = models.FloatField()

    def __str__(self):
        return self.user_upi


class PayAmount(TimeStampedModel):
    user_upi = models.CharField(max_length=50, null=False, blank=False)
    pay_amount = models.FloatField()


class Transactions(TimeStampedModel):
    wallet = models.ForeignKey(WalletDetails, on_delete=models.CASCADE)
    extra_feild = JSONField()
