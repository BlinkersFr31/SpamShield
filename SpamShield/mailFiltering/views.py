from django.shortcuts import render, redirect
from django.http import HttpResponse

from imap_tools import MailBox, AND, OR, MailMessageFlags

from .models import Domain, Serveur

from .spam.checkMails import checkMail

def getMails(serveur):
    messages = []
    with MailBox(serveur.host).login(serveur.user, serveur.password, initial_folder='junk') as mailbox:
        for msg in mailbox.fetch(AND(keyword="SPAM_BLOCKLIST"), mark_seen=False, reverse=True, bulk=True):
            messages.append(msg)
        for msg in mailbox.fetch(AND(keyword="SPAM_DKIM"), mark_seen=False, reverse=True, bulk=True):
            messages.append(msg)
        for msg in mailbox.fetch(AND(keyword="SPAM_DKIM_DIFF"), mark_seen=False, reverse=True, bulk=True):
            messages.append(msg)
        for msg in mailbox.fetch(AND(keyword="SPAM_DOMAIN_DIFF"), mark_seen=False, reverse=True, bulk=True):
            messages.append(msg)
    with MailBox(serveur.host).login(serveur.user, serveur.password) as mailbox:
        for msg in mailbox.fetch(AND(seen=False), mark_seen=False, reverse=True, bulk=True):
            checkMail(msg, mailbox)
            messages.append(msg)
    return messages


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