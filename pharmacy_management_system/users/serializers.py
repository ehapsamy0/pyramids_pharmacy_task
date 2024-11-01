from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "name", "role"]

    def get_role(self, obj):
        # if obj.is_patient:
        #     return "patient"
        # elif obj.is_pharmacist:
        #     return "pharmacist"
        return "admin"


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_patient", "is_pharmacist"]

    def validate(self, data):
        """
        Ensure that the user is either a patient or a pharmacist, but not both.
        """
        is_patient = data.get("is_patient", True)  # Default to patient if not provided
        is_pharmacist = data.get("is_pharmacist", False)

        # Validation to ensure at least one of the fields is selected, and they are not both True
        if is_patient and is_pharmacist:
            raise serializers.ValidationError(
                "A user cannot be both a patient and a pharmacist."
            )
        if not is_patient and not is_pharmacist:
            raise serializers.ValidationError(
                "A user must be either a patient or a pharmacist."
            )

        return data

    def create(self, validated_data):
        # Create user with password hashing and correct flags
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_patient=validated_data.get("is_patient", True),
            is_pharmacist=validated_data.get("is_pharmacist", False),
        )
        return user
