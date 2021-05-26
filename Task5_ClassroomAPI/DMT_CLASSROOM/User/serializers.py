from rest_framework import serializers
from User.models import User

class UserDetailSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            user_status=validated_data['user_status']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'id', 'user_status')