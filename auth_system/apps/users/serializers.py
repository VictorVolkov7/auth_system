from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User, AccessRoleRule, Role


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user account."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message=_('This email is already taken.'))]
    )
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'middle_name', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        """
        Validates the input data, ensuring passwords match.

        Args:
            attrs: Dictionary of field values to validate.
        Returns:
            attrs: Validated attributes.
        """
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data: dict) -> User:
        """
        Creates a new user instance with the password hashed.

        Args:
            validated_data: Validated data for creating the user.
        Returns:
            The created user instance.
        """
        validated_data.pop('password_repeat')
        validated_data['password'] = make_password(validated_data['password'])

        if 'role' not in validated_data or validated_data['role'] is None:
            user_role = Role.objects.get(name='Пользователь')
            validated_data['role'] = user_role

        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data representation and updates."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'middle_name', 'role')
        read_only_fields = ('id', 'role')


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    """Serializer for assess role representation/updates and delete."""

    class Meta:
        model = AccessRoleRule
        fields = ('id', 'role', 'element', 'read_permission', 'read_all_permission', 'create_permission',
                  'update_permission', 'update_all_permission', 'delete_permission', 'delete_all_permission')
        read_only_fields = ('id',)
