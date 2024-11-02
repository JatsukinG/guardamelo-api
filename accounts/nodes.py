from graphene_django import DjangoObjectType
from graphene import relay

from accounts.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = []
        interfaces = (relay.Node,)
