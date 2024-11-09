from graphene import relay
from graphene_django import DjangoObjectType

from resources.models import Resource


class ResourceNode(DjangoObjectType):
    class Meta:
        model = Resource
        filter_fields = []
        interfaces = (relay.Node,)
