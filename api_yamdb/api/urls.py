from rest_framework.authtoken import views
from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CommentViewSet, ReviewViewSet, CategoryViewSet, GenreViewSet

app_name = 'api'

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
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
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]