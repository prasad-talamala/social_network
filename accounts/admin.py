from django.contrib import admin

from accounts.models import PostsModel, SocialConnectivity

admin.site.register(PostsModel)
admin.site.register(SocialConnectivity)