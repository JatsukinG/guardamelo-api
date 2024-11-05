from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from projects.nodes import ProjectNode, DocumentNode


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = DjangoFilterConnectionField(ProjectNode)

    document = relay.Node.Field(DocumentNode)
    documents = DjangoFilterConnectionField(DocumentNode)
