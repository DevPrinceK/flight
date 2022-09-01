from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Wallet
from backend.models import Agency


@receiver(post_save, sender=Agency)
def create_wallet(sender, instance, created, **kwargs):
    '''Create a wallet for new agencies'''
    if created == True:
        wallet = Wallet.objects.create()
        wallet.save()
        instance.wallet = wallet
        instance.save()
        print('Wallet created for Agency')
    else:
        # create wallet for existing agency without a wallet
        if not instance.wallet:
            wallet = Wallet.objects.create()
            wallet.save()
            instance.wallet = wallet
            instance.save()
            print('Wallet created for labourer')
