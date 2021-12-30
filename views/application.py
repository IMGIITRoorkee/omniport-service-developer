from rest_framework import response, status
from rest_framework import viewsets, permissions, generics

from open_auth.models import Application
from open_auth.serializers.application import (
    ApplicationDetailSerializer,
    ApplicationListSerializer,
    ApplicationHiddenDetailSerializer,
)

from developer.utils.membership_notifications import (
    send_membership_notification
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

    def update(self, request, *args, **kwargs):
        """
        Update membership status of the application member,
        Update the is_approved status to false if scope is edited
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: response
        """

        application = kwargs.get('pk')
        new_team_members = request.data.get('team_members')
        try:
            application = Application.objects.get(pk=application)
        except Application.DoesNotExist:
            pass
        old_team_members = application.team_members.all()
        old_team_member_ids = list()
        new_team_member_ids = list()
        if old_team_members:
            for old_member in old_team_members:
                old_team_member_ids.append(old_member.id)
        if new_team_members:
            for new_member in new_team_members:
                new_team_member_ids.append(new_member.get('id'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Change approval status to false if data points requested have changed
        data_points = request.data.get('data_points')
        if (data_points 
                and not (set(instance.data_points) == set(data_points))):
            instance.is_approved = False

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if len(old_team_member_ids) > len(new_team_member_ids):
            send_membership_notification(
                application.name,
                'removed from',
                list(set(old_team_member_ids)-set(new_team_member_ids))
            )
        else:
            send_membership_notification(
                application.name,
                'added to',
                list(set(new_team_member_ids)-set(old_team_member_ids))
            )
        return response.Response(serializer.data)


class ApplicationHiddenDetailView(generics.GenericAPIView):
    """
    View details of Application which should not be exposed directly
    """

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        """
        Authenticate if the requesting user is Team Member
        of the application and check the password entered.
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: response containing client_secret
        """

        try:
            data = request.data
            application_id = data.get('id')
            user_password = data.get('password')

            if not all([application_id, user_password]):
                return response.Response(
                    data='Empty application ID or password received.',
                    status=status.HTTP_400_BAD_REQUEST,
                )

            person = request.person
            user = request.user
            user_id = person.id
            application = Application.objects.get(pk=application_id)
            application_team_members = application.team_members

            if application_team_members.filter(id=user_id).exists():

                if user.check_password(user_password):
                    return response.Response(
                        data=ApplicationHiddenDetailSerializer(application).data,
                        status=status.HTTP_200_OK,
                    )

                else:
                    return response.Response(
                        data='Wrong password',
                        status=status.HTTP_403_FORBIDDEN,
                    )

            else:
                return response.Response(
                    data='Requested user is not a team-member.',
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Application.DoesNotExist:
            return response.Response(
                data='Requested application does not exist.',
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError:
            return response.Response(
                data='Incorrect application ID',
                status=status.HTTP_400_BAD_REQUEST,
            )
