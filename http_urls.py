from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers

from developer.views.application import ApplicationViewSet, ApplicationHiddenDetailView

app_name = 'developer'

router = routers.SimpleRouter()
router.register(r'application', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('application/<int:id>/secret_data/',ApplicationHiddenDetailView.as_view(),name="hidden-detail"),
]
