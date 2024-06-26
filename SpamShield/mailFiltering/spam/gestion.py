from imap_tools import MailBox, AND, MailMessageFlags

import logging
from mailFiltering.models import Domain
from .checkMails import checkMail

logger = logging.getLogger("django")

def getMailsServeur(serveur):
    logger.info("getMailsServeur " + str(serveur))
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
    logger.debug(str(messages))
    return messages

def deleteMailsServeur(serveur, listeMailsUID):
    logger.info("deleteMailsServeur " + str(serveur) + " - " + str(listeMailsUID))
    if (len(listeMailsUID) > 0):
        with MailBox(serveur.host).login(serveur.user, serveur.password, initial_folder='junk') as mailbox:
            mailbox.delete(listeMailsUID)

def markSpamMailsServeur(serveur, listeMailsUID):
    logger.info("markSpamMailsServeur " + str(serveur) + " - " + str(listeMailsUID))
    if (len(listeMailsUID) > 0):
        with MailBox(serveur.host).login(serveur.user, serveur.password) as mailbox:
            flag=('SPAM_BLOCK_MANUEL',)
            mailbox.flag(listeMailsUID, flags, True)
            mailbox.move(listeMailsUID, 'Junk')

def whitelistMailsServeur(serveur, listeMailsUID):
    logger.info("whitelistMailsServeur " + str(serveur) + " - " + str(listeMailsUID))
    if (len(listeMailsUID) > 0):
        with MailBox(serveur.host).login(serveur.user, serveur.password, initial_folder='junk') as mailbox:
            flag=('WHITELIST_MANUEL',)
            mailbox.flag(listeMailsUID, flags, True)
            mailbox.move(listeMailsUID, 'INBOX')

def addDomains(listeDomains, allow, block):
    logger.info("addDomains " + str(listeDomains) + " - " + str(allow) + " - " + str(block))
    for domain in listeDomains: 
        d = Domain(name=domain, allow=allow, block=block)
        d.save()
