from django.urls import include, path
from rest_framework import routers


from .views import (CategorieViewSet, CommentViewSet, GenreViewSet,
                    PostViewSet, TitleViewSet, TokenObtain, UserCreate,
                    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
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
