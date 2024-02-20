from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from services.generator import CodeGenerator
from django.utils.encoding import smart_str, smart_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

    def get_user(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        return authenticate(email=email, password=password)

    def create(self, validated_data):
        return self.get_user()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError({"error": "No account with this email."})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Password is wrong."})

        if not user.is_active:
            raise serializers.ValidationError({"error": "This account is not activate."})

        return super().validate(attrs)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token), "access": str(token.access_token)
        }
        return repr_


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    username = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "mobile",
            "password",
            "password_confirm"
        )
        extra_kwargs = {
            "mobile": {"write_only": True}
        }

    def validate(self, attrs):
        email = attrs.get("email")
        mobile = attrs.get("mobile")
        username = attrs.get("username")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        # Check if email, username, and mobile already exist
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email already exists."})
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({"error": "This username already exists."})
        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError({"error": "This phone number already exists."})

        # Check username length
        if len(username) < 8:
            raise serializers.ValidationError({"error": "Username must be at least 8 characters in length."})

        # Check if passwords match and meet requirements
        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords did not match."})
        if len(password) < 8:
            raise serializers.ValidationError({"error": "Password should contain 8 character at least."})
        if not any(_.isdigit() for _ in password_confirm):
            raise serializers.ValidationError({"error": "The password must contain at least 1 number and letters."})
        if not any(_.isupper() for _ in password_confirm):
            raise serializers.ValidationError({"error": "There must be at least 1 uppercase letter in the password."})
        return super().validate(attrs)

    def create(self, validated_data):
        password_confirm = validated_data.pop("password_confirm")
        user = User.objects.create(
            **validated_data, is_active=False,
            activation_code=CodeGenerator().create_user_activation_code(size=4, model_=User)
        )
        user.set_password(password_confirm)
        user.save()

        # sending verification mail
        send_mail(
            "Activation mail",
            f"Your activation code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True
        )

        return user

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        uuid = urlsafe_base64_encode(smart_bytes(instance.id))
        repr_["uuid"] = uuid
        return repr_


class ActivationSerializer(serializers.ModelSerializer):
    activation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("activation_code",)

    def validate(self, attrs):
        activation_code = attrs.get("activation_code")
        user = self.instance
        if not user.activation_code == activation_code:
            raise serializers.ValidationError({"error": "Kod sefdir."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.activation_code = None
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
        )

    def get_uuid(self, obj):
        return urlsafe_base64_encode(smart_bytes(obj.id))

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError({"error": "There is no user with this e-mail address."})

        if not user.is_active:
            raise serializers.ValidationError({"error": "This account is not activate."})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get("email"))
        user.activation_code = CodeGenerator().create_user_activation_code(size=6, model_=User)
        user.save()

        # send code to email
        send_mail(
            "Reset Password",
            f"Your reset code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True
        )
        return user


class ResetPasswordCheckSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    activation_code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "activation_code",
        )

    def get_uuid(self, obj):
        return urlsafe_base64_encode(smart_bytes(obj.id))

    def validate(self, attrs):
        user = self.instance
        code = attrs.get("activation_code")

        if not user.activation_code == code:
            raise serializers.ValidationError({"error": "Wrong code."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.activation_code = None
        instance.save()
        return instance


class ResetPasswordCompleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_confirm"
        )
        extra_kwargs = {
            "email": {"read_only": True}
        }

    def validate(self, attrs):
        user = self.instance
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if len(password) < 8:
            raise serializers.ValidationError({"error": "Password should contain 8 character at least."})
        if user.check_password(password):
            raise serializers.ValidationError({"error": "You used this password."})
        if not password == password_confirm:
            raise serializers.ValidationError({"error": "Passwords did not match."})
        if not any(_.isdigit() for _ in password_confirm):
            raise serializers.ValidationError({"error": "The password must contain at least 1 number and letters."})
        if not any(_.isupper() for _ in password_confirm):
            raise serializers.ValidationError({"error": "There must be at least 1 uppercase letter in the password."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        user = self.instance
        password = validated_data.get("password")

        user.set_password(password)
        user.activation_code = None
        user.save()
        return user

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token), "access": str(token.access_token)
        }
        return repr_


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "old_password",
            "password",
            "password_confirm"
        )

    def validate(self, attrs):
        password = attrs.get("password")
        old_password = attrs.get("old_password")
        password_confirm = attrs.get("password_confirm")
        user = self.context.get("user")

        if not password == password_confirm:
            raise serializers.ValidationError({"error": "Passwords did not match."})
        if len(password) < 8:
            raise serializers.ValidationError({"error": "Password should contain 8 character at least."})
        if not any(_.isdigit() for _ in password):
            raise serializers.ValidationError({"error": "The password must contain at least 1 number and letters."})
        if not any(_.isupper() for _ in password_confirm):
            raise serializers.ValidationError({"error": "There must be at least 1 uppercase letter in the password."})
        if not user.check_password(old_password):
            raise serializers.ValidationError({"error": "Old password is not correct."})
        if user.check_password(password_confirm):
            raise serializers.ValidationError({"error": "You used this password."})
        return attrs


class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "logo",
            "first_name",
            "last_name",
            "username",
            "bio",
            "birth_day",
            "gender"
        )
        extra_kwargs = {
            "bio": {"write_only": True},
            "logo": {"write_only": True},
            "gender": {"write_only": True},
            "username": {"write_only": True},
            "birth_day": {"write_only": True},
            "last_name": {"write_only": True},
            "first_name": {"write_only": True},
        }

    def validate(self, attrs):
        user = self.instance
        username = attrs.get("username")

        if User.objects.exclude(id=user.id).filter(username__iexact=username).exists():
            raise serializers.ValidationError({"error": "This username already exists."})
        return super().validate(attrs)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token), "access": str(token.access_token)
        }
        return repr_


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "logo",
            "username"
        )
        extra_kwargs = {
            "logo": {"read_only": True},
            "username": {"read_only": True},
        }


class DeleteAccountSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
        )
        extra_kwargs = {
            "email": {"read_only": True}
        }

    def get_uuid(self, obj):
        uuid = urlsafe_base64_encode(smart_bytes(obj.id))
        return uuid

    def create(self, validated_data):
        # Sending a verification password to the email account of the user who wants to delete her account
        user = self.context.get("user")
        user.activation_code = CodeGenerator().create_user_activation_code(size=6, model_=User)
        user.save()
        send_mail(
            "Account Delete",
            f"Your account delete code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True
        )
        return user


class AccountDeleteCheckSerializer(serializers.ModelSerializer):
    activation_code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "activation_code",
        )

    def validate(self, attrs):
        user = self.instance
        activation_code = attrs.get("activation_code")
        # checking the code sent to the e-mail
        if not user.activation_code == activation_code:
            raise serializers.ValidationError({"error": "Wrong code."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        # deleting the account of the user who entered the code correctly
        instance.delete()
        return instance

