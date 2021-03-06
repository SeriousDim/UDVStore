from django.core.validators import MinValueValidator
from rest_framework import serializers

from api.internal.models import StorageCell
from api.internal.models.order import Order
from api.internal.models.profile import Profile


class CartSerializer(serializers.Serializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    storage_cell = serializers.PrimaryKeyRelatedField(queryset=StorageCell.objects.filter(amount__gt=0))
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])

    def update(self, instance: Order, validated_data: dict) -> Order:
        instance.storage_cell = validated_data.get("storage_cell", instance.storage_cell)
        instance.amount = validated_data.get("amount", instance.amount)

        return instance

    def create(self, validated_data: dict) -> Order:
        return Order(
            profile=validated_data["profile"],
            storage_cell=validated_data["storage_cell"],
            amount=validated_data["amount"],
        )
