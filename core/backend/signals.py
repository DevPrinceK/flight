import requests
import array
from core import settings
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


@receiver(post_save, sender=Agency)
def notify_devprincek(sender, instance, created, **kwargs):
    if created:
        contact = instance.phone if instance.phone is not None else ''
        name = instance.name if instance.name is not None else ''
        email = instance.email if instance.email is not None else ''
        subject = "New Agency Sign-up."
        message = "Hey there! \n There is a new agency sign-up. \n Kindly confirm and approve!"

        # For admins
        agency_info = name + ' ' + contact + ' ' + email + ' \n'
        body = subject.upper() + ' \n\n' + message
        content = body + ' \n\n' + 'FROM: \n' + agency_info
        send_sms("EasyGo Transport", content, ["0558366133"])

        # for agencies
        message = "Hey there! \n We have received your application to transact with EasyGo Trasport. \n We are doing our due deligence and will get your agency approved as soon as possible."
        agency_info = name + ' ' + contact + ' ' + email + ' \n'
        body = subject.upper() + ' \n\n' + message
        content = body + ' \n\n' + 'AGENCY INFO: \n' + agency_info
        send_sms("EasyGo Transport", content, ["0558366133"])
    else:
        if instance.is_approved:
            # for agencies
            message = "Congratulations! \n Your application to transact on EasyGO has been approved. \n Kindly log into the portal to start transacting."
            subject = "Agency Approved!"
            agency_info = name + ' ' + contact + ' ' + email + ' \n'
            body = subject.upper() + ' \n\n' + message
            content = body + ' \n\n' + 'AGENCY INFO: \n' + agency_info
            send_sms("EasyGo Transport", content, ["0558366133"])


def send_sms(sender: str, message: str, recipients: array.array):
    header = {"api-key": settings.ARKESEL_API_KEY, 'Content-Type': 'application/json',
              'Accept': 'application/json'}
    SEND_SMS_URL = "https://sms.arkesel.com/api/v2/sms/send"
    payload = {
        "sender": sender,
        "message": message,
        "recipients": recipients
    }
    response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    print(response.json())
    return response.json()
