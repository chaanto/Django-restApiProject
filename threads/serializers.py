from rest_framework import serializers
from .models import Thread

class ThreadSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Thread
        fields = ['id', 'name', 'content', 'board', 'uid']