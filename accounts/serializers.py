from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


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


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para visualizar e atualizar dados do perfil do usuário"""

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'is_active']

    def validate_first_name(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Nome deve ter pelo menos 2 caracteres."
            )
        return value.strip() if value else value

    def validate_last_name(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Sobrenome deve ter pelo menos 2 caracteres."
            )
        return value.strip() if value else value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para alteração de senha"""
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """Valida se a senha atual está correta"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def validate_new_password(self, value):
        """Valida a nova senha usando os validadores do Django"""
        validate_password(value)
        return value

    def validate(self, attrs):
        """Valida se a nova senha e confirmação são iguais"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "As senhas não coincidem."
            })
        return attrs

    def save(self):
        """Salva a nova senha"""
        user = self.context['request'].user
        # Type ignore para validated_data do DRF
        new_password = self.validated_data['new_password']  # type: ignore
        user.set_password(new_password)
        user.save()
        return user
