from rest_framework.serializers import ModelSerializer

from api.internal.models.store import Transaction
from api.internal.modules.profile.serializers.ProfileSerializer import ProfileSerializer
from api.internal.modules.cart.serializers import OrderSerializer
from api.internal.serializers.RequestSerializer import RequestSerializer
from api.internal.serializers.TransactionFileSerializer import TransactionFileSerializer


class TransactionSerializer(ModelSerializer):
    from_profile = ProfileSerializer(source="source", required=False)
    to_profile = ProfileSerializer(source="destination", required=False)
    order = OrderSerializer(required=False)
    request = RequestSerializer(required=False)
    files = TransactionFileSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ("id", "type", "from_profile", "to_profile", "accrual", "description", "created_at", "order", "request", "files")
        extra_kwargs = {
            "type": {"required": False},
            "description": {"required": True},
            "order": {"required": False},
            "accrual": {"required": False},
        }
