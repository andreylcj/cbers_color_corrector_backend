

from django.urls import path
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]