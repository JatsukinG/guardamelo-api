from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from projects.nodes import ProjectNode, SubProjectNode, SubProjectGroupNode, SnippetNode


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = DjangoFilterConnectionField(ProjectNode)

    subproject = relay.Node.Field(SubProjectNode)
    subprojects = DjangoFilterConnectionField(SubProjectNode)

    subproject_group = relay.Node.Field(SubProjectGroupNode)
    subproject_groups = DjangoFilterConnectionField(SubProjectGroupNode)

    snippet = relay.Node.Field(SnippetNode)
    snippets = DjangoFilterConnectionField(SnippetNode)
