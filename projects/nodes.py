from graphene import relay
from graphene_django import DjangoObjectType

from projects.models import Project, Document


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        filter_fields = []
        interfaces = (relay.Node,)


class DocumentNode(DjangoObjectType):
    class Meta:
        model = Document
        filter_fields = []
        interfaces = (relay.Node,)
