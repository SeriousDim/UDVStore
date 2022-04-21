from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.internal.orders.serializers import OrderSerializer
from api.internal.services.order import get_formed_order_by_transaction, change_status_order_to


class OrderViewSet(GenericViewSet):
    def retrieve(self, request: Request, pk=None) -> Response:
        order = get_formed_order_by_transaction(pk)

        if not order:
            return Response(status=400)

        return Response(data=OrderSerializer(order, context={"request": request}).data)

    def partial_update(self, request: Request, pk=None) -> Response:
        order = get_formed_order_by_transaction(pk)
        data = {"status": request.data.get("status")}

        serializer = OrderSerializer(order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_order = change_status_order_to(order, data["status"])
        if not new_order:
            return Response(status=400)

        return Response(data=OrderSerializer(new_order, context={"request": request}).data)
