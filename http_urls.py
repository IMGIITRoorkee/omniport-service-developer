from django.urls import include, path

from rest_framework import routers

from developer.views.application import ApplicationViewSet, ApplicationHiddenDetailView

app_name = 'developer'

router = routers.SimpleRouter()
router.register(r'application', ApplicationViewSet, basename='application')

urlpatterns = [
    path('application/secret_data/', ApplicationHiddenDetailView.as_view(), name='hidden-detail'),
    path('', include(router.urls)),
]
