from imap_tools import MailBox, AND, MailMessageFlags

import logging

import checkdmarc

logger = logging.getLogger("django")

import time
import traceback
from django.conf import settings
from mailFiltering.models import CheckMailTaskThreaded, Domain
from django_task.job import Job

def checkMail(msg, mailbox) :
    #logger.debug("Msg : " + msg.from_ + " - " msg.to + " - " + msg.subject)
    domain = msg.headers["from"][0].split("@")[1].split(">")[0]
    try :
        domain_block = Domain.objects.get(name=domain, block=True)
    except :
        domain_block = None
    try :
        domain_allow = Domain.objects.get(name=domain, allow=True)
    except :
        domain_allow = None
    flags = ()
    if domain_allow :
        logger.info("Whitelist " + domain)
        fl = ('WHITELIST',)
        flags = flags + fl
        mailbox.flag([msg.uid], flags, True)
    else :
        if domain_block :
            fl = ('SPAM_BLOCKLIST',)
            flags = flags + fl
            logger.info("Blocklist " + domain)
        result = checkdmarc.dmarc.check_dmarc(domain)
        if result["valid"] == False and domain.count(".") > 1:
            domain = domain[domain.find(".")+1:]
            result = checkdmarc.dmarc.check_dmarc(domain)
            logger.debug("Check DMARK for " + domain + " : " + str(result["valid"]))
        if result["valid"] == True and not "dkim-signature" in msg.headers :
            fl = ('SPAM_DKIM',)
            flags = flags + fl
            #logger.info("Msg : " + msg.from_ + " - " msg.to + " - " + msg.subject)
            logger.info("Pretend etre pour le domaine " + domain + " qui a un DKIM mais ne l'utilise pas")
        
        if "dkim-signature" in msg.headers :
            dkim = msg.headers["dkim-signature"]
            isspamdkim = True
            for dv in dkim:
                if dv.find("d=") and isspamdkim:
                    logger.debug(dv)
                    dkimdomain = dv.split("d=")[1].split(";")[0]
                    logger.debug(dkimdomain)
                    if dkimdomain.find(domain) == -1:
                        logger.info("Pretend être pour le domaine " + domain + " qui a un DKIM pour un domaine different")
                    else:
                        isspamdkim = False
                        break
            if isspamdkim:
                fl = ('SPAM_DKIM_DIFF',)
                flags = flags + fl
            
        if msg.from_.find(domain) == -1 :
            fl = ('SPAM_DOMAIN_DIFF',)
            flags = flags + fl
            #logger.info("Msg : " + msg.from_ + " - " msg.to + " - " + msg.subject)
            logger.info("Mail du domaine " + domain + " qui a expéditeur de domaine différent " + msg.from_)
            
        if len(flags) > 0:
            mailbox.flag([msg.uid], flags, True)
            mailbox.move([msg.uid], 'Junk')
        
class checkMailJob(Job):

    @staticmethod
    def execute(job, task):
        serveur = task.serveur
        with MailBox(serveur.host).login(serveur.user, serveur.password) as mailbox:
            while True:
                responses = mailbox.idle.wait(timeout=60)
                if responses:
                    for msg in mailbox.fetch(AND(seen=False), mark_seen=False, reverse=True, bulk=True):
                        checkMail(msg, mailbox)
                else:
                    logger.info('no updates in 60 sec')
