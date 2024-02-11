from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from new_pereval.views import PassViewSet, EmailView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = routers.DefaultRouter()
router.register(r'pass', PassViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/submitData/', include(router.urls)),
    path('', include(router.urls)),
    path('api/submitData/user__email=<str:email>', EmailView.as_view(), name='email'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]