from rest_framework import serializers

from api.internal.models.store import Transaction
from api.internal.modules.orders.serializers import OrderSerializer


class FormedOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Transaction
        fields = ("id", "created_at", "order")
