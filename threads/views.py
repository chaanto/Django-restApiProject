from email import message
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ThreadSerializers
from .models import Thread
from boards.views import validate_token
from users.models import User


# Create your views here.

class CreateView(APIView) :
    def post(self, request) :
        payload = validate_token(request)
        
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
            
        if user :
            request.data.update({'uid': user.id})
            serializer = ThreadSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data)

class GetView(APIView) :
    def get(self, request) :
        payload = validate_token(request)
        
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            thread_list = list(Thread.objects.values())
            
            return Response({'data': thread_list})

class UpdateView(APIView) :
    def patch(self, request) :
        thread_id = request.data['id']
        payload = validate_token(request)
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            thread = Thread.objects.filter(id=thread_id).first()
            if user.is_superuser or user.is_staff or thread.uid.id == user.id or thread.board.uid.id == user.id or thread.board.moderator.id == user.id :
                serializer = ThreadSerializers(instance=thread, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                message = 'Data Updated'
            else :
                message = 'Not allowed'
        else :
            message = 'User does not exist'
            
        return Response({
            'message': message
        })

class DeleteView(PermissionRequiredMixin, APIView):
    def delete(self, request) :
        thread_id = request.data['id']
        payload = validate_token(request)
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            thread = Thread.objects.filter(id=thread_id).first()
            if user.is_superuser or user.is_staff or thread.uid.id == user.id or thread.board.uid.id == user.id or thread.board.moderator.id == user.id :
                thread.delete()
                message = 'Data deleted'
            else :
                message = 'Not allowed'
        else :
            message = 'User does not exist!'
            
        return Response({
            'message': message
        })

            
                
