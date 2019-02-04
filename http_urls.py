from django.urls import include, path
from rest_framework import routers

from developer.views.application import ApplicationViewSet

app_name = 'developer'

router = routers.SimpleRouter()
router.register(r'application', ApplicationViewSet, base_name='application')

urlpatterns = [
    path('', include(router.urls)),
]
