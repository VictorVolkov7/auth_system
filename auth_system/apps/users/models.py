from datetime import timedelta
from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    """Abstract model with timestamps."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated at'),
    )

    class Meta:
        abstract = True


class User(AbstractUser, TimestampedModel):
    """Custom user model with email field."""

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Middle name'),
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name=_('Email Address'),
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users',
        verbose_name=_('Role'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        """
        Uses the model first_name, last_name and email fields.

        Return:
            String representation of User model.
        """
        return f'{self.first_name} {self.last_name} - {self.email}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Role(TimestampedModel):
    """User role model."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Role name'),
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )

    def __str__(self) -> str:
        """
        Uses the model name.

        Return:
            String representation of Role model.
        """
        return self.name

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class BusinessElement(TimestampedModel):
    """
    Application objects to which access rights are assigned

    (for example: users, products, stores, orders, access rules).
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name')
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Description')
    )

    def __str__(self) -> str:
        """
        Uses the model name.

        Return:
            String representation of BusinessElement model.
        """
        return self.name


class AccessRoleRule(TimestampedModel):
    """Access rights for each role and business element."""

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='access_rules',
        verbose_name=_('Role'),
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        related_name='access_rules',
        verbose_name=_('Business element'),
    )

    # Разрешения
    read_permission = models.BooleanField(
        default=False,
        verbose_name=_('Read own'),
    )
    read_all_permission = models.BooleanField(
        default=False,
        verbose_name=_('Read all'),
    )
    create_permission = models.BooleanField(
        default=False,
        verbose_name=_('Create'),
    )
    update_permission = models.BooleanField(
        default=False,
        verbose_name=_('Update own'),
    )
    update_all_permission = models.BooleanField(
        default=False,
        verbose_name=_('Update all'),
    )
    delete_permission = models.BooleanField(
        default=False,
        verbose_name=_('Delete own'),
    )
    delete_all_permission = models.BooleanField(
        default=False,
        verbose_name=_('Delete all'),
    )

    def __str__(self) -> str:
        """
        Uses the Role and BusinessElement fields name.

        Return:
            String representation of AccessRoleRule model.
        """
        return f'{self.role.name} → {self.element.name}'

    class Meta:
        verbose_name = _('Access role rule')
        verbose_name_plural = _('Access role rules')
        unique_together = ('role', 'element')


class Session(TimestampedModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('User')
    )
    session_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Session key')
    )
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active')
    )

    def is_expired(self) -> bool:
        """
        Checks if the session has expired.

        Return:
            True if the session has expired or is inactive, False otherwise.
        """
        return (not self.is_active) or timezone.now() >= self.expire_at

    @classmethod
    def create_session(cls, user: User, minutes: int = 60):
        """
        Uses the model first_name, last_name and email fields.

        Args:
            user: The user instance for which the session is created.
            minutes: Session lifetime in minutes. Default is 60.
        Return:
            Session object.
        """
        return cls.objects.create(
            user=user,
            session_key=token_urlsafe(32),
            expire_at=timezone.now() + timedelta(minutes=minutes),
        )
