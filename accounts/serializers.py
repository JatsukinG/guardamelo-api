from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    print("user serializer...")
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        # Create user and set unusable password
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()
        return user
