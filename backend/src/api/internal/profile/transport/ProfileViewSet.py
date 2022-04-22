from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.internal.models.profile import Profile
from api.internal.models.store import Transaction, TransactionFile, TransactionTypes
from api.internal.profile.serializers.ProfileSerializer import ProfileSerializer
from api.internal.profile.serializers.TransactionSerializer import TransactionSerializer
from api.internal.services.profile import get_profile_history
from api.internal.services.user import get_profile_by_user


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post", "patch", "delete")

    filter_backends = [filters.SearchFilter]
    search_fields = ["^user__first_name", "^user__last_name", "^patronymic"]

    @action(detail=False, methods=['get'])
    def current(self, request):
        cur_user = request.user
        cur_profile = Profile.objects.filter(user=cur_user)[0]
        ser = ProfileSerializer(cur_profile)
        return Response(ser.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        cur_user = request.user
        cur_profile = Profile.objects.filter(user=cur_user)[0]
        transactions = get_profile_history(cur_profile)
        ser = TransactionSerializer(transactions, many=True)
        return Response(ser.data)

    @action(detail=False, methods=['post'])
    def report_activity(self, request):
        ser = TransactionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        td = ser.validated_data
        del td['files']
        nt = Transaction(**td)
        nt.type = TransactionTypes.ACCEPT
        nt.source = get_profile_by_user(request.user)
        nt.save()

        for k, v in request.FILES.items():
            tf = TransactionFile(transaction=nt,
                                 filename=v)
            tf.save()

        return Response(status=200)
