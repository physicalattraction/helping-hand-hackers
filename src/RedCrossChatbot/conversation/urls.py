from django.urls import path, include
from rest_framework.routers import DefaultRouter
from conversation.views import ConversationViewSet

router = DefaultRouter()
router.register(r'', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]
