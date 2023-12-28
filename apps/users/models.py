from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from safedelete.models import (HARD_DELETE_NOCASCADE, SOFT_DELETE_CASCADE,
                               SafeDeleteModel)
from simple_history.models import HistoricalRecords

from apps.comun.models import AbstractModel, AbstractNullableModel

# def random_image_chooser():
    # """This defines the default image for the user"""
    # images = [
    #     'profiles/generic/profile_happy.png',
    #     'profiles/generic/profile_kakashi.jpg',
    #     'profiles/generic/profile_whats.jpg',
    # ]
    # i = randrange(3)
    # return images[i]
