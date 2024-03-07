from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        if name:
            user.name = name
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Unable to authenticate with provided credentials',
                code='authentication'
            )