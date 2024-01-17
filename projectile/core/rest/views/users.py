from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from core.permissions import IsAdminUser
from core.models import User
from core.rest.serializers.users import UserListSerializer
from common.renderers import ErrorRenderers


class UserList(ListCreateAPIView):
    """Views to get or create user instance"""

    serializer_class = UserListSerializer
    permission_classes = [
        IsAdminUser,
    ]
    renderer_classes = [
        ErrorRenderers,
    ]
    queryset = User().get_all_actives().select_related("userotp").all()


class UserDetail(RetrieveUpdateAPIView):
    """View to retrieve or update a user instance."""

    serializer_class = UserListSerializer
    permission_classes = [
        IsAdminUser,
    ]
    renderer_classes = [
        ErrorRenderers,
    ]
    queryset = User().get_all_actives()
    lookup_field = "uid"
