from notifications.actions import push_notification

from groups.utils.get_category import get_category


def send_membership_notification(application_name, membership_type, person_id):
    """
    Send appropriate notifications to the application member as per
    the membership_type parameter
    :param application_name: name of the application
    :param membership_type: one of the values, 'added to' or 'removed from'
    :param person_id: id of the person 'added' or 'removed'
    :return: notification
    """

    push_notification(
        template=f'You were {membership_type} the developer group '
                 f'for the application \'{application_name}\'',
        category=get_category(),
        web_onclick_url='',
        android_onclick_activity='',
        ios_onclick_action='',
        is_personalised=True,
        person=person_id[0],
        has_custom_users_target=False,
        persons=None,
    )
