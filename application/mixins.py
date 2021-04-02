"""
A mixin which provides some helper classes for User app
"""

from django.core.serializers import serialize
import json
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from application import settings
from application import models


class UserSerializer(object): 
    """
    This class provide helper methods for user related serializers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context['request']
        self.user = None

    def get_data(self):
        """
        Serialize user and its related objects.
        A serializer must provide self.user to consume this method
        """
        
        try:
            user = serialize('json', [self.user])
        except Exception as e:
            print(e)
    
        user = json.loads(user)[0]['fields']
        user.pop('password')
        user.pop('groups')
        user.pop('is_superuser')
        user.pop('is_staff')
        user.pop('is_active')
        user.pop('user_permissions')
        user.pop('last_login')
        
        try:
            profile = models.Profile.objects.get(user_id=self.user)
            user['profile_media'] = str(profile.profile_media) if str(profile.profile_media)=="" else self.request.build_absolute_uri(str(profile.profile_media.url))
            user['coin'] = profile.coin
            user['cash'] = profile.cash

            app_settings = models.App_Settings.objects.filter()[:1].get()
            user['app_settings_coin'] = app_settings.top_up_coin
        except Exception as e:
            print(e)

        payload = jwt_payload_handler(self.user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        
        user['token'] = token #self.user.auth_token.key
        
        return user