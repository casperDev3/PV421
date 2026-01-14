from django.shortcuts import render
from notifications.consumers import MassMailerConsumer
from .models  import Mailer

def mailer_create():
    smm = MassMailerConsumer()
    smm.send_mass_mail(
        status="Mass email sent successfully.",
        message="This is a mass email sent to all users.",
        progress=100
    )
    return None


def mailer_list():
    # get list of mailers
    print("test")
    # smm = MassMailerConsumer()
    # smm.send_mass_mail(
    #     status="Mass email sent successfully.",
    #     message="This is a mass email sent to all users.",
    #     progress=100
    # )
    return "mailer list"