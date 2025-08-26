from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove o campo username
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True
    )
    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        # Se username for fornecido, retorna None para ignorar
        return None

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        # Remove username dos dados limpos
        data.pop('username', None)
        return data

    def save(self, request):
        # Remove username dos dados antes de salvar
        validated_data = getattr(self, 'validated_data', {})
        if validated_data and 'username' in validated_data:
            del validated_data['username']
        return super().save(request)
