from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.internal.cart.serializers import CartSerializer, TransactionSerializer
from api.internal.models.profile import Profile
from api.internal.models.store import Order
from api.internal.orders.serializers import OrderSerializer
from api.internal.services.cart import (
    validate_new_order,
    get_order,
    validate_amount,
    get_orders_by_user,
    pay, get_orders_by_profile,
)
from api.internal.services.user import get_profile_by_user


class CartViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ("get", "post", "patch", "delete")

    def list(self, request: Request) -> Response:
        orders = get_orders_by_user(request.user)

        serializer = OrderSerializer(orders, many=True, context={"request": request})

        return Response(data=serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        profile = get_profile_by_user(request.user)
        order = get_order(pk, profile)

        if not order:
            return Response(status=404)

        return Response(data=OrderSerializer(order, context={"request": request}).data)

    def create(self, request: Request) -> Response:
        profile = get_profile_by_user(request.user)
        data = self._get_data(request, profile)

        cart_serializer = CartSerializer(data=data)
        cart_serializer.is_valid(raise_exception=True)

        order = cart_serializer.save()
        if validate_new_order(order):
            order.save()

            return Response(data=OrderSerializer(order, context={"request": request}).data)

        return Response(status=400)

    def partial_update(self, request: Request, pk=None) -> Response:
        profile = get_profile_by_user(request.user)
        data = self._get_data(request, profile)

        order = get_order(pk, profile)
        if not order:
            return Response(status=400)

        cart_serializer = CartSerializer(order, data=data, partial=True)
        cart_serializer.is_valid(raise_exception=True)

        updated_order: Order = cart_serializer.save()

        if not validate_amount([updated_order]):
            return Response(status=400)

        updated_order.save()

        return Response(OrderSerializer(updated_order, context={"request": request}).data)

    def destroy(self, request: Request, pk=None) -> Response:
        profile = get_profile_by_user(request.user)
        order = get_order(pk, profile)

        if not order:
            return Response(status=404)

        order.delete()
        return Response(status=200)

    @action(methods=["post"], detail=False,
            url_path="pay", url_name="pay",
            permission_classes=[IsAuthenticated])
    def pay(self, request: Request) -> Response:
        profile = get_profile_by_user(request.user)
        orders = get_orders_by_profile(profile)

        if not orders:
            return Response(status=404)

        transactions = pay(orders)
        if not transactions:
            return Response(status=406)

        return Response(data=TransactionSerializer(transactions, many=True).data)

    def _get_data(self, request: Request, profile: Profile) -> dict:
        data = {
            "profile": profile.id,
            "storage_cell": request.data.get("storage_cell"),
            "amount": request.data.get("amount"),
        }

        return dict((field, value) for field, value in data.items() if value is not None)