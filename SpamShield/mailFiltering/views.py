from django.shortcuts import render, redirect
from django.http import HttpResponse

from imap_tools import MailBox, AND, OR, MailMessageFlags

from .models import Domain, Serveur

from .spam.checkMails import checkMail
from .spam.gestion import getMailsServeur

import logging

logger = logging.getLogger("django")

def getMails(serveur):
    logger.debug("getMails " + serveur)
    return getMailsServeur(serveur)


def index(request):
    serveurs = Serveur.objects.all()
    messages = []
    if len(serveurs) > 0:
        serveur = serveurs[0]
        messages = getMails(serveur)
            
    return render(
            request,
            "liste.html",
            {
                "messages": messages,
                "serveurs": serveurs,
                "serveur": serveur.id,
            },
        )
        
def listemails(request, serveur_id):
    serveurs = Serveur.objects.all()
    serveur = Serveur.objects.get(id=serveur_id)
    messages = getMails(serveur)
    return render(
            request,
            "liste.html",
            {
                "messages": messages,
                "serveurs": serveurs,
                "serveur": serveur.id,
            },
        )

def gestionMails(request, serveur_id):
    logger.debug("gestionMails " + request)
    action = request.POST["action"]
    logger.debug("action " + action)
    mailsUID = request.POST["mailsUID"]
    logger.mailsUID("mailsUID " + mailsUID)
    domains = request.POST["domains"]
    logger.debug("domains " + domains)
        
def serveurs(request):
    serveurs = Serveur.objects.all()
    return render(
            request,
            "serveurs.html",
            {
                "serveurs": serveurs,
            },
        )
        
def serveur(request, serveur_id):
    serveur = Serveur.objects.get(id=serveur_id)
    return render(
            request,
            "serveur.html",
            {
                "serveur": serveur,
            },
        )
        
def saveServeur(request, serveur_id):
    serveur = Serveur.objects.get(id=serveur_id)
    serveur.password = request.POST["password"]
    serveur.host = request.POST["host"]
    serveur.user = request.POST["user"]
    serveur.save()
    return redirect("serveurs")
