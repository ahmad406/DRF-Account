from django.utils.translation import to_locale
from rest_framework import authentication
from rest_framework import permissions
from userapi import models,serializer,permission
from rest_framework import status
from rest_framework import viewsets 
from rest_framework import response, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializer.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self,request):
        '''name'''
        serializer = self.serializer_class (data=request.data)
        if serializer.is_valid():
            name= serializer.validated_data.get('name')
            message= f'hello {name}'
            return Response ({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
    
    def put(self,request,pk=None):
        '''update object'''
        return Response ({'method':'PUT'})
    
    def patch(self,request,pk=None):
        '''update  partial object'''
        return Response ({'method':'PATCH'})

    def delete(self,request,pk=None):
        '''delete object'''
        return Response ({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializer.HelloSerializer
    '''Test API ViewSet'''
    def list(self,request):
        a_viewset = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django ViewSet',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message':'Hello!','a_viewset':a_viewset})
    
    def create(self,request):
        '''Create  a new message '''
        serializer =self.serializer_class(data=request.data)

        if serializer.is_valid():
            name =serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self,request,pk=None):
        '''handle getting an object by its ID '''
        return Response({'http_method ':'GET'})


    def update(self,request,pk=None):
        '''handle updating an object by its ID '''
        return Response({'http_method ':'PUT'})

    def partial_update(self,request,pk=None):
        '''handle part updating an object by its ID '''
        return Response({'http_method ':'PATCH'})

    def destroy(self,request,pk=None):
        '''delete object'''
        return Response ({'method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    '''handling creating and updating profile'''
    serializer_class = serializer.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes =(TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)



class UserLoginApiView(ObtainAuthToken):
    '''Handle creating user authaentication tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''handling creating and updating user feed item'''
    authentication_classes = (TokenAuthentication,)
    serializer_class =serializer.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.UpdateOwnStatus,IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        '''set user profile to logged user'''
        serializer.save(user_profile=self.request.user)

    