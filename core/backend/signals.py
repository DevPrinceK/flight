from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Ticket, Wallet
from backend.models import Agency
from backend.models import Transaction


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


@receiver(post_save, sender=Transaction)
def generate_ticket(sender, instance, created, **kwargs):
    '''Generate ticket for new transactions'''
    if created == True:
        if instance.status_code == "000":
            Ticket.objects.create(transaction=instance)
    else:
        # generate ticket for existing transaction without a ticket
        if instance.status_code == "000":
            ticket = Ticket.objects.filter(transaction=instance).first()
            if not ticket:
                Ticket.objects.create(transaction=instance)
