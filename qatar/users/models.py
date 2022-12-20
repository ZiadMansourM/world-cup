import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES)
    birthday=models.DateField(auto_now=False, null=True, blank=True)
    nationality=models.CharField(max_length=50, null=True, blank=True)
    is_site_admin = models.BooleanField(
        _('site admin status'),
        default=False,
        help_text=_('Designates whether the user is a Site Administrator.'),
    )
    is_manager = models.BooleanField(
        _('manager status'),
        default=False,
        help_text=_('Designates whether the user is a Manager'),
    )
    is_staff = None

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return f"{self.username}"