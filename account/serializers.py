from rest_framework import serializers
import base64
from io import BytesIO
from PIL import Image
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'name']

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    signature_base64 = serializers.CharField(required=True)
    signature_stroke = serializers.JSONField(required=False, allow_null=True)

    def validate_signature_base64(self, value):
        """Validate if the base64 string is a valid image."""
        try:
            # Check if it starts with a data URL prefix for an image
            if not value.startswith("data:image"):
                raise serializers.ValidationError("Invalid base64 signature format. Must start with 'data:image'.")
            
            # Extract the base64 part by removing the data URL scheme
            base64_data = value.split(",")[1]

            # Try decoding and open the image
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))

            # Verify the image to ensure it's valid and not corrupted
            image.verify()  # This will raise an error if the image is invalid
            
        except Exception as e:
            raise serializers.ValidationError(f"Invalid image: {str(e)}")
        
        return value
    def create(self, validated_data):
        """Create a new User instance."""
        # Extract data
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        name = validated_data.get('name')
        signature_base64 = validated_data.get('signature_base64')
        signature_stroke = validated_data.get('signature_stroke', None)
        
        # Create a new User instance (make sure to save the signature or any other fields)
        user = User.objects.create(
            email=email,
            phone=phone,
            name=name,
            signaturebase64=signature_base64,
            signaturejson=signature_stroke,
        )
        
        return user