from accounts.models import User
import requests
import array
from core import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from django.template import Context, loader


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


@receiver(post_save, sender=Ticket)
def send_email(sender, instance, created, **kwargs):
    '''send ticket to user via email'''
    if created:
        subject = "Trip Booking Ticket"
        template_name = "backend/notifications/ticket.html"
        receipients = [instance.transaction.booking.user.email]
        send_generic_email(instance, subject, template_name, receipients)


@receiver(post_save, sender=Agency)
def notify_admins_and_agency(sender, instance, created, **kwargs):
    contact = instance.phone if instance.phone is not None else ''
    name = instance.name if instance.name is not None else ''
    email = instance.email if instance.email is not None else ''
    agency_admins = User.objects.filter(agency=instance)
    nums = [str(agency_admin.phone).strip() for agency_admin in agency_admins]
    nums.append(str(instance.phone))
    nums.append("0558366133")
    if created:
        subject = "New Agency Sign-up."
        message = "Hey there! \nThere is a new agency sign-up. \nKindly confirm and approve!"
        # For admins
        agency_info = name + ' ' + contact + ' ' + email + ' \n'
        body = subject.upper() + ' \n\n' + message
        content = body + ' \n\n' + 'FROM: \n' + agency_info
        send_sms("EasyGo", content, ["0558366133", "0546573849", "0243555025", "0545065461"])  # noqa
        # for agencies
        message = "Hey there! \nWe have received your application to transact with EasyGo Trasport.\nWe are doing our due deligence and will get your agency approved as soon as possible."
        agency_info = name + ' ' + contact + ' ' + email + ' \n'
        body = subject.upper() + ' \n\n' + message
        content = body + ' \n\n' + 'AGENCY INFO: \n' + agency_info
        send_sms("EasyGo", content, nums)
    else:
        if instance.is_approved:
            # for agencies
            message = "Congratulations! \nYour application to transact on EasyGO has been approved. \nKindly log onto the portal to start transacting."
            subject = "Agency Approved!"
            agency_info = name + ' ' + contact + ' ' + email + ' \n'
            body = subject.upper() + ' \n\n' + message
            content = body + ' \n\n' + 'AGENCY INFO: \n' + agency_info
            try:
                send_sms("EasyGo", content, nums)
            except Exception as e:
                print(e)
            finally:
                print("CONGRATULATIONS PART OF THE CODE RUNS")


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


def send_generic_email(ticket, subject, template_name, receipients):
    '''Send mail to user who booked the trip'''
    text = render_to_string(template_name, {
        'ticket': ticket,
    })
    # t = loader.get_template(tempiclate_name)
    # html = t.render(Context({'tket': ticket}))
    msg = EmailMultiAlternatives(
        subject, text,
        settings.EMAIL_HOST_USER, receipients)
    msg.attach_alternative(text, "text/html")
    try:
        msg.send()
    except Exception as err:
        print(err)
    else:
        print("Successful....Email sent to: ", receipients)
