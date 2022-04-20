from django.urls import include, path
from rest_framework import routers


from users.views import UserViewSet

from .views import (AdminUserCreateViewSet, CategorieViewSet, CommentViewSet,
                    GenreViewSet, PostViewSet, TitleViewSet, TokenObtain,
                    UserCreate)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', AdminUserCreateViewSet)
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

urlpatterns = [
    path('auth/signup/', UserCreate.as_view(), name='create_new_user'),
    path('auth/token/', TokenObtain.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
