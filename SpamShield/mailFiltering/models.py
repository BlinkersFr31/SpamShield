from django.db import models
from django_task.models import TaskThreaded

from des import DesKey

key1 = DesKey(b"FbfTmSHhdhjYVsy4DxxzW57Z")

class Domain(models.Model):
    name = models.CharField(max_length=200)
    allow = models.BooleanField(default=False)
    block = models.BooleanField(default=True)  
    
    def __str__(self):
        usage = ""
        if self.allow :
            usage = "allow"
        elif self.block :
            usage = "block"
        return self.name + " - " + usage
    
class pwdField(models.BinaryField):
    description = "Encrypted password value"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["blank"]
        del kwargs["null"]
        return name, path, args, kwargs
    
    def get_prep_value(self, value):
        if value is None:
            return None
        res = bytes(value, 'utf-8')
        encVal = key1.encrypt(res, padding=True)
        return encVal 

    def from_db_value(self, value, expression, connection):
        if value is None:
          return value
        decVal = key1.decrypt(value, padding=True)
        return str(decVal, 'utf-8')
    
    def to_python(self, value):
        if isinstance(value, Customer):
            return value
        if value is None:
            return value
        decVal = key1.decrypt(value, padding=True)
        return str(decVal, 'utf-8')
    
class Serveur(models.Model):
    host = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    password = pwdField()
    
    def __str__(self):
        return self.host + " - " + self.user

class CheckMailTaskThreaded(TaskThreaded):
    serveur = models.ForeignKey(
        Serveur,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .spam.checkMails import checkMailJob
        return checkMailJob
