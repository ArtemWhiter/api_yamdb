from rest_framework.authtoken import views
from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, UserListViewSet

from .views import TitleViewSet, CommentViewSet, PostViewSet, CategorieViewSet, GenreViewSet


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserListViewSet)
router.register(r'users/(?P<username>\d+)/', UserViewSet)

router.register(r'titles', TitleViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'posts', PostViewSet)


router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
#router.register(r'follow', FollowViewSet, basename='following',)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
