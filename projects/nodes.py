from graphene import relay
from graphene_django import DjangoObjectType

from projects.filtersets import NoteFilterSet
from projects.models import Project, Note


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        filter_fields = []
        interfaces = (relay.Node,)


class NoteNode(DjangoObjectType):
    class Meta:
        model = Note
        filterset_class = NoteFilterSet
        interfaces = (relay.Node,)
