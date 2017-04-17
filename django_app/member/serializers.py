"""
Serialize to view user list made by custom user model (MyUser).
커스텀 유저 모델(MyUser)로 생성된 이용자 목록을 직렬화한다.
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize user list.
    이용자 목록 직렬화.
    """

    class Meta:
        model = User
        fields = ('id', 'email')
        ordering = ('id',)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

        else:
            msg = _('이메일 혹은 비밀번호가 맞지 않습니다.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
