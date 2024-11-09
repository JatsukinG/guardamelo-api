from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from resources.mutations import CreateResource, UpdateResource, DeleteResource
from resources.nodes import ResourceNode


class Query(ObjectType):
    resource = relay.Node.Field(ResourceNode)
    resources = DjangoFilterConnectionField(ResourceNode)


class Mutation(ObjectType):
    create_resource = CreateResource.Field()
    update_resource = UpdateResource.Field()
    delete_resource = DeleteResource.Field()
