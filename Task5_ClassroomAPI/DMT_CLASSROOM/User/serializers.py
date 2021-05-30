from rest_framework import serializers

from User.models import User

from django.contrib.auth import authenticate

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

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'id', 'user_status','token')
        read_only_field = ('token',)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)


        if email is None:
            raise serializers.ValidationError(
                'Почта не указана.'
            )


        if password is None:
            raise serializers.ValidationError(
                'Пароль не указан.'
            )


        user = authenticate(username=email, password=password)


        if user is None:
            raise serializers.ValidationError(
                'Пользователь не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Пользователь не активен.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }