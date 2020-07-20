from rest_framework import serializers
from sms.models import PhoneNumber


class CustomBaseSerializer(serializers.Serializer):

    def validate(self, data):
        return super().validate(data)


class InboundSerializer(CustomBaseSerializer):
    """
    Serializer class to validate input for Inbound SMS
    """
    _from = serializers.CharField(min_length=6, max_length=16, required=True)
    _to = serializers.CharField(min_length=6, max_length=16, required=True)
    _text = serializers.CharField(min_length=1, max_length=126, required=True)

    def validate(self, data):
        try:
            PhoneNumber.objects.get(number=data["_to"])
        except PhoneNumber.DoesNotExist:
            raise serializers.ValidationError(detail="to parameter not found")
        return data


class OutboundSerializer(CustomBaseSerializer):
    """
    Serializer class to validate input for Outbound SMS
    """
    _from = serializers.CharField(min_length=6, max_length=16, required=True)
    _to = serializers.CharField(min_length=6, max_length=16, required=True)
    _text = serializers.CharField(min_length=1, max_length=126, required=True)

    def validate(self, data):
        try:
            PhoneNumber.objects.get(number=data["_from"])
        except PhoneNumber.DoesNotExist:
            raise serializers.ValidationError(detail="from parameter not found")
        return data





