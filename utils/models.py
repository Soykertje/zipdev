""" Django models utilities """

# Django
from django.db import models


class BaseModel(models.Model):
    """ Base model
    Act as an abstract model and all the models in the project should inherit from it.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was modified.'
    )

    deleted = models.BooleanField(
        default=False,
        help_text='Set to False when an element is deleted'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
