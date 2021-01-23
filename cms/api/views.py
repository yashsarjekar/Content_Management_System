################################## Libraries Required #################################
from django.shortcuts import render
from rest_framework import generics
from .serializer import AuthorSerializer,AdminSerializer
import io
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import permissions
from .backends import JWTAuthorAuthentication,JWTAdminAuthentication
from .serializer import ContentSerializer
import jwt
from rest_framework import authentication,exceptions
from .models import Content,Author,Admin,AdminBlacklistToken,AuthorBlacklistToken
import json
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .utils import generate_access_token,generate_refresh_token
# Create your views here.
################################### Author Section View Code ############################

###### Author Register View #######
class AuthorRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data) #converting json into stream data
        parsed_data = JSONParser().parse(stream_data)#converting stream into python native datatypes
        serializer = AuthorSerializer(data = parsed_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'message':'Author Successfully Registered'}
            return JsonResponse(message)
        return JsonResponse(serializer.errors)

###### Author Login View ############
class AuthorLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        email =  parsed_data.get("email")
        password = parsed_data.get('password')
        author = authenticate(username = email,password=password)
        print(author)
        if author:
            access_token = generate_access_token(author)
            refresh_token = generate_refresh_token(author)
            user = AuthorSerializer(author)
            data = {
                'user': user.data,
                'access_token':access_token,
                'refresh_token':refresh_token,
            }
            #print(auth_token)
            return JsonResponse(data) 
        message = {'message': 'User Not found'}   
        return JsonResponse(message)

####### Author Content View, Create, Update, Delete Operations #######
class AuthorContentView(generics.GenericAPIView):
    authentication_classes = [JWTAuthorAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    ##### Author Content Create View #####
    def post(self,request,*args, **kwargs): 
        serializer = ContentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'Content Created by Author'})
        return JsonResponse(serializer.errors)

    ##### Author Content View #####
    def get(self,request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')
        payload = jwt.decode(token,options={"verify_signature": False})
        email = payload.get('email')
        try:
            contents = Content.objects.filter(email=email)
            serializer = ContentSerializer(contents,many=True)
            return JsonResponse(serializer.data,safe=False)
        except Content.DoesNotExist:
            return JsonResponse({'message':'You Does Not have Content'})

    ##### Author Content Delete ######
    def delete(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        content_id = parsed_data.get('id')
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')
        payload = jwt.decode(token,options={"verify_signature": False})
        email = payload.get('email')
        if content_id:
            try:
                content = Content.objects.get(id = content_id)
                if email == content.email:
                    content.delete()
                    message = {'message':'Content Deleted'}
                    return JsonResponse(message)
                else:
                    message = {'message':'You are not Authorized to Delete this Content'}
                    return JsonResponse(message)
            except Content.DoesNotExist:
                message = {'message': 'Content is not available'}
                return JsonResponse(message)
        else:
            message = {'message': 'Please Provide content id'}
            return JsonResponse(message)
    
    ##### Author Content Update #####
    def put(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        content_id = parsed_data.get('id')
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')
        payload = jwt.decode(token,options={"verify_signature": False})
        email = payload.get('email')
        if content_id:
            try:
                content = Content.objects.get(id = content_id)
                if email == content.email:
                    serializer = ContentSerializer(content,data = parsed_data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        message = {'message':'Content Updated Successfully'}
                        return JsonResponse(message)
                    else:
                        return JsonResponse(serializer.errors)
                else:
                    message = {'message':'You are not Authorized to Update this Content'}
                    return JsonResponse(message)
            except Content.DoesNotExist:
                message = {'message': 'Content is not available'}
                return JsonResponse(message)
        else:
            message = {'message': 'Please Provide content id'}
            return JsonResponse(message)

########## Author Refresh Token ##################
class AuthorRefreshToken(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        try:
            payload = jwt.decode(
                refresh_token,settings.REFRESH_TOKEN_SECRET_KEY,options=jwt_options,
                algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        blacklist = AuthorBlacklistToken.objects.filter(token=refresh_token).exists()
        if blacklist:
            raise exceptions.AuthenticationFailed(
                'Please Login Again.'
            )
        try:
            user = Author.objects.get(email=payload.get('email'))
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        access_token = generate_access_token(user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return JsonResponse(data)

########## Author Logout ##################
class AuthorLogout(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        try:
            payload = jwt.decode(
                refresh_token,settings.REFRESH_TOKEN_SECRET_KEY,options=jwt_options,
                algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')  
        try:
            user = Author.objects.get(email=payload.get('email'))
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        if user:
            token_blacklist = AuthorBlacklistToken(token=refresh_token,user=user)
            token_blacklist.save()
            message = {'message':'You have Logout Successfully'}
            return JsonResponse(message)

########################  Admin Section View Code ##########################

##### Admin Register View ##### 
class AdminRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        python_data = json.loads(request.body)
        for i in range(len(python_data)):
            serializer = AdminSerializer(data = python_data[i])
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse(serializer.errors)
        return JsonResponse({'message':'Admin User is Seeded'})


##### Admin Login View #####
class AdminLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        email =  parsed_data.get("email")
        password = parsed_data.get('password')
        admin = authenticate(username = email,password=password)
        if admin:
            access_token = generate_access_token(admin)
            refresh_token = generate_refresh_token(admin)
            user = AdminSerializer(admin)
            data = {
                'user': user.data,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return JsonResponse(data) 
        message = {'message': 'Admin Not found'}   
        return JsonResponse(message)

##### Admin Content View ########
class AdminContentView(generics.GenericAPIView):
    authentication_classes = [JWTAdminAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        try:
            contents = Content.objects.all()
            serializer = ContentSerializer(contents,many=True)
            return JsonResponse(serializer.data,safe=False)
        except Content.DoesNotExist:
            return JsonResponse({'message':'Content is Not Available'})

    def delete(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        content_id = parsed_data.get('id')
        if content_id:
            try:
                content = Content.objects.get(id = content_id)
                content.delete()
                message = {'message':'Content Deleted'}
                return JsonResponse(message)
            except Content.DoesNotExist:
                message = {'message': 'Content is not available'}
                return JsonResponse(message)
        else:
            message = {'message': 'Please Provide content id'}
            return JsonResponse(message)

    def put(self,request):
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        parsed_data = JSONParser().parse(stream_data)
        content_id = parsed_data.get('id')
        if content_id:
            try:
                content = Content.objects.get(id = content_id)
                serializer = ContentSerializer(content,data = parsed_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    message = {'message':'Content Updated Successfully'}
                    return JsonResponse(message)
                else:
                    return JsonResponse(serializer.errors)
            except Content.DoesNotExist:
                message = {'message': 'Content is not available'}
                return JsonResponse(message)
        else:
            message = {'message': 'Please Provide content id'}
            return JsonResponse(message)

###### Search the Content #######
class SearchContent(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title', '^body','^summary','^categories']
        


############ Admin Refresh Token ##############
class AdminRefreshToken(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        try:
            payload = jwt.decode(
                refresh_token,settings.REFRESH_TOKEN_SECRET_KEY,options=jwt_options,
                algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        blacklist = AdminBlacklistToken.objects.filter(token=refresh_token).exists()
        if blacklist:
            raise exceptions.AuthenticationFailed(
                'Please Login Again.'
            )
        try:
            print(payload.get('email'))
            user = Admin.objects.get(email=payload.get('email'))
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        access_token = generate_access_token(user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return JsonResponse(data)
    

########## Admin Logout ##################
class AdminLogout(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        try:
            payload = jwt.decode(
                refresh_token,settings.REFRESH_TOKEN_SECRET_KEY,options=jwt_options,
                algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')  
        try:
            user = Admin.objects.get(email=payload.get('email'))
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        if user:
            token_blacklist = AdminBlacklistToken(token=refresh_token,user=user)
            token_blacklist.save()
            message = {'message':'You have Logout Successfully'}
            return JsonResponse(message)