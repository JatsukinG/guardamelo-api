from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from projects.mutations import CreateProject, UpdateProject, DeleteProject, CreateDocument, \
    UpdateDocument, DeleteDocument
from projects.nodes import ProjectNode, DocumentNode


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = DjangoFilterConnectionField(ProjectNode)

    document = relay.Node.Field(DocumentNode)
    documents = DjangoFilterConnectionField(DocumentNode)


class Mutation(ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()

    create_document = CreateDocument.Field()
    update_document = UpdateDocument.Field()
    delete_document = DeleteDocument.Field()
