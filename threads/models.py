from django.db import models
from users.models import User
from boards.models import Board

# Create your models here.

class Thread(models.Model) :
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    uid = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='thread_uid'
    )
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name