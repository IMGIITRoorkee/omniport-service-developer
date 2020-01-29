from django.conf import settings

from categories.models import Category


def get_category():
    """
    Get or create Category instance with slug
    :return: the found or newly created Category object
    """

    service_name = settings.DISCOVERY.get_app_configuration(
        'developer'
    ).nomenclature.name
    service_verbose = settings.DISCOVERY.get_app_configuration(
        'developer'
    ).nomenclature.verbose_name
    category, _ = Category.objects.get_or_create(
        slug=service_name,
        name=service_verbose,
    )
    return category
