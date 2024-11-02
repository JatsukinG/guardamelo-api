from graphene import relay
from graphene_django import DjangoObjectType

from projects.models import Project, Subproject, SubprojectGroup, Snippet


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        filter_fields = []
        interfaces = (relay.Node,)


class SubProjectNode(DjangoObjectType):
    class Meta:
        model = Subproject
        filter_fields = []
        interfaces = (relay.Node,)


class SubProjectGroupNode(DjangoObjectType):
    class Meta:
        model = SubprojectGroup
        filter_fields = []
        interfaces = (relay.Node,)


class SnippetNode(DjangoObjectType):
    class Meta:
        model = Snippet
        filter_fields = []
        interfaces = (relay.Node,)
