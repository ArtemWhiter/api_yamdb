from django.urls import include, path
from rest_framework import routers


from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    TitleViewSet, TokenObtain, UserCreate,
                    UserViewSet, ReviewViewSet)


app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comment',
)

urlpatterns = [
    path('auth/signup/', UserCreate.as_view(), name='create_new_user'),
    path('auth/token/', TokenObtain.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
