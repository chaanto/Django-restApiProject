from itertools import count
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from restApiProject.settings import SECRET_KEY
from .serializers import BoardSerializer
from .models import Board
from users.models import User
from django.db.models import Count
import jwt

# Create your views here.

def validate_token(request) :
    """
        To validate jwt token in cookies
    """
    token = request.COOKIES.get('jwt')
    payload = None
        
    if not token :
        return False
        
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    except :
        payload = False
    
    return payload

class CreateView(APIView) :
    def post(self, request) :
        payload = validate_token(request)
        
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
            
        if user :
            request.data.update({'uid': user.id})
            serializer = BoardSerializer(data=request.data)
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
            board_list = list(Board.objects.values())
            
            return Response({'data': board_list})

class GetSortView(APIView) :
    def get(self, request) :
        payload = validate_token(request)
        
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            board_list = list(Board.objects.order_by('name').values())
            
            return Response({'data': board_list})

class GetGroupByView(APIView) :
    def get(self, request) :
        payload = validate_token(request)
        
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            board_list = (Board.objects
                          .values('name')
                          .annotate(dcount=Count('name'))
                          .order_by()
            )
            
            return Response({'data': board_list})

class UpdateView(APIView) :
    def patch(self, request) :
        board_id = request.data['id']
        payload = validate_token(request)
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            board = Board.objects.filter(id=board_id).first()
            if user.is_superuser or user.is_staff or board.uid.id == user.id :
                serializer = BoardSerializer(instance=board, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                message = 'Data Updated'
            else :
                message = 'Not allowed'
                
        return Response({
            'message': message
        })

class DeleteView(APIView):
    
    def delete(self, request) :
        board_id = request.data['id']
        payload = validate_token(request)
        if payload :
            user = User.objects.filter(id=payload['id']).first()
        else :
            return Response({"message": "The token is not valid"})
        
        if user :
            board = Board.objects.filter(id=board_id).first()
            if user.is_superuser or user.is_staff or board.uid.id == user.id :
                board.delete()
                message = 'Data deleted'
            else :
                message = 'Not allowed'
                
            return Response({
                'message': message
            })

            
                
