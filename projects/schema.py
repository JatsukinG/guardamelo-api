from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from projects.mutations import CreateProject, UpdateProject, DeleteProject, CreateNote, UpdateNote, DeleteNote
from projects.nodes import ProjectNode, NoteNode


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = DjangoFilterConnectionField(ProjectNode)

    note = relay.Node.Field(NoteNode)
    notes = DjangoFilterConnectionField(NoteNode)


class Mutation(ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()

    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()
