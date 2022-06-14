from django.db import models
from users.models import User

# Create your models here.

class Board(models.Model) :
    name = models.CharField(max_length=255)
    uid = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='uid'
    )
    moderator = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='moderator', blank=True, null=True
    )
    
    def __str__(self):
        return self.name
    