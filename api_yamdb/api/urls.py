from rest_framework.authtoken import views
from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CommentViewSet, PostViewSet, CategorieViewSet, GenreViewSet

app_name = 'api'

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'titles', TitleViewSet)
#router.register(r'categories', CategorieViewSet)
#router.register(r'genres', GenreViewSet)
#router.register(r'posts', PostViewSet)


#router.register(
#    r'posts/(?P<post_id>\d+)/comments',
#    CommentViewSet,
#    basename='comment',
#)
#router.register(r'follow', FollowViewSet, basename='following',)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]