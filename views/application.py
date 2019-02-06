from rest_framework import viewsets, permissions

from open_auth.models import Application
from open_auth.serializers.application import (
    ApplicationDetailSerializer,
    ApplicationListSerializer,
)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on Application
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ApplicationDetailSerializer
    pagination_class = None

    def get_serializer_class(self):
        """
        Get the appropriate serializer class for the current action
        :return: the appropriate serializer class for the current action
        """

        mapping = {
            'list': ApplicationListSerializer,
        }
        if self.action in mapping:
            return mapping[self.action]

        return super().get_serializer_class()

    def get_queryset(self):
        """
        Filter the queryset to only include only the applications whose team
        includes the current person
        :return: the filtered queryset
        """

        return Application.objects.filter(team_members=self.request.person)
