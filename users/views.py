from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from restApiProject.settings import SECRET_KEY
from .serializers import UserSerializer
from .models import User
from datetime import datetime, timedelta
import jwt 

# Create your views here.

class RegisterView(APIView) :
    def post(self, request) :
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    

class LoginView(APIView) :
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if not user :
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password) :
            raise AuthenticationFailed('Incorrect Email/Password')
        
        payload = {
            'id' : user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow() 
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = ({
            'jwt': token
        })
        
        return response
    
class UserView(APIView) :
    def get(self, request) :
        token = request.COOKIES.get('jwt')
        
        if not token :
            raise AuthenticationFailed('Unauthenticated!')
        
        try :
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignature as e:
            raise AuthenticationFailed(e)
        except :
            raise AuthenticationFailed('Token not valid')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
class LogoutView(APIView) :
    def post(self, request) :
        response = Response()
        response.delete_cookie('jwt')
        
        response.data = {
            'message': 'Success'
        }
        
        return response